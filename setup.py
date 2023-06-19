from setuptools import setup

setup(name='gpioButton',
      version='0.0.1',
      description='CraftBeerPi Plugin',
      author='',
      author_email='',
      url='',
      include_package_data=True,
      package_data={
        # If any package contains *.txt or *.rst files, include them:
      '': ['*.txt', '*.rst', '*.yaml'],
      'gpioButton': ['*','*.txt', '*.rst', '*.yaml']},
      packages=['gpioButton'],
     )