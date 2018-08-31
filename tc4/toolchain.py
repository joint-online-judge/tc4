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
