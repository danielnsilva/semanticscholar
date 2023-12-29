from setuptools import setup

with open("README.md", "r", encoding='utf8') as fh:
    long_description = fh.read()

setup(
    name='semanticscholar',
    version='0.7.0',
    description='Unofficial Python client library for Semantic Scholar APIs.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='http://danielnsilva.com/semanticscholar',
    author='Daniel Silva',
    author_email='danielnsilva@gmail.com',
    license='MIT',
    packages=['semanticscholar'],
    python_requires='>=3.8',
    install_requires=['tenacity', 'httpx', 'nest_asyncio'],
    test_suite='tests',
    tests_require=['vcrpy'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    zip_safe=False
)
