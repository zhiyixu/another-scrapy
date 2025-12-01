import importlib

def load_object(path: str):

    module_name, attr_name = path.rsplit(".", 1)
    module = importlib.import_module(module_name)
    return getattr(module, attr_name)