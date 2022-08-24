import setuptools

setuptools.setup(
    name="lds_data",
    version="0.1a",
    author="Sven Latham",
    author_email="sven.latham@london.gov.uk",
    description="Access the London Datastore API through code",
    url="https://github.com/Greater-London-Authority/lds-data-py",
    packages=setuptools.find_packages(),
    include_package_data=True
)