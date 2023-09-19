from setuptools import find_packages, setup
from typing import List

HYPHEN_E_DOT = '-e .'

def get_requirements()->List[str]:

    ''' Get the requirements.txt file and install the dependencies while setup

        Returns
        -------
        requirements: List of string objects of modules to be installed.

    '''

    with open('requirements.txt') as f:
        requirements = [line for line in f]
        requirements = [req.replace("\n", "") for req in requirements]

        if HYPHEN_E_DOT in requirements:
            requirements.remove(HYPHEN_E_DOT)

    return requirements


setup(
    name="WebScraper_Integration_with_Chatgpt_EmailSender",
    version='0.0.1',
    author="Mohit Nilkute",
    author_email="mohitnilkute012@gmail.com",
    install_requires=get_requirements(),
    packages=find_packages()
)