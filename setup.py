from setuptools import setup, find_packages

setup(
    name='empowerk12_asana',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'sqlalchemy',
        'pyodbc',
        'python-dotenv',
        'asana',
        'setuptools'
    ],
)