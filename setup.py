from setuptools import setup, find_packages

setup(
    name='testsolar-testtool-sdk-py2',
    version='0.3.0',
    author='asiazhang',
    author_email='asiazhang2002@gmail.com',
    description='Python2 SDK for TestSolar testtool',
    url='https://github.com/OpenTestSolar/testtool-sdk-python-py2',
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    python_requires='>=2.7',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
    ],
    license='Apache License 2.0',
    keywords='testsolar',
    test_suite='tests',
)
