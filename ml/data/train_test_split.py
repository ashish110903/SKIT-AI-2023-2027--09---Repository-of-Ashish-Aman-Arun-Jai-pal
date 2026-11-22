def train_test_split_dataset(data: list, test_ratio: float = 0.2):
    split_idx = int(len(data) * (1 - test_ratio))
    return data[:split_idx], data[split_idx:]
