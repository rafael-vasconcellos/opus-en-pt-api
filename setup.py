from setuptools import setup, find_packages


with open('requirements.txt', 'r', encoding='utf-8') as fh:
    install_requires = fh.read().splitlines()

setup(
    name="opus_api",
    version="1.0",
    packages=["opus_api"],
    install_requires=install_requires,
    entry_points={
        "console_scripts": [
            "opus_api=opus_api.app_uvi:main",  # Substitua pelo ponto de entrada correto
        ],
    },
)

"""

"""