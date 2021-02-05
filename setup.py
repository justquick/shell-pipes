import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='shell-pipes',
    version='0.1.0',
    author='Justin Quick',
    author_email='justquick@gmail.com',
    description='Extending Python syntax to implement shell commands as pipes using subprocess',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/justquick/pipes',
    py_modules=['shpipes'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 2',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: System :: Shells',
        'Programming Language :: Unix Shell',
    ],
    python_requires='>=2.7',
)
