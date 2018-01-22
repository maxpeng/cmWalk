from setuptools import setup, find_packages
import os
# To use a consistent encoding
from codecs import open
from cmwalk import version


# Get the long description from the README file
def readme():
    here = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
        return f.read().replace('\r', '')


setup(name='cmwalk',
      version=version.VERSION,
      description='A python script to walk subdirectories of a C/C++ project of embedded system to generate CMakeLists.txt files for building the executable.',
      long_description=readme(),
      long_description_content_type='text/x-rst; charset=UTF-8',
      keywords = ['cmake'],
      classifiers=[],
      url='https://github.com/maxpeng/cmWalk',
      author='Max Peng',
      author_email='max.peng1768@gmail.com',
      license='MIT',
      packages=find_packages(),
      include_package_data=True,
      install_requires=['jinja2', 'walkdir'],
      entry_points={
          'console_scripts': [
              'cmwalk = cmwalk.cmwalk:main'
          ]
      },
      zip_safe=False)
