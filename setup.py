from setuptools import setup, find_packages

setup(
    name="opus_api",
    version="1.0",
    packages=["opus_api"],
    #install_requires=[],
    entry_points={
        "console_scripts": [
            "app_uvi=opus_api.app_uvi.__main__:main",  # Substitua pelo ponto de entrada correto
        ],
    },
)

"""

"""