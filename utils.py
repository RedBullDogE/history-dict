class KeyWrapper:
    """
    Util class for addding the ability to bind a key-function to a sequence.
    """

    def __init__(self, seq, key_func):
        self.seq = seq
        self.key_func = key_func

    def __len__(self):
        return len(self.seq)

    def __getitem__(self, k):
        return self.key_func(self.seq[k])
