import os
from distutils.core import setup

setup(name='dadawarehouse',
      author='Thomas Levine',
      author_email='_@thomaslevine.com',
      description='House all of Tom\'s data',
      url='http://small.dada.pink/dadawarehouse',
      packages=['warehouse'],
      install_requires = [
          'pylev>=1.2.0',
          'pyzmail>=1.0.3',
          'historian>=0.0.2',
          'SQLAlchemy>=0.9.4',
          'psycopg2>=2.5.4',
      ],
      tests_require = ['nose'],
      scripts = [os.path.join('bin', 'dadawarehouse')],
      version='0.0.1',
      license='AGPL',
)
