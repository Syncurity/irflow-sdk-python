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
	long_description=open('DESCRIPTION').read(),
	license='Commercial',
	copyright='Copyright {} Syncurity'.format(datetime.datetime.now().year),
	url='https://www.syncurity.net',
	packages=['irflow_client'],
	install_requires=base_requirements,

)
