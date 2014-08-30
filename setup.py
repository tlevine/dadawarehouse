import os
from distutils.core import setup

setup(name='dadawarehouse',
      author='Thomas Levine',
      author_email='_@thomaslevine.com',
      description='House all of Tom\'s data',
      url='http://small.dada.pink/dadawarehouse',
      packages=['warehouse'],
      install_requires = [
          'historian >= 0.0.2',
      ],
      tests_require = ['nose'],
      scripts = [os.path.join('bin', 'dadawarehouse')],
      version='0.0.1',
      license='AGPL',
)
