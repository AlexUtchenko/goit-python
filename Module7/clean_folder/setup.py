from setuptools import setup, find_namespace_packages

setup(
    name='clean_folder',
    version='1',
    description='The first useful script',
    url='http://github.com/',
    author='Alex Utchenko',
    author_email='',
    license='',
    packages=find_namespace_packages(),
    install_requires=[],
    entry_points={'console_scripts': ['clean-folder = clean_folder.clean()']}
    )
