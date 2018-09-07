from copy import copy, deepcopy
from os import path
from ruamel import yaml

from tc4.arglist import ArgList


def load_config(filename=None):
    global config
    if not filename:
        filename = path.join(path.dirname(__file__), 'toolchain.yaml')
    pass
    with open(filename) as file:
        data = yaml.safe_load(file)
        __config = dict()
        for name, tool in data:
            if __config.__contains__(name):
                raise ValueError('Tool %s redefined' % name) from None
            __config[name] = Tool(name, tool)
        config = __config


def get_config():
    if not config:
        load_config()
    return config


class Tool:
    def __init__(self, name, data):
        if 'type' not in data:
            raise ValueError('Type undefined ') from None
        # self.type = 'type' in data and data['type'] or 'system'
        self.name = name
        self.extends = 'base'
        for key, value in data:
            self.__setattr__(key, value)
        if hasattr(self, 'execute_args'):
            self.__execute_args = ArgList(self.execute_args[0])
            self.add_args(self.execute_args[1:])

    def __getattribute__(self, item):
        if item == 'execute_args':
            return self.__execute_args
        else:
            return self.__dict__[item]

    def extend(self, data):
        self.extends = 'extends' in data and data['extends'] or 'base'
        pass

    def add_args(self, execute_args):
        for arg in execute_args:
            self.__execute_args.add(arg)


class ToolChain:
    def __init__(self, problem, name, data):
        self.__problem = problem
        self.__name = name
        self.__data = list()
        map(self.add_tool, data)
        self.__tools_loaded = False
        self.__tools = None

    def __iter__(self):
        self.__load_tools()
        return iter(self.__tools)

    def __len__(self):
        self.__load_tools()
        return len(self.__tools)

    def __getitem__(self, item):
        self.__load_tools()
        return self.__tools[item]

    def __setitem__(self, key, value):
        self.__load_tools()
        self.__tools[key] = value
        return self.__tools[key]

    def __copy__(self):
        obj = ToolChain(self.__problem, self.__name, [])
        obj.__data = copy(self.__data)

    def add_tool(self, tool):
        if 'type' not in tool:
            raise ValueError('Key \'%s\' not found' % 'type')
        if 'extends' not in tool:
            raise ValueError('Key \'%s\' not found' % 'extends')
        if 'name' not in tool:
            tool['name'] = tool['extends']
        self.__data.append(tool)
        self.__tools_loaded = False

    def __load_tools(self, used_name=None):
        if not self.__tools_loaded:
            if self.__name not in self.__problem.__toolchains:
                raise ValueError('Toolchain %s not found' % self.__name) from None
            self.__tools = list()
            for tool in self.__data:
                if tool.type == 'toolchain':
                    if not used_name:
                        used_name = set()
                    used_name.add(self.__name)
                    if tool.name in used_name:
                        raise ValueError('Toolchain %s loop dependency found' % tool.name) from None
                    toolchain = self.__problem.get_toolchain(tool.name)
                    self.__tools.extend(toolchain.__load_tools(used_name))
                else:
                    self.__tools.append(tool)
            self.__tools_loaded = True
        return self.__tools
