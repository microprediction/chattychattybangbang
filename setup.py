import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

setup(
    name="chattychattybangbang",
    version="0.0.2",
    description="chat utilities",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/chattychattybangbang/chattychattybangbang",
    author="chattychattybangbang",
    author_email="pcotton@intechinvestments.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    packages=["chattychattybangbang"],
    test_suite='pytest',
    tests_require=['pytest'],
    include_package_data=True,
    install_requires=["numpy","pandas","getjson","hypothesis","openai"],
    entry_points={
        "console_scripts": [
            "chattychattybangbang=chattychattybangbang.__main__:main",
        ]
    },
)
