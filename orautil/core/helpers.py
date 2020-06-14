class SpecialDict(dict):
    def __init__(self, *args, **kwargs):
        self.update(*args, **kwargs)
        super(SpecialDict, self).__init__(*args, **kwargs)

    def __setitem__(self, key, value):
        if key in dict.keys(self):
            values = dict.pop(self, key)
            values = set(values)
            values.add(value)
        elif key not in dict.keys(self):
            values = set()
            values.add(value)
        values = list(values)
        values.sort()
        dict.__setitem__(self, key, values)

    def __getitem__(self, key):
        return dict.__getitem__(self, key)
