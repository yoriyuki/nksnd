def collation_features(mrphs):
    for i in range(len(mrphs)):
        features = set([m.key() for m in mrphs[0:i-1]])
        (features, mrphs[i].key())
