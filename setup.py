import pathlib
from setuptools import setup

# The directory containing this file
SETUP_PATH = pathlib.Path(__file__).parent

# The text of the README file
README = (SETUP_PATH / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="AutonomousMobileRobot",
    version="1.0.0",
    description="This repository is your go-to resource for simulating and experimenting with AMRs, offering a rich set of algorithms and tools. From Simultaneous Localization and Mapping (SLAM) to cutting-edge Machine Learning techniques, Object Detection, and advanced Path Planning.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/Ezte27/Autonomous_Mobile_Robot",
    author="Esteban Calderon",
    author_email="estedcg27@gmail.com",
    license="MIT",
    requires="python >= 3.9",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
    ],
    packages=["AutonomousMobileRobot"],
    include_package_data=True,
    install_requires=[
        "numpy", 
        "matplotlib",
        ],
    entry_points={
        "console_scripts": [
            "AMR=AutonomousMobileRobot.__main__:main",
        ]
    },
)