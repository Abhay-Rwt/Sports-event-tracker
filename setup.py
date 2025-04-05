from setuptools import setup, find_packages

setup(
    name="sports-event-tracker-chatbot",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "Flask>=2.0.1",
        "requests>=2.26.0",
        "python-dotenv>=0.19.0",
        "Flask-SocketIO>=5.1.1",
        "gunicorn>=20.1.0",
        "openai>=0.27.0",
        "beautifulsoup4>=4.10.0",
    ],
) 