from setuptools import find_packages, setup

def get_requirements() -> list[str]:
    with open("requirements.txt") as f:
        requirements = [req.strip() for req in f]
        if "-e ." in requirements:
            requirements.remove("-e .")
        return requirements

setup(
    name = "car_price_predictor",
    version = "1.0",
    author = "ree",
    author_email = "r33t4m@gmail.com",
    packages = find_packages(),
    requires = get_requirements()
)
