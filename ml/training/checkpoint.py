import json
def save_model_checkpoint(params: dict, path: str):
    with open(path, 'w') as f: json.dump(params, f)
