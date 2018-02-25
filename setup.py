from setuptools import setup, find_packages

setup(name='org_to_anki',
	version='0.1',
	description='Org to Anki notes parser',
	author='Conor OKelly',
	author_email='okellyconor@gmail.com',
	url='https://github.com/c-okelly/org_to_anki',
	install_requires=['requests','nose'],
	packages=['org_to_anki'],
	entry_points={
		'console_scripts': [
			'org_to_anki = org_to_anki.main:main'
		]
	},
	scripts=['bin/foo']
	)
