class SpecialDict(dict):
    def __setitem__(self, key, value):
        if key in super(SpecialDict, self).keys():
            values = super(SpecialDict, self).pop(key)
            values = set(values)
            values.add(value)
        elif key not in super(SpecialDict, self).keys():
            values = set()
            values.add(value)
        super(SpecialDict, self).__setitem__(key, values)