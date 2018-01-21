#!/usr/bin/env python

import sys
import os
import argparse
from jinja2 import Environment, FileSystemLoader
import json
import walkdir # https://walkdir.readthedocs.io/en/stable/#
from . import version


def parseArgs():
    description = "A python script to generate CMakeLists.txt of a C/C++ project - v{}.".format(version.VERSION)
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('input_dir', help='The base directory of C/C++ project.')
    args = parser.parse_args()
    return args


def getPackagePath():
    """
    Return the full path of this package.
    :return: full path of this package.
    """
    return os.path.dirname(__file__)


class CmWalk(object):
    CFG_JSON_FILENAME = 'cmwalk.json'
    TOP_LEVEL_CMAKELISTS_JINJA2_TEMPLATE = 'TopLevel_CMakeLists.txt.jinja2'
    SUBDIR_CMAKELISTS_JINJA2_TEMPLATE = 'SubDir_CMakeLists.txt.jinja2'


    def __init__(self):
        self.envJinja = Environment(loader=FileSystemLoader(getPackagePath()), trim_blocks=True, lstrip_blocks=True)


    @classmethod
    def readCfgJson(cls, working_path):
        """Read cmWalk configuration data of a working directory from a json file.

        :param working_path: working path for reading the configuration data.
        :return: the configuration data represented in a json object, None if the configuration files does not
                 exist.
        """

        cfg_json_filename = os.path.join(working_path, cls.CFG_JSON_FILENAME)
        if os.path.isfile(cfg_json_filename):
            with open(cfg_json_filename) as json_file:
                cfg = json.load(json_file)
                return cfg
        return None


    def genTopLevelDirCMakeListsFile(self, working_path, subdirs, files, cfg):
        """
        Generate top level CMakeLists.txt.

        :param working_path: current working directory
        :param subdirs: a list of subdirectories of current working directory.
        :param files: a list of files in current working directory.
        :return: the full path name of generated CMakeLists.txt.
        """

        fnameOut = os.path.join(working_path, 'CMakeLists.txt')
        template = self.envJinja.get_template(self.TOP_LEVEL_CMAKELISTS_JINJA2_TEMPLATE)
        fcontent = template.render({'project_name':os.path.basename(os.path.abspath(working_path)),
                                    'subdirs': subdirs,
                                    'files': files,
                                    'cfg': cfg})
        with open(fnameOut, 'w') as f:
            f.write(fcontent)
        return fnameOut


    def genSubDirCMakeListsFile(self, working_path, addToCompilerIncludeDirectories, subdirs, files):
        """
        Generate CMakeLists.txt in subdirectories.

        :param working_path: current working directory
        :param subdirs: a list of subdirectories of current working directory.
        :param files: a list of files in current working directory.
        :return: the full path name of generated CMakeLists.txt.
        """

        fnameOut = os.path.join(working_path, 'CMakeLists.txt')
        template = self.envJinja.get_template(self.SUBDIR_CMAKELISTS_JINJA2_TEMPLATE)
        fcontent = template.render({'addToCompilerIncludeDirectories':addToCompilerIncludeDirectories,
                                    'subdirs': subdirs,
                                    'files': files})
        with open(fnameOut, 'w') as f:
            f.write(fcontent)
        return fnameOut


def main():
    args = parseArgs()

    it = walkdir.filtered_walk(args.input_dir,
                              included_files=['*.s', '*.cpp', '*.c', '*.cxx', '*.h', '*.hpp'])

    cmwalk = CmWalk()

    dir_depth = 0
    for working_path, subdirs, files in it:
        print("Generating CMakeLists.txt in %s..." % working_path)

        # read configuration data of the working path form the json file, 'cfg' will be None if it does not exist.
        cfg = cmwalk.readCfgJson(working_path)
        addToCompilerIncludeDirectories = True
        if cfg:
            if 'sourceDirectories' in cfg.keys():
                includedSourceDirs = []
                for subdir in subdirs:
                    if subdir in cfg['sourceDirectories']:
                        includedSourceDirs.append(subdir)
                subdirs[:] = includedSourceDirs[:]
            elif 'ignoredDirectories' in cfg.keys():
                for ignoredDir in cfg['ignoredDirectories']:
                    try:
                        subdirs.remove(ignoredDir)
                    except:
                        pass
            elif 'ignoredFiles' in cfg.keys():
                for ignoredFile in cfg['ignoredFiles']:
                    try:
                        files.remove(ignoredFile)
                    except:
                        pass

            if 'addToCompilerIncludeDirectories' in cfg.keys():
                addToCompilerIncludeDirectories = cfg['addToCompilerIncludeDirectories']

        if dir_depth == 0:
            # generate top level CMakeLists.txt.
            cmwalk.genTopLevelDirCMakeListsFile(working_path, subdirs, files, cfg)
        else:
            # generate CMakeLists.txt in subdirectories.
            cmwalk.genSubDirCMakeListsFile(working_path, addToCompilerIncludeDirectories, subdirs, files)
        dir_depth += 1
    print("\nFinished the generation of CMakeLists.txt files!")


if __name__ == '__main__':
    sys.exit(main())
