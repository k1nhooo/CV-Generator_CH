from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="swiss-cv-generator",
    version="1.0.0",
    author="Swiss CV Generator Team",
    description="Synthetische Lebenslauf-Generierung für den Schweizer Arbeitsmarkt",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "pandas>=1.5.0",
        "numpy>=1.20.0",
        "python-dateutil>=2.8.0",
        "pydantic>=1.10.0",
        "click>=8.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=22.0.0",
            "flake8>=4.0.0",
        ]
    },
    entry_points={
        "console_scripts": [
            "swiss-cv-gen=swiss_cv_generator.cli:main",
        ],
    },
)
