import ast
import json
import xml.etree.ElementTree as ET


def parse_xml_function_call(source_code):
    """
    Parse XML format function calls.
    
    Expected format:
    <function_calls>
      <function name="func1">
        <arg name="arg1">value1</arg>
        <arg name="arg2">value2</arg>
      </function>
      <function name="func2">
        <arg name="param1">value</arg>
      </function>
    </function_calls>
    
    Returns:
    [
        {"func1": {"arg1": value1, "arg2": value2}},
        {"func2": {"param1": value}}
    ]
    """
    try:
        root = ET.fromstring(source_code)
    except ET.ParseError as e:
        # If parsing fails, try to find the function_calls block
        import re
        match = re.search(r"<function_calls>.*?</function_calls>", source_code, re.DOTALL)
        if match:
            try:
                root = ET.fromstring(match.group(0))
            except ET.ParseError:
                return []
        else:
            return []
    
    results = []
    
    # Find all function elements
    function_elements = root.findall(".//function")
    
    for func in function_elements:
        func_name = func.attrib.get("name")
        if not func_name:
            continue
        
        param_dict = {}
        
        # Find all arg elements within this function
        for arg in func.findall("arg"):
            arg_name = arg.attrib.get("name")
            arg_value = arg.text if arg.text else ""
            
            # Convert the value to appropriate Python type
            arg_value = _convert_value(arg_value.strip())
            
            if arg_name:
                param_dict[arg_name] = arg_value
        
        results.append({func_name: param_dict})
    
    return results


def _convert_value(value_str):
    """
    Convert string value to appropriate Python type.
    Handles: null, true, false, numbers, strings, lists, dicts
    """
    value_str = value_str.strip()
    
    # Handle JSON keywords
    if value_str == "null":
        return None
    elif value_str == "true":
        return True
    elif value_str == "false":
        return False
    
    # Try to parse as JSON (handles numbers, lists, dicts, strings)
    try:
        return json.loads(value_str)
    except (json.JSONDecodeError, ValueError):
        pass
    
    # Try Python literal eval for complex types
    try:
        return ast.literal_eval(value_str)
    except (ValueError, SyntaxError):
        pass
    
    # Return as string if all else fails
    return value_str

