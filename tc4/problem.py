from os import makedirs, path
from shutil import rmtree
from tempfile import mkdtemp
from ruamel import yaml
from zipfile import ZipFile

from tc4.case import Case
from tc4.toolchain import ToolChain
from tc4.util import movechilden


class Problem:
    def __init__(self, file):
        self.zip_file = ZipFile(file)
        # make case insensitive in tc4
        self.canonical_dict = dict((name.lower(), name) for name in self.zip_file.namelist())
        self.extract_dir = mkdtemp(prefix='tc4.zipfile.')
        self.__config_loaded = None
        self.__toolchains = dict()
        self.cases = list()

    def __del__(self):
        rmtree(self.extract_dir)

    def open(self, name):
        try:
            return self.zip_file.open(self.canonical_dict[name.lower()])
        except KeyError:
            raise FileNotFoundError(name) from None

    def extract(self, name, dest):
        file_found = False
        name = name.lstrip('/')
        head, tail = path.split(name)

        if not name.endswith('/'):
            if name.lower() in self.canonical_dict:
                # single file
                file_found = True
                self.zip_file.extract(self.canonical_dict[name.lower()], path=self.extract_dir)
            else:
                head = name
                dest = path.join(dest, tail)

        if not file_found and (head == '' or head.lower() + '/' in self.canonical_dict):
            # directory
            file_found = True
            for compressed_file in self.canonical_dict:
                if compressed_file.startswith(head.lower()):
                    self.zip_file.extract(self.canonical_dict[compressed_file], path=self.extract_dir)

        if file_found:
            if not path.isdir(dest):
                makedirs(dest)
            movechilden(path.join(self.extract_dir, head), dest)
        else:
            raise FileNotFoundError(name) from None

    def load_config(self, filename='config.yaml', reload=False):
        if self.__config_loaded == filename and not reload:
            return
        data = yaml.safe_load(self.open(filename))
        if 'toolchains' in data:
            for name, toolchain in data['toolchains']:
                if name in self.__toolchains:
                    raise ValueError('Toolchain %s redefined' % name) from None
                self.__toolchains[name] = ToolChain(toolchain)
        if 'cases' in data:
            for case in data['cases']:
                self.cases.append(Case(case))
        self.__config_loaded = filename

    def get_toolchain(self, name):
        if name not in self.__toolchains:
            raise ValueError('Toolchain %s not found' % name) from None
        toolchain = self.__toolchains[name]
        result = list()
        for tool in toolchain:
            if tool.type == 'toolchain':
                result.extend(self.get_toolchain(tool.name))
            else:
                result.append(tool)
        return result
    

def load_problem(file):
    return Problem(file)


# test
if __name__ == '__main__':
    problem = load_problem('example/test.zip')
    print(problem.canonical_dict)
    problem.extract('', 'example/folder')
    problem.load_config()
