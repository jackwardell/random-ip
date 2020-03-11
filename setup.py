from setuptools import find_packages
from setuptools import setup

# REQUIREMENTS = Path(os.path.dirname(os.path.realpath(__file__))) / "requirements.txt"
#
# with open(REQUIREMENTS, 'r') as f:
#     requirements = f.readlines()

setup(
    name="iprandom",
    version="0.1.0",
    author="Jack Wardell",
    author_email="jackwardell@me.com",
    description="library for generating random ip addresses",
    packages=find_packages(),
    python_requires=">=3.6",
    # install_requires=requirements,
)
