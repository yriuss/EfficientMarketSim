from setuptools import setup, find_packages

setup(
    name='EfficientMarketSim',
    version='1.0',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'matplotlib',
        'agentpy',
    ],
)