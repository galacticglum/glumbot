import json
from pathlib import Path
from deeppavlov import train_model

_MODEL_CONFIG_NAME = 'base_model_config.json'

def init_model(data_path, data_format='csv'):
    model_config_path = Path(__file__).absolute().parent / _MODEL_CONFIG_NAME
    with open(model_config_path, 'r') as file:
        model_config = json.load(file)
        model_config['dataset_reader']['data_path'] = data_path
        model = train_model(model_config, download=True)
        return model