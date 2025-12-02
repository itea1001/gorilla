from utils import default_decode_ast_prompting, default_decode_execute_prompting

s2 = '''
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

s3 = '[func_name1(params_name1=1, params_name2=False), func_name2(params)]'

s4 = '[{"function": "func1", "parameters": {"param1": false, "param2": {"a": 1}}}, {"function": "func2", "parameters": {"param": [2,3]}}]'

s5 = '[A.func_name1.book_flight({param_name1: {"a": null}, param_name2: "economy"}),func_name2({params: [1,2,3] })]'

s6 = '[func_name1({param_name1: value1, param_name2: value2}),func_name2({params: values})]'

def main():
    print("Testing XML parser:")
    parsed_xml = default_decode_ast_prompting(s2, language="XML")
    print(f"XML result: {parsed_xml}\n")
    
    print("Testing JSON parser:")
    parsed_json = default_decode_ast_prompting(s4, language="JSON")
    print(f"JSON result: {parsed_json}\n")
    
    print("Testing Python parser:")
    parsed_python = default_decode_ast_prompting(s3, language="Python")
    print(f"Python result: {parsed_python}\n")


if __name__ == "__main__":
    main()


'''
program
└── expression_statement
    └── method_invocation
        ├── object: identifier
        ├── name: identifier
        └── arguments: argument_list
            ├── decimal_integer_literal
            └── method_invocation
                ├── object: identifier
                ├── name: identifier
                └── arguments: argument_list
                    ├── decimal_integer_literal
                    └── decimal_integer_literal

'''



'''
Questions:
1. if in the output some values are not python style, e.g. null, false, do we convert them to python style?
'''