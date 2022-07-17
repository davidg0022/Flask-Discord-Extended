from setuptools import setup, find_packages


classifiers=[
    'Framework :: Flask',
    'Environment :: Web Environment',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    'Programming Language :: Python'
]


requirements = [
    "Flask",
    "oauthlib",
    "requests_oauthlib",
]


setup(
    name='Flask-Discord-Extended',
    version='0.0.1',
    url='https://github.com/davidg0022/Flask-Discord-Extended',
    license='MIT',
    author='Gatea David',
    author_email='davidgatea21@gmail.com',
    description='The Python OAuth2 and Discord Bot Commands for Flask applications.',
    long_description_content_type="text/markdown",
    long_description=open('README.md').read() + '\n\n' + open('CHANGELOG.txt').read(),
    packages=find_packages(),
    platforms='any',
    zip_safe=False,
    include_package_data=True,
    install_requires=requirements,
    classifiers=classifiers
)