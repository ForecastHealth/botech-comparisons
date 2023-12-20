from setuptools import setup, find_packages

setup(
    name='botech_comparisons',
    version='0.1.0',
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    license='Apache 2.0',
    description='Compare results',
    long_description=open('README.md').read(),
    url='https://github.com/ForecastHealth/botech_comparisons',
    author='Forecast Health',
    author_email='rory@forecasthealth.org'
)
