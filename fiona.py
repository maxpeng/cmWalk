import sys
import os
import walkdir
from jinja2 import Environment, FileSystemLoader

dirTarget = r'''./nucleo_f429zi_freertos_plus_tcp'''


def genTopLevelDirCMakeListsFile(working_path, subdirs, files):
    """Generate top level CMakeLists.txt.

    :param working_path: current working directory
    :param subdirs: a list of subdirectories of current working directory.
    :param files: a list of files in current working directory.
    :return: the full path name of generated CMakeLists.txt.
    """

    env = Environment(loader=FileSystemLoader('.'), trim_blocks=True, lstrip_blocks=True)

    fnameTemplate = 'TopLevel_CMakeLists.txt.jinja2'
    fnameOut = os.path.join(working_path, 'CMakeLists.txt')

    template = env.get_template(fnameTemplate)
    fcontent = template.render({'project_name':os.path.basename(os.path.abspath(working_path)), 'subdirs': subdirs, 'files': files})
    with open(fnameOut, 'w') as f:
        f.write(fcontent)
    return fnameOut


def genSubDirCMakeListsFile(working_path, subdirs, files):
    """Generate CMakeLists.txt in subdirectories.

    :param working_path: current working directory
    :param subdirs: a list of subdirectories of current working directory.
    :param files: a list of files in current working directory.
    :return: the full path name of generated CMakeLists.txt.
    """

    env = Environment(loader=FileSystemLoader('.'), trim_blocks=True, lstrip_blocks=True)

    fnameTemplate = 'SubDir_CMakeLists.txt.jinja2'
    fnameOut = os.path.join(working_path, 'CMakeLists.txt')

    template = env.get_template(fnameTemplate)
    fcontent = template.render({'subdirs': subdirs, 'files': files})
    with open(fnameOut, 'w') as f:
        f.write(fcontent)
    return fnameOut


def mainFunction():
    it = walkdir.filtered_walk(dirTarget,
                              excluded_dirs=['.*', 'build', 'cmake-build-debug'],
                              included_files=['*.s', '*.cpp', '*.c', '*.cxx', '*.h', '*.hpp'])

    dir_depth = 0
    for working_path, subdirs, files in it:
        if dir_depth == 0:
            # generate top level CMakeLists.txt.
            genTopLevelDirCMakeListsFile(working_path, subdirs, files)
        else:
            # generate CMakeLists.txt in subdirectories.
            genSubDirCMakeListsFile(working_path, subdirs, files)
        dir_depth += 1


if __name__ == '__main__':
    sys.exit(mainFunction())
