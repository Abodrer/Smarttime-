from setuptools import setup, find_packages

setup(
    name='SmartTimeBot',
    version='1.0',
    packages=find_packages(),
    install_requires=[
        'telethon==1.25.0',
        'colorama==0.4.6',
    ],
    entry_points={
        'console_scripts': [
            'start-bot=main:main',  # يتم استدعاء main.py
        ],
    },
)