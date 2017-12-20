#!/usr/bin/env python

import sys
import os
import argparse
from jinja2 import Environment, FileSystemLoader
import json
import walkdir # https://walkdir.readthedocs.io/en/stable/#


__VERSION__ = '0.0.2'


def parseArgs():
    description = "A python script to generate CMakeLists.txt of a C/C++ project - {}.".format(__VERSION__)
    parser = argparse.ArgumentParser(description = description)
    parser.add_argument('input_dir', help = 'The base directory of C/C++ project.')
    args = parser.parse_args()
    return args


def genTopLevelDirCMakeListsFile(working_path, subdirs, files):
    """
    Generate top level CMakeLists.txt.

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
    """
    Generate CMakeLists.txt in subdirectories.

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


def readCfgJson(working_path):
    """Read cmWalk configuration data of a working directory from a json file.

    :param working_path: working path for reading the configuration data.
    :return: the configuration data represented in a json object, None if the configuration files does not
             exist.
    """

    CFG_JSON_FILENAME = 'cmwalk.json'
    cfg_json_filename = os.path.join(working_path, CFG_JSON_FILENAME)
    if os.path.isfile(cfg_json_filename):
        with open(cfg_json_filename) as json_file:
            cfg = json.load(json_file)
            return cfg
    return None



def mainFunction():
    args = parseArgs()

    it = walkdir.filtered_walk(args.input_dir,
                              included_files=['*.s', '*.cpp', '*.c', '*.cxx', '*.h', '*.hpp'])

    dir_depth = 0
    for working_path, subdirs, files in it:
        print("Generating CMakeLists.txt in %s..." % working_path)

        # read configuration data of the working path form the json file, 'cfg' will be None if it does not exist.
        cfg = readCfgJson(working_path)
        if cfg:
            if 'sourceDirs' in cfg.keys():
                includedSourceDirs = []
                for subdir in subdirs:
                    if subdir in cfg['sourceDirs']:
                        includedSourceDirs.append(subdir)
                subdirs.clear()
                subdirs.extend(includedSourceDirs)
            elif 'ignoredDirs' in cfg.keys():
                for ignoredDir in cfg['ignoredDirs']:
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

        if dir_depth == 0:
            # generate top level CMakeLists.txt.
            genTopLevelDirCMakeListsFile(working_path, subdirs, files)
        else:
            # generate CMakeLists.txt in subdirectories.
            genSubDirCMakeListsFile(working_path, subdirs, files)
        dir_depth += 1
    print("\nFinished the generation of CMakeLists.txt files!")


if __name__ == '__main__':
    sys.exit(mainFunction())
