from distutils.core import setup

setup(
    name="oneconf",
    version="0.1.0",
    author="Tomas Korbar",
    author_email="tomas.korb@seznam.cz",
    license="GPL3",
    description="Configuration library",
    packages=["oneconf.configuration", "oneconf.exceptions"],
)
