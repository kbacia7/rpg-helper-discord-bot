#!.venv/bin python3
from setuptools import setup, find_namespace_packages

setup(
    name='rpgdiscordhelper',
    packages=find_namespace_packages(include=['rpgdiscordhelper.*']),
    install_requires=[
        'discord.py',
        'PyMySQL',
        'pyparsing',
        'pytimeparse',
        'PyYAML',
        'SQLAlchemy',
        'alembic'
    ],
    version='0.1'
)