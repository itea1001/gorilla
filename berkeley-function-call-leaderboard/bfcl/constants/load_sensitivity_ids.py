
import re
import json

final_test_ids = {
    "simple": [],
    "irrelevance": [],
    "parallel": [],
    "multiple": [],
    "parallel_multiple": [],
    "java": [],
    "javascript": [],
    "live_simple": [],
    "live_multiple": [],
    "live_parallel": [],
    "live_parallel_multiple": [],
    "live_irrelevance": [],
    "live_relevance": [],
    "multi_turn_base": [],
    "multi_turn_miss_func": [],
    "multi_turn_miss_param": [],
    "multi_turn_long_context": [],
    "multi_turn_composite": []
}

with open("./prompt_sensitivity_ids.txt", 'r') as f:
    lines = [line.strip() for line in f]
for line in lines:
    test_id = line
    test_category = re.split(r'\d', line, maxsplit=1)[0]
    test_category = test_category[:len(test_category) - 1]
    if test_category not in final_test_ids.keys():
        print(f"not supported test category {test_category}")
        continue
    final_test_ids[test_category].append(test_id)

with open("/net/scratch2/mingxuanl/gorilla-dev/gorilla/berkeley-function-call-leaderboard/prompt_sensitivity_ids_to_generate.json", 'w') as f:
    json.dump(final_test_ids, f)
    