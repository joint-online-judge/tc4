class ArgList:
    def __init__(self, main=''):
        self.__main = main
        self.__data = []
        self.__args_loaded = False
        self.__args = [self.__main]

    def add(self, data, replace=False):
        if isinstance(data, str):
            data = data.split(' ')
        if not len(data):
            return
        if data[0].startswith('-'):
            name = data[0]
            value = data[1:]
        else:
            name = None
            value = data

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
            for i, (_name, _value) in enumerate(self.__data):
                if _name == name:
                    self.__data[i][1] = value
                    return
        self.__data.append((name, value))
        self.__args_loaded = False

    def set(self, name, value):
        self.add(name, value, True)

    def set_main(self, main):
        self.__args[0] = self.__main = main

    def get_main(self):
        return self.__main

    def get_args(self):
        if not self.__args_loaded:
            self.__args = [self.__main]
            for arg in self.__data:
                arg[0] and self.__args.append(arg[0])
                arg[1] and self.__args.extend(arg[1])
            self.__args_loaded = True
        return self.__args

    def serialize(self):
        return ' '.join(self.get_args())


# test
if __name__ == '__main__':
    arg_list = ArgList('g++')
    arg_list.set('-o', 'main')
    arg_list.add(['main.cpp', '1.cpp'])
    print(arg_list.serialize())
