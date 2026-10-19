def compute_confusion_matrix(y_true, y_pred):
    tp = sum(1 for t, p in zip(y_true, y_pred) if t == 'CRITICAL' and p == 'CRITICAL')
    fp = sum(1 for t, p in zip(y_true, y_pred) if t != 'CRITICAL' and p == 'CRITICAL')
    fn = sum(1 for t, p in zip(y_true, y_pred) if t == 'CRITICAL' and p != 'CRITICAL')
    tn = sum(1 for t, p in zip(y_true, y_pred) if t != 'CRITICAL' and p != 'CRITICAL')
    return {'TP': tp, 'FP': fp, 'FN': fn, 'TN': tn}
