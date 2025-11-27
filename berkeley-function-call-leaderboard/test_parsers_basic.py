"""
Basic functionality tests for JSON and XML parsers
"""
import sys
sys.path.insert(0, '/net/scratch2/mingxuanl/gorilla-dev/gorilla/berkeley-function-call-leaderboard')

from bfcl.model_handler.parser.json_parser import parse_json_function_call
from bfcl.model_handler.parser.xml_parser import parse_xml_function_call

print("=" * 70)
print("BASIC PARSER TESTS")
print("=" * 70)

# Test 1: XML Parser
print("\n1. XML Parser - Basic Test")
xml_input = '''
<function_calls>
  <function name="func1">
    <arg name="arg1">null</arg>
    <arg name="arg2">"abc"</arg>
  </function>
  <function name="func2">
    <arg name="param1">[1,2,3]</arg>
  </function>
</function_calls>
'''

xml_result = parse_xml_function_call(xml_input)
print(f"Input: <function_calls> with 2 functions")
print(f"Output: {xml_result}")
print(f"Expected: [{{'func1': {{'arg1': None, 'arg2': 'abc'}}}}, {{'func2': {{'param1': [1, 2, 3]}}}}]")
print(f"Status: {'✓ PASS' if len(xml_result) == 2 and 'func1' in xml_result[0] and 'func2' in xml_result[1] else '✗ FAIL'}")

# Test 2: JSON Parser
print("\n2. JSON Parser - Basic Test")
json_input = '[{"function": "func1", "parameters": {"param1": false, "param2": {"a": 1}}}, {"function": "func2", "parameters": {"param": [2,3]}}]'

json_result = parse_json_function_call(json_input)
print(f'Input: [{{"function": "func1", "parameters": ...}}, ...]')
print(f"Output: {json_result}")
print(f"Expected: [{{'func1': {{'param1': False, 'param2': {{'a': 1}}}}}}, {{'func2': {{'param': [2, 3]}}}}]")
print(f"Status: {'✓ PASS' if len(json_result) == 2 and 'func1' in json_result[0] and 'func2' in json_result[1] else '✗ FAIL'}")

print("\n" + "=" * 70)
print("Tests complete!")
print("=" * 70)

