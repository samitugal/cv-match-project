from setuptools import setup, find_packages

setup(
    name="cvinsight",
    version="0.1.0",
    description="AI-powered CV processing, analysis, and anonymization tool for corporate HR departments",
    packages=find_packages(),
    install_requires=[
        "black>=25.1.0",
        "isort>=6.0.1",
        "langdetect>=1.0.9",
        "numpy<2.0.0",
        "protobuf>=3.20.0",
        "pypdf2>=3.0.1",
        "pytest>=8.3.5",
        "python-docx>=1.1.0",
        "python-dotenv>=1.1.0",
        "transformers>=4.52.4",
        "torch>=2.0.0"
    ],
)
