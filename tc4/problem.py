from os import path, makedirs
from shutil import copytree, rmtree, move
from tempfile import mkdtemp
from zipfile import ZipFile

from tc4.util import movechilden


class Problem:
    def __init__(self, file):
        self.zip_file = ZipFile(file)
        # make case insensitive in tc4
        self.canonical_dict = dict((name.lower(), name) for name in self.zip_file.namelist())

    def open(self, name):
        try:
            return self.zip_file.open(self.canonical_dict[name.lower()])
        except KeyError:
            raise FileNotFoundError(name) from None

    def extract(self, name, dest, subfolder=True):
        extract_dir = mkdtemp('tc4.zipfile')
        file_found = False
        dirname = path.dirname(name) + '/'

        if not name.endswith('/'):
            if name.lower() in self.canonical_dict:
                # single file
                self.zip_file.extract(self.canonical_dict[name.lower()], path=extract_dir)
                file_found = True
            else:
                dirname = name + '/'

        if not file_found:
            if dirname.lower() in self.canonical_dict:
                # directory
                file_found = True
                for compressed_file in self.canonical_dict:
                    if compressed_file.startswith(dirname.lower()):
                        self.zip_file.extract(self.canonical_dict[compressed_file], path=extract_dir)

        if file_found:
            if not path.isdir(dest):
                makedirs(dest)
            if name.endswith('/'):
                movechilden(path.join(extract_dir, dirname), dest)
            else:
                movechilden(path.join(extract_dir, name), dest)

        rmtree(extract_dir)

        if not file_found:
            raise FileNotFoundError(name) from None

def load_problem(file):
    return Problem(file)


# test
if __name__ == '__main__':
    problem = load_problem('example/test.zip')
    print(problem.canonical_dict)
    problem.extract('compile', 'example/folder')
