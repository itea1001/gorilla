import json
import re


def parse_json_function_call(source_code):
    """
    Parse JSON format function calls.
    
    Expected format:
    [
        {"function": "func_name", "parameters": {"param1": value1, "param2": value2}},
        {"function": "func_name2", "parameters": {"param": value}}
    ]
    
    Returns:
    [
        {"func_name": {"param1": value1, "param2": value2}},
        {"func_name2": {"param": value}}
    ]
    """
    # Try to find JSON array in the source code
    json_match = re.search(r"\[\s*{.*?}\s*(?:,\s*{.*?}\s*)*\]", source_code, re.DOTALL)
    if json_match:
        source_code = json_match.group(0)
    
    try:
        json_dict = json.loads(source_code)
    except json.JSONDecodeError as e:
        return []
    
    # Convert from the JSON format to our internal format
    function_calls = []
    for function_call in json_dict:
        if isinstance(function_call, dict):
            function_name = function_call.get("function")
            parameters = function_call.get("parameters", {})
            if function_name:
                function_calls.append({function_name: parameters})
    
    return function_calls

