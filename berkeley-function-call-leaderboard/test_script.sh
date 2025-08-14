#! /bin/bash


bfcl generate --model gpt-4o-mini-2024-07-18 --test-category single_turn_python_tool_adv --num-threads 32 --result-dir result_1 --random-select-num 1 --seed 42
bfcl generate --model gpt-4o-mini-2024-07-18 --test-category single_turn_python_tool_adv --num-threads 32 --result-dir result_2 --random-select-num 2 --seed 42
# bfcl generate --model gpt-4o-mini-2024-07-18 --test-category single_turn_python_tool_adv --num-threads 32 --result-dir result_4 --random-select-num 4 --seed 42
# bfcl generate --model gpt-4o-mini-2024-07-18 --test-category single_turn_python_tool_adv --num-threads 32 --result-dir result_8 --random-select-num 8 --seed 42
# bfcl generate --model gpt-4o-mini-2024-07-18 --test-category single_turn_python_tool_adv --num-threads 32 --result-dir result_16 --random-select-num 16 --seed 42
# bfcl generate --model gpt-4o-mini-2024-07-18 --test-category single_turn_python_tool_adv --num-threads 32 --result-dir result_32 --random-select-num 32 --seed 42
# bfcl generate --model gpt-4o-mini-2024-07-18 --test-category single_turn_python_tool_adv --num-threads 32 --result-dir result_64 --random-select-num 64 --seed 42
# bfcl generate --model gpt-4o-mini-2024-07-18 --test-category single_turn_python_tool_adv --num-threads 32 --result-dir result_128 --random-select-num 128 --seed 42
# bfcl generate --model gpt-4o-mini-2024-07-18 --test-category single_turn_python_tool_adv --num-threads 32 --result-dir result_256 --random-select-num 256 --seed 42

bfcl evaluate --model gpt-4o-mini-2024-07-18 --test-category single_turn_python_tool_adv --result-dir result_1 --score-dir score_1
bfcl evaluate --model gpt-4o-mini-2024-07-18 --test-category single_turn_python_tool_adv --result-dir result_2 --score-dir score_2
# bfcl evaluate --model gpt-4o-mini-2024-07-18 --test-category single_turn_python_tool_adv --result-dir result_4 --score-dir score_4
# bfcl evaluate --model gpt-4o-mini-2024-07-18 --test-category single_turn_python_tool_adv --result-dir result_8 --score-dir score_8
# bfcl evaluate --model gpt-4o-mini-2024-07-18 --test-category single_turn_python_tool_adv --result-dir result_16 --score-dir score_16
# bfcl evaluate --model gpt-4o-mini-2024-07-18 --test-category single_turn_python_tool_adv --result-dir result_32 --score-dir score_32
# bfcl evaluate --model gpt-4o-mini-2024-07-18 --test-category single_turn_python_tool_adv --result-dir result_64 --score-dir score_64
# bfcl evaluate --model gpt-4o-mini-2024-07-18 --test-category single_turn_python_tool_adv --result-dir result_128 --score-dir score_128
# bfcl evaluate --model gpt-4o-mini-2024-07-18 --test-category single_turn_python_tool_adv --result-dir result_256 --score-dir score_256