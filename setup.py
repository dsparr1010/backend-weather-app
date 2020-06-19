from setuptools import setup



setup(
    name = 'hello',
    version = '1.0',
    py_modules = ['hello'],
    install_requires = [
        'Click',
        'requests',
        'python-dotenv'
    ],
    entry_points = '''
        [console_scripts]
        hello = hello:cli
    ''',
)


