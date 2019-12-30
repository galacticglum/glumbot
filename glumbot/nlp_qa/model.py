import json
import deeppavlov

from glumbot.utils import rmtree
from urllib.parse import urlparse
from enum import Enum
from pathlib import Path
from deeppavlov import train_model

class ModelType(Enum):
    FAST_TEXT = 1,
    TF_IDF_LOG_REG = 2

class Model(object):
    _MODEL_CONFIG_NAMES = {
        ModelType.FAST_TEXT: 'model_config_fasttext.json',
        ModelType.TF_IDF_LOG_REG: 'model_config_tfidf_logreg.json'
    }

    def __init__(self, model_type, data_path, data_format='csv'):
        self.type = model_type
        self.model_config_path = Path(__file__).absolute().parent / Model._MODEL_CONFIG_NAMES[model_type]
        with open(self.model_config_path, 'r') as file:
            model_config = json.load(file)
            model_config['dataset_reader']['data_path'] = data_path
            if 'metadata' in model_config and 'download' in model_config['metadata']:
                for file in model_config['metadata']['download']:
                    if 'always_remove' in file and file['always_remove']:
                        url_path = Path(urlparse(file['url']).path)

                        # Resolve variables
                        root_path = Path(deeppavlov.__file__).parent
                        subdir_path = file['subdir'].format(DEEPPAVLOV_PATH=str(root_path), ROOT_PATH=str(root_path), \
                            MODELS_PATH=str(root_path / 'models'), DOWNLOADS_PATH=str(root_path / 'downloads'))

                        if 'remove_files' in file:
                            for additional_file in file['remove_files']:
                                filepath = Path(subdir_path) / additional_file
                                if filepath.exists(): filepath.unlink()

                        filepath = Path(subdir_path) / (url_path.stem + ''.join(url_path.suffixes))
                        if filepath.exists(): filepath.unlink()

            self.model = train_model(model_config, download=True)

    def predict(self, values):
        prediction = self.model(values)
        if self.type == ModelType.TF_IDF_LOG_REG:
            prediction = [prediction[0][0], max(prediction[1][0])]
        elif self.type == ModelType.FAST_TEXT:
            prediction = [prediction[0][0], prediction[1][0]]

        return prediction