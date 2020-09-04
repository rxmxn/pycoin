from setuptools import setup, find_packages

setup(
    name='pycoin',
    version='0.1',
    py_modules=['pycoin'],
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'alpha_vantage', # TODO: until the new update of alpha_vantage includes the new function I add, if we install pycoin, it does not allow to run the command to get the ratings and I haven't been able to install the egg
        'aiohttp==3.6.2',
'async-timeout==3.0.1',
'attrs==20.1.0',
'cbpro==1.1.4',
'chardet==3.0.4',
'click==7.1.2',
'idna==2.10',
'multidict==4.7.6',
'numpy==1.19.1',
'pandas==1.1.1',
'pymongo==3.5.1',
'python-dateutil==2.8.1',
'pytz==2020.1',
'requests==2.13.0',
'six==1.10.0',
'sortedcontainers==2.2.2',
'websocket-client==0.40.0',
'yarl==1.5.1',
    ],
    entry_points='''
        [console_scripts]
        pycoin=cli:cli
    ''',
)
