from setuptools import find_namespace_packages, setup

setup(
    name="TRIO",
    version="1.0.1",
    description="it does many things, see README",
    url="https://github.com/anilev6/Trio",
    author="ByteCrafters",
    license="kek",
    packages=find_namespace_packages(),
    install_requires=["markdown"],
    include_package_data=True,
    entry_points={"console_scripts": ["trio = trio:main_menu"]},
)
