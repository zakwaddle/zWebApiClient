import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='zWebApiClient',
    version='v0.0.2',
    author='Zak Waddle',
    author_email='zakwaddle@gmail.com',
    description='Admin level actions for Zoom',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=['zWebApiClient'],
    install_requires=['requests'],
)
