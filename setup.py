from setuptools import setup, find_packages

from pkg_resources import parse_requirements


def get_requires(req_file):
    # type: (str) -> list
    with open(req_file, 'r') as f:
        install_requires = [str(req) for req in parse_requirements(f)]
        return install_requires


setup(
    name='testsolar-testtool-sdk-py2',
    version='0.1.6',
    author='asiazhang',
    author_email='asiazhang2002@gmail.com',
    description='Python2 SDK for TestSolar testtool',
    url='https://github.com/OpenTestSolar/testtool-sdk-python-py2',
    packages=find_packages(),
    python_requires='>=2.7, <3',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
    ],
    license='Apache License 2.0',
    keywords='testsolar',
    install_requires=get_requires('requirements.txt'),
    tests_require=get_requires('requirements-dev.txt'),
    test_suite='tests',
)
