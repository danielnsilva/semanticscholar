from setuptools import setup

setup(
    name='semanticscholar',
    version='0.1.0',
    description='A python library that aims to retrieve data from Semantic Scholar API',
    url='http://danielnsilva.com/semanticscholar',
    author='Daniel Silva',
    author_email='danielnsilva@gmail.com',
    license='MIT',
    packages=['semanticscholar'],
    install_requires=['requests','retrying'],
    test_suite='nose.collector',
    tests_require=['nose'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    zip_safe=False
)