from setuptools import setup, find_packages

setup(
    name='kpiServer',
    version='0.1.0',
    description='KPI Server for Ericsson Magic Leap Hackathon 2019 Project',
    python_requires=">=3.5.0",
    packages=find_packages(),
    install_requires=["Flask"],
)

