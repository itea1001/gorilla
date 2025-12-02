from model_config import MODEL_CONFIG_MAPPING


for model_name in MODEL_CONFIG_MAPPING:
    if "FC" in MODEL_CONFIG_MAPPING[model_name].display_name and MODEL_CONFIG_MAPPING[model_name].is_fc_model == False:
        print(model_name, MODEL_CONFIG_MAPPING[model_name].display_name)