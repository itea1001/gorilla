import json
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from bfcl_eval.constants.category_mapping import TEST_FILE_MAPPING, VERSION_PREFIX



def main():
    test_categories = [
        "simple",
        "multiple",
        "parallel",
        "parallel_multiple",
        "live_simple",
        "live_multiple",
        "live_parallel",
        "live_parallel_multiple",
    ]

    tot_function_list = []

    for test_category in test_categories:
        test_filename = f"../bfcl_eval/data/{TEST_FILE_MAPPING[test_category]}"

        test_data = []

        with open(test_filename, "r") as f:
            for line in f:
                test_data.append(json.loads(line))

        # print(test_data[0]["function"])

        for test_case in test_data:
            tot_function_list.extend(test_case["function"])

    print(len(tot_function_list))




        

if __name__ == "__main__":
    main()