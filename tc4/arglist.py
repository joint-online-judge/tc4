class ArgList:
    def __init__(self):
        self.__args = []

    def add(self, name, value=None, replace=False):
        if not value:
            value = name
            name = None
        if name and not isinstance(name, str):
            raise TypeError(name) from None
        if not value:
            value = []
        elif isinstance(value, str):
            value = [value]
        else:
            value = list(value)
        if replace and name:
            for i, (_name, _value) in enumerate(self.__args):
                if _name == name:
                    self.__args[i][1] = value
                    return
        self.__args.append((name, value))

    def set(self, name, value):
        self.add(name, value, True)
        pass

    def get_args(self):
        args = []
        for arg in self.__args:
            arg[0] and args.append(arg[0])
            arg[1] and args.extend(arg[1])
        return args

    def serialize(self):
        return ' '.join(self.get_args())


# test
if __name__ == '__main__':
    arg_list = ArgList()
    arg_list.set('-o', 'main')
    arg_list.add(['main.cpp', '1.cpp'])
    print(arg_list.serialize())
