import sys
import os
import yaml
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from string import Template

from LLM_wrapper.base import LLMWrapper
from LLM_wrapper.gpt import GPTWrapper
from LLM_wrapper.logger_config import LoggerConfig
from tool_adv_baseline.utils import random_select_function_list

class LLMTrajectoryJudgeWrapper:

    def __init__(
        self,
        model_name: str,
    ):
        self.model_name = model_name
        self.logger = LoggerConfig.get_logger("LLM Trajectory Judge")
        if "gpt" in self.model_name:
            self.api = GPTWrapper(model_name)
        else:
            raise ValueError(f"Model {self.model_name} not supported")
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "prompt.yaml"), "r") as f:
            self.prompt_templates = yaml.safe_load(f)
        
    def check_single_function_use(
        self,
        function_call: dict,
        function_info: dict,
    ) -> bool:

        func_call_name = list(function_call.keys())[0]
        func_call_params = function_call[func_call_name]
        avail_func_params = function_info["parameters"]["properties"]
        required_params = function_info["parameters"]["required"]

        for param_name, param_value in func_call_params.items():
            if param_name not in avail_func_params:
                return False
            if type(param_value).__name__ != avail_func_params[param_name]["type"]:
                return False
            if "items" in avail_func_params[param_name]:
                # only check nested once for now
                expected_nested_type = avail_func_params[param_name]["items"]["type"]
                for item in param_value:
                    if type(item).__name__ != expected_nested_type:
                        return False
            if "enum" in avail_func_params[param_name]:
                if param_value not in avail_func_params[param_name]["enum"]:
                    return False
        
        for req_param in required_params:
            if req_param not in func_call_params:
                return False

        return True
    
    def preprocess_prompt_check_query_fulfillment(
        self,
        trajectory: dict,
    ) -> bool:
        raw_prompt = self.prompt_templates["check_query_fulfillment"]
        system_prompt = Template(raw_prompt["system"]).substitute()
        user_prompt = Template(raw_prompt["user"]).substitute(
            query=trajectory["prompt"]["question"][0][0]["content"],
            function_calls=trajectory["model_result_raw"]
        )
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        return messages

    
    def batched_judge_trajectory(
        self,
        trajectory_list: list,
        random_select_num: int,
        seed: int,
    ) -> list:
        '''
        Judge the trajectory of a model's response.

        trajectory_list: list of dict in score.json
        random_select_num and seed: used to determine additional functions provided during generation


        Return:
        list of correctness results, 0 or 1



        proposed procedure:
        for each function called, first find same-name functions in list, then use llm to check if function usage is correct
        if all pass, use llm judge to see if the function calls correctly address the query
        '''

        judge_results = []
        pending_trajectories = []
        pending_ids = []

        additional_function_list = random_select_function_list(random_select_num=random_select_num, seed=seed)
        for trajectory in trajectory_list:
            # print('='*20)
            id = trajectory["id"]
            # original_function_list = trajectory["prompt"]["function"]
            # all_function_list = original_function_list + additional_function_list
            if "model_result_decoded" not in trajectory:
                judge_results.append("0")
                continue
            model_result_decoded = trajectory["model_result_decoded"]
            err_index = []
            for item in trajectory["error"]:
                if type(item) == dict:
                    err_index.append(list(item.keys())[0])
            for call_idx, function_call in enumerate(model_result_decoded):
                # print('-'*10)
                # for parallel and parallel_multiple, only check the function calls that are marked incorrect
                if f"Model Result Index {call_idx}" not in err_index and len(err_index) > 0:
                    continue
                function_name = list(function_call.keys())[0]
                func_call_correctness = False
                called_function_doc = {}
                for avail_function in additional_function_list:
                    if function_name == avail_function["name"]:
                        func_call_correctness = self.check_single_function_use(function_call, avail_function)
                        # print(f"checking, num={random_select_num}, id={id}, function call: {function_call}\nfunction doc: {avail_function}")
                        # print(f"check result: {func_call_correctness}")
                        if func_call_correctness:
                            called_function_doc = avail_function
                            break
                if not func_call_correctness:
                    judge_results.append("0")
                    break
            if func_call_correctness:
                judge_results.append("na")
                pending_trajectories.append(trajectory)
                pending_ids.append(id)
        print(pending_ids)
        
        all_msg = []
        
        for trajectory in pending_trajectories:
            messages = self.preprocess_prompt_check_query_fulfillment(trajectory)
            all_msg.append(messages)
        generate_kwargs = {
            "temperature": 0.001,
            "max_tokens": 1024,
        }
        responses = self.api.batched_generate(
            messages=all_msg,
            max_concurrent=32,
            **generate_kwargs,
        )

        for i in range(0, len(judge_results)):
            if judge_results[i] == "na":
                try:
                    resp = responses.pop(0)
                except IndexError:
                    judge_results[i] = "0"
                    self.logger.warning("Batched judge error!")
                if resp.lower() == "yes":
                    judge_results[i] = "1"
                else:
                    judge_results[i] = "0"
        
        return judge_results

                        







