## setup.py
from setuptools import find_packages, setup

setup(
    name='join-analyzer',
    version='0.1.0',
    packages=find_packages(),
    # install_requires=[
    #     'argparse==1.4.0',
    #     'solc-select==0.2.0',
    #     'slither-analyzer==0.6.11',
    #     'crytic-compile==0.1.0',
    # ],
    entry_points={
        'console_scripts': ['join=join.__main__:main'],
    },
)
