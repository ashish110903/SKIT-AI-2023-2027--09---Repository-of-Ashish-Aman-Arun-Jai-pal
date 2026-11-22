import json
from datetime import datetime

def log_experiment(name: str, metrics: dict):
    record = {'timestamp': datetime.utcnow().isoformat(), 'experiment': name, 'metrics': metrics}
    with open('ml/experiments.log', 'a') as f:
        f.write(json.dumps(record) + '\n')
