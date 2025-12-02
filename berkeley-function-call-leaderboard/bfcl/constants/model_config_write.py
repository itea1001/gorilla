import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from model_handler.handler_map import HANDLER_MAP
from eval_config import UNDERSCORE_TO_DOT
from model_metadata import MODEL_METADATA_MAPPING, INPUT_PRICE_PER_MILLION_TOKEN, OUTPUT_PRICE_PER_MILLION_TOKEN

f = open("./tmp.txt", "w")
sys.stdout = f

all_model_names = []
for key in HANDLER_MAP.keys():
    all_model_names.append(key)


for i in range(0, len(all_model_names)):
    model_name = all_model_names[i]
    model_display_name = MODEL_METADATA_MAPPING[model_name][0]
    model_url = MODEL_METADATA_MAPPING[model_name][1]
    model_organization = MODEL_METADATA_MAPPING[model_name][2]
    model_license = MODEL_METADATA_MAPPING[model_name][3]
    model_handler = HANDLER_MAP[model_name]
    model_input_price = INPUT_PRICE_PER_MILLION_TOKEN.get(model_name, None)
    model_output_price = OUTPUT_PRICE_PER_MILLION_TOKEN.get(model_name, None)
    is_fc_model = "FC" in model_name
    underscore_to_dot = model_name in UNDERSCORE_TO_DOT
    print(f"""\"{model_name}\": ModelConfig(
    model_name=\"{model_name}\",
    model_display_name=\"{model_display_name}\",
    model_url=\"{model_url}\",
    model_organization=\"{model_organization}\",
    model_license=\"{model_license}\",
    model_handler={model_handler.__name__},
    input_price={model_input_price},
    output_price={model_output_price},
    is_fc_model={is_fc_model},
    underscore_to_dot={underscore_to_dot},
),""")