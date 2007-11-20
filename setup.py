from setuptools import setup, find_packages

version = '0.1'

setup(name='collective.passwordhistory',
      version=version,
      description="A package to prevent users of a Plone site from re-using previously used passwords",
      long_description="""\
""",
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Framework :: Zope2",
        "Framework :: Zope3",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='plone',
      author='Emyr Thomas',
      author_email='emyr.thomas@gmail.com',
      url='http://svn.plone.org/svn/collective/collective.passwordhistory',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['collective'],
      include_package_data=True,
      zip_safe=True,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
