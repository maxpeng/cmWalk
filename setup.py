from setuptools import setup, find_packages
from cmwalk import version

setup(name='cmwalk',
      version=version.VERSION,
      description='A python script to walk subdirectories of a C/C++ project of embedded system to generate CMakeLists.txt files for building the executable.',
      keywords = ['cmake'],
      url='https://github.com/maxpeng/cmWalk',
      author='Max Peng',
      author_email='max.peng1768@gmail.com',
      license='MIT',
      packages=find_packages(),
      install_requires=['jinja2', 'walkdir'],
      package_data={
          # If any package contains *.txt or *.rst files, include them:
          'cmwalk': ['*.jinja2', '../README.md'],
      },
      entry_points={
          'console_scripts': [
              'cmwalk = cmwalk.cmwalk:mainFunction'
          ]
      },
      zip_safe=False)
