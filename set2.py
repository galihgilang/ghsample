from setuptools import setup, find_packages

setup(
    name='kpiGenerator',
    version='0.1.0',
    description='KPI Generator for Ericsson Magic Leap Hackathon 2019 Project',
    python_requires=">=3.5.0",
    packages=find_packages(),
    install_requires=["psutil", "requests"],
    entry_points = {
        "console_scripts": [
            "kpiGenerator = kpiGenerator:main"
        ]
    }
)


master