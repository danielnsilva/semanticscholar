from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='pysemanticscholar',
    version='0.1.6',
    description='A python library aiming to get data via Semantic Scholar API',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='http://danielnsilva.com/semanticscholar',
    author='Daniel Silva',
    author_email='danielnsilva@gmail.com',
    license='MIT',
    packages=['semanticscholar'],
    install_requires=['requests', 'tenacity'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    zip_safe=False
)
