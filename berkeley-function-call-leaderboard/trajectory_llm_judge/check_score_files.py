import sys
import os
import yaml
import json
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from string import Template
import matplotlib.pyplot as plt

from LLM_wrapper.base import LLMWrapper
from LLM_wrapper.gpt import GPTWrapper
from LLM_wrapper.logger_config import LoggerConfig

from trajectory_llm_judge.llm_judge_wrapper import LLMTrajectoryJudgeWrapper



def main():
    model_name = "gpt-4.1"
    llm_judge = LLMTrajectoryJudgeWrapper(model_name)

    all_avr_acc = []

    save_img = False

    random_select_nums = [0,1,2,4,8,16,32,64,128,256]
    for random_select_num in random_select_nums:
        gen_model_name = "gpt-4o-mini-2024-07-18"
        test_categories = [
            "simple",
            "parallel",
            "multiple",
            "parallel_multiple",
            "live_simple",
            "live_parallel",
            "live_multiple",
            "live_parallel_multiple",
        ]

        adjusted_acc_list = []

        for test_category in test_categories:
            score_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), f"score_{random_select_num}/{gen_model_name}/BFCL_v3_{test_category}_score.json")
            score_data = []
            with open(score_file, "r") as f:
                for line in f:
                    if line.strip():
                        score_data.append(json.loads(line.strip()))
            metadata = score_data[0]
            n_correct = metadata["correct_count"]
            trajectories = score_data[1:]
            judge_results = llm_judge.batched_judge_trajectory(trajectories, random_select_num, 42)
            for judge_result in judge_results:
                if judge_result == "1":
                    n_correct += 1
            
            adjusted_acc = float(n_correct / metadata["total_count"])
            adjusted_acc_list.append(adjusted_acc)

            print(f"for num={random_select_num}, test_category={test_category}, added n_correct={n_correct - metadata['correct_count']}")
        
        avr_acc = float(sum(adjusted_acc_list) / len(adjusted_acc_list))
        all_avr_acc.append(avr_acc)
    
    print(all_avr_acc)

    x_plot = [0.5 if x == 0 else x for x in random_select_nums]

    plt.figure(figsize=(10, 6))
    plt.semilogx(x_plot, all_avr_acc, marker='o', linewidth=2, markersize=6)
    plt.xlabel('number of additional functions (log scale)')
    plt.ylabel('avr acc')

    # Custom x-axis labels to show the real values
    plt.xticks(x_plot, random_select_nums)
    plt.grid(True, alpha=0.3)
    
    if save_img:
        plt.savefig('./accuracy_plot.png', dpi=300)


                
            



if __name__ == "__main__":
    main()