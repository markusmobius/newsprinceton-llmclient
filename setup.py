from setuptools import setup, find_packages

setup(
    name='LlmClient',
    version='1.0.31',
    description='Python library for LLM client',
    url='https://github.com/markusmobius/newsprinceton-llmclient',
    packages=find_packages(),
    install_requires=[
        'jsonschema',
        'grpcio',
        'requests',
        'protobuf',
        'python-magic'
    ],    
    include_package_data=True
)