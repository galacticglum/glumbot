from pathlib import Path
import importlib.util

class Config(object):
    def __init__(self, defaults=None):
        self._CONFIG = {}
        self.loaded_pyfiles = []

        if defaults is not None and isinstance(defaults, dict):
            self._CONFIG = defaults

    def from_pyfile(self, filename, root_path='instance', overwrite=True):
        '''
        Adds a Python file as a configuration file.

        :param filename:
            The name of the configuration file. This can be an absolute or relative path.
        :param root_path:
            The path to the root directory of the configuration file. If a filepath is specified,
            the parent directory is considered the root path. 
        :param overwrite:
            Indicates whether duplicate keys should be overwritten in the configuration. Defaults to `True`.
        '''

        root_path = Path(root_path)

        # If the specified root path was actually a filepath,
        # use the parent directory.
        if root_path.is_file():
            root_path = root_path.parent()

        path = root_path / Path(filename)
        if path.exists():
            spec = importlib.util.spec_from_file_location('{}.py'.format(path.stem), path.resolve())
            config_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(config_module)

            for key in config_module.__dict__:
                if key in self._CONFIG and not overwrite: continue
                self._CONFIG[key] = config_module.__dict__[key]

            self.loaded_pyfiles.append(path)

    def get(self, key):
        '''
        Retrieves the value of the specified key in the configuration object.

        :returns:
            If the key is in the configuration dictionary, the value of the key is returned.
            Otherwise, a value of `None` is returned.
        '''

        return self._CONFIG[key] if key in self._CONFIG else None

    def __getitem__(self, key):
        '''
        Retrieves the value of the specified key in the configuration object.

        :returns:
            If the key is in the configuration dictionary, the value of the key is returned.
            Otherwise, a value of `None` is returned.
        '''

        return self.get(key)