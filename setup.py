from setuptools import setup

version = '0.1.1'

setup(
    name='Taskban',
    version=version,
    description='Implement a Kanban workflow with Taskwarrior',
    author='Lyz',
    author_email='lyz@riseup.net',
    packages=['taskban', ],
    license='GPLv2',
    long_description=open('README.md').read(),
    entry_points={
      'console_scripts': ['taskban = taskban:main']
    }
)
