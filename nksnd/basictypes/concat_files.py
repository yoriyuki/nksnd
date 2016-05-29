def concat(files):
    for file in files:
        for line in file:
            yield line
