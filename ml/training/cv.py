def k_fold_split(items: list, k: int = 5):
    n = len(items)
    return [items[i::k] for i in range(k)]
