import pathlib
from setuptools import setup, find_packages

# The directory containing this file
SETUP_PATH = pathlib.Path(__file__).parent

# The text of the README file
README = (SETUP_PATH / "README.md").read_text()

NAME                = "AutonomousMobileRobot"
VERSION             = "1.0.0"
DESCRIPTION         = "This repository is your go-to resource for simulating and experimenting with AMRs, offering a rich set of algorithms and tools. From Simultaneous Localization and Mapping (SLAM) to cutting-edge Machine Learning techniques, Object Detection, and advanced Path Planning."
LONG_DESCRIPTION    = README
AUTHOR              = "Esteban Calderon"
AUTHOR_EMAIL        = "estedcg27@gmail.com"
URL                 = "https://github.com/Ezte27/Autonomous_Mobile_Robot"
LICENSE             = "MIT"
KEYWORDS            = ["AMR", "SLAM", "Path Planning", "Machine Learning", "Object Detection", "Autonomous Mobile Robot"]
PLATFORMS           = ["Windows", "Linux", "MacOS"]
INSTALL_REQUIRES    = ["numpy", "matplotlib", "pygame", "rtree"]

# This call to setup() does all the work
setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    maintainer=AUTHOR,
    maintainer_email=AUTHOR_EMAIL,
    url=URL,
    packages=find_packages(),
    py_modules= [],
    scripts=[],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
    ],
    license=LICENSE,
    keywords=KEYWORDS,
    platforms=PLATFORMS,
    python_requires=">=3.10",
    include_package_data=True,
    install_requires=INSTALL_REQUIRES,
    # entry_points={
    #     "console_scripts": [
    #         "AMR=AutonomousMobileRobot.__main__:main",
    #     ]
    # },
)