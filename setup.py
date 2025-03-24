from setuptools import setup,find_packages
from typing import List

def get_requirements(filepath:str)->List[str]:
    with open(filepath) as file:
        requirement = file.readlines()
        requirement =  [i.replace('\n','') for i in requirement]
        return requirement







setup(
    name = 'Anime',
    version = '0.0.1',
    author = 'vardhman',
    author_email='vardhmanajmera76@gmail.com',
    packages = find_packages(),
    install_requires = get_requirements('requirements.txt')
)















