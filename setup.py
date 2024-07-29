from setuptools import setup, find_packages

setup(
    name='Query Buster',
    version='0.1.0',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    include_package_data=True,
    install_requires=[
        'flask',
        'requests',
        'psycopg2-binary',
        'redis',
    ],
    entry_points={
        'console_scripts': [
            'project_name=main:main',
        ],
    },
    author='Brian Ruff',
    author_email='briananthonyruff@gmail.com',
    description='PoC of using Redis to cache SQL query results to speed up REST API calls.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/BrianARuff/poc_redis_postgres_python-flask_api.git',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
