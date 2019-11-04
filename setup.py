"""Installer for the getoffmylawn package."""

from setuptools import find_packages
from setuptools import setup

setup(
    name="getoffmylawn",
    version="0.1",
    description="Pyramid URL redirector",
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        "License :: MIT",
    ],
    author="David Glick",
    author_email="david@glicksoftware.com",
    url="http://github.com/davisagli/getoffmylawn",
    keywords="pyramid openapi realworld",
    license="MIT",
    packages=find_packages("src", exclude=["ez_setup"]),
    package_dir={"": "src"},
    include_package_data=True,
    zip_safe=False,
    entry_points="""\
    [paste.app_factory]
    main = getoffmylawn:main
    """,
    test_suite="getoffmylawn",
)
