import json
import sys
import os
import random
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from bfcl_eval.constants.category_mapping import TEST_FILE_MAPPING, VERSION_PREFIX



def get_tot_function_list(
    test_categories: list[str]
) -> list[dict]:

    tot_function_list = []

    for test_category in test_categories:
        test_filename = f"/net/scratch2/mingxuanl/tool_adv/gorilla/berkeley-function-call-leaderboard/bfcl_eval/data/{TEST_FILE_MAPPING[test_category]}"

        test_data = []

        with open(test_filename, "r") as f:
            for line in f:
                test_data.append(json.loads(line))

        for test_case in test_data:
            tot_function_list.extend(test_case["function"])
    
    return tot_function_list

def random_select_function_list(
    test_categories: list[str] = ["simple", "multiple", "parallel", "parallel_multiple", "live_simple", "live_multiple", "live_parallel", "live_parallel_multiple"],
    random_select_num: int = 100,
    seed: int = 42,
):
    random.seed(seed)
    return random.sample(get_tot_function_list(test_categories), random_select_num)