from setuptools import setup, find_packages

setup(
    name="aero-cli",
    version="1.2.0",
    description="Aero Linux Core Control Suite for Power, Memory, and Local AI Runtimes",
    author="Aero Linux Team",
    packages=find_packages(),
    scripts=["bin/aero"],
    install_requires=[],
    entry_points={
        "console_scripts": [
            "aero=aero.__main__:main",
        ],
    },
)
