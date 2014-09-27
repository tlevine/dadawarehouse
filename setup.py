import os
from distutils.core import setup

setup(name='dadawarehouse',
      author='Thomas Levine',
      author_email='_@thomaslevine.com',
      description='House all of Tom\'s data',
      url='http://small.dada.pink/dadawarehouse',
      packages=['warehouse'],
      install_requires = [
          'picklecache>=0.0.5',
          'requests>=2.3.0',
          'pyzmail>=1.0.3',
          'historian>=0.0.3',
          'SQLAlchemy>=0.9.4',
          'psycopg2>=2.5.4',
      ],
      tests_require = ['nose'],
      scripts = [os.path.join('bin', 'dadawarehouse')],
      version='0.0.1',
      license='AGPL',
      classifiers=[
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3.4',
      ],
)
