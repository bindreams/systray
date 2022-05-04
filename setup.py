from setuptools import setup

install_requires = [
    "PySide6",
]

setup(
    name="systray",
    version="0.1.0",
    description="Simple interface for system tray icons",
    author="Andrey Zhukov",
    url="https://github.com/andreasxp/systray",
    license="MIT",
    install_requires=install_requires,
    py_modules=["systray"],
)
