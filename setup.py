from setuptools import setup, find_packages

setup(name='org_to_anki',
      version='0.1',
      description='Org to Anki notes parser',
      author='Conor OKelly',
      author_email='okellyconor@gmail.com',
      url='https://github.com/c-okelly/org_to_anki',
      python_requires='>3.4',
      install_requires=['requests', 'bs4'],
      tests_require=['responses', 'nose', 'coverage'],
      test_suite="nose.collector",
      packages=find_packages(),
      include_package_data=True,
      entry_points={
          'console_scripts': [
              'org_to_anki = org_to_anki.main:parseAndUploadOrgFile',
              'ankiq = org_to_anki.quickNote:quickNote'
          ]
      }
      )