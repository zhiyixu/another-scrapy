import importlib 

def dload(p: str):

    module_name, class_name = p.rsplit(".", 1)
    module = importlib.import_module(module_name)
    return getattr(module, class_name)