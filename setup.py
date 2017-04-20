from setuptools import setup
import datetime

with open('requirements.txt') as f:
    base_requirements = f.read().splitlines()

setup(
    name='irflow_client',
    version=open('VERSION').read(),
    author='JP Bourget, Michael Deale',
    author_email='jp@syncurity.net',
    maintainer='Syncurity Corp.',
    maintainer_email='support@syncurity.net',
    description=open('SUMMARY').read(),
    keywords='Syncurity syncurity IR-Flow ir-flow irflow security incident response',
    long_description=open('DESCRIPTION').read(),
    license='Commercial',
    copyright='Copyright {} Syncurity'.format(datetime.datetime.now().year),
    url='https://github.com/Syncurity/irflow-sdk-python',
    packages=['irflow_client'],
    install_requires=base_requirements,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Security',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ]
)
