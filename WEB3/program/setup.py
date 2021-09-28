from setuptools import setup, find_namespace_packages


setup(
    name='cli_assistant',
    version='1.1',
    description='Program - personal assistant',
    url='https://github.com/OksanaDonchuk/Project3/blob/Nikita/main.py',
    author='Python3 - Project team3',
    author_email='flyingcircus@example.com',
    license='MIT',
    packages=find_namespace_packages(),
    entry_points={
        'console_scripts': ['cli_com=test_gotovo.main:main'],
    }
)
