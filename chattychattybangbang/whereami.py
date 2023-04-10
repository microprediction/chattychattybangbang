import os
import pathlib

ROOT_PATH = str(pathlib.Path(os.path.dirname(os.path.realpath(__file__))).parent)

if __name__=='__main__':
    print(ROOT_PATH)