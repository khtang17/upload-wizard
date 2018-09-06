from setuptools import setup, find_packages

# To use a consistent encoding
from codecs import open
from os import path

# here = path.abspath(path.dirname(__file__))

# Get the long description from the relevant file
# with open(path.join(here, 'DESCRIPTION.rst'), encoding='utf-8') as f:
#     long_description = f.read()

setup(
    name='VENDOR-UPLOAD',

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version='0.20180808.2',

    description='Upload Wizard v1.0',
    long_description='',

    zip_safe=False,

    # The project's main homepage.
    url='https://github.com/chinzod/vendor-upload',

    # Author details
    author='Chinzorig Dandarchuluun',
    author_email='chinzo.dandar@gmail.com',

    # Choose your license
    license='UC Regents',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        # Pick your license as you wish (should match "license" above)
        'License :: Chinzorig Dandarchuluun',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3.5',
    ],

    # What does your project relate to?
    keywords='sample setuptools development',

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=find_packages(exclude=['contrib', 'docs', 'tests*', 'venv']),

    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=[
        'alembic==0.9.9',
        'amqp==2.3.2',
        'asn1crypto==0.24.0',
        'awsebcli==3.14.1',
        'Babel==2.6.0',
        'bcrypt==3.1.4',
        'billiard==3.5.0.3',
        'blessed==1.15.0',
        'blinker==1.4',
        'boto3==1.7.44',
        'botocore==1.10.44',
        'cached-property==1.4.3',
        'celery==4.2.0',
        'cement==2.8.2',
        'certifi==2018.4.16',
        'cffi==1.11.5',
        'chardet==3.0.4',
        'click==6.7',
        'colorama==0.3.9',
        'cryptography==2.2.2',
        'docker==3.4.0',
        'docker-compose==1.21.2',
        'docker-pycreds==0.3.0',
        'dockerpty==0.4.1',
        'docopt==0.6.2',
        'docutils==0.14',
        'dominate==2.3.1',
        'et-xmlfile==1.0.1',
        'Flask==1.0.2',
        'Flask-Admin==1.5.1',
        'Flask-BabelEx==0.9.3',
        'Flask-Bootstrap==3.3.7.1',
        'Flask-Excel==0.0.7',
        'Flask-HTTPAuth==3.2.4',
        'Flask-Login==0.4.1',
        'Flask-Mail==0.9.1',
        'Flask-Menu==0.7.0',
        'Flask-Migrate==2.2.1',
        'Flask-Moment==0.6.0',
        'Flask-Principal==0.4.0',
        'Flask-Security==3.0.0',
        'Flask-SQLAlchemy==2.3.2',
        'Flask-User==0.6.21',
        'Flask-WTF==0.14.2',
        'hurry==1.0',
        'hurry.filesize==0.9',
        'idna==2.6',
        'itsdangerous==0.24',
        'jdcal==1.4',
        'Jinja2==2.10',
        'jmespath==0.9.3',
        'jsonschema==2.6.0',
        'kombu==4.2.1',
        'lml==0.0.1',
        'Mako==1.0.7',
        'MarkupSafe==1.0',
        'openpyxl==2.5.4',
        'passlib==1.7.1',
        'pathspec==0.5.5',
        'psycopg2==2.7.5',
        'py==1.4.34',
        'pycparser==2.18',
        'pycryptodome==3.6.3',
        'pyexcel==0.5.8',
        'pyexcel-io==0.5.7',
        'pyexcel-webio==0.1.4',
        'pyexcel-xls==0.5.7',
        'pyexcel-xlsx==0.5.6',
        'python-dateutil==2.7.3',
        'python-dotenv==0.8.2',
        'python-editor==1.0.3',
        'pytz==2018.4',
        'PyYAML==3.12',
        'requests==2.18.4',
        's3transfer==0.1.13',
        'semantic-version==2.5.0',
        'six==1.11.0',
        'speaklater==1.3',
        'SQLAlchemy==1.2.8',
        'tabulate==0.7.5',
        'termcolor==1.1.0',
        'texttable==0.9.1',
        'urllib3==1.22',
        'vine==1.1.4',
        'visitor==0.1.3',
        'wcwidth==0.1.7',
        'websocket-client==0.48.0',
        'Werkzeug==0.14.1',
        'WTForms==2.2.1',
        'xlrd==1.1.0',
        'xlwt==1.3.0',
    ],

    scripts=(
        'application.py',
        'config.py',
        'setup.py',
        'requirements.txt',
    ),
    # List additional groups of dependencies here (e.g. development
    # dependencies). You can install these using the following syntax,
    # for example:
    # $ pip install -e .[dev,test]
    # extras_require={
    #     'dev': ['check-manifest'],
    #     'test': ['coverage'],
    # },

    # If there are data files included in your packages that need to be
    # installed, specify them here.  If using Python 2.6 or less, then these
    # have to be included in MANIFEST.in as well.
    include_package_data=True,
    package_data={
        'static': 'app/static/*',
        'templates': 'app/template/*',
    },

    # Although 'package_data' is the preferred approach, in some case you may
    # need to place data files outside of your packages. See:
    # http://docs.python.org/3.4/distutils/setupscript.html#installing-additional-files # noqa
    # In this case, 'data_file' will be installed into '<sys.prefix>/my_data'
    # data_files=[('my_data', ['data/data_file.txt'])],

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    # entry_points={
    #     'console_scripts': [
    #         'sample=application.py:main',
    #     ],
    # },
)