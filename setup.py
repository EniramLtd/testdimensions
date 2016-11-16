from setuptools import setup

try:
    long_description = open('README.rst', 'U').read()
except IOError:
    long_description = 'See https://github.com/akaihola/testdimensions'

setup(name='testdimensions',
      version='0.0.1',
      url='https://github.com/akaihola/testdimensions',
      license='FreeBSD',
      author='Antti Kaihola',
      author_email='antti dot kaihola at eniram and finally fi for finland',
      description='Multi-dimensional parameterized tests for Pytest and Nose',
      classifiers=[
            'Programming Language :: Python',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3.3',
            'Programming Language :: Python :: 3.4',
            'Programming Language :: Python :: 3.5',
            'License :: OSI Approved :: BSD License',
      ],
      py_modules=['testdimensions'],
      tests_require=['pytest-mock>=1.2', 'mock>=2.0.0'],
      long_description=long_description)
