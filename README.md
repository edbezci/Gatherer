# Gatherer
Gatherer is a tool designed to collect and store research papers from ArXiv based on user inputs. It allows researchers, students, data scientists, and AI enthusiasts to automate the cumbersome process of searching and saving research data for future reference or further processing.
With Gatherer, you can quickly gather important papers and store them in an easy-to-manage CSV format.
## Version
Gatherer is currently at version 0.1.
## License
This project is licensed under the terms of the MIT License.
## Features

- Gather research data from ArXiv.
- User input based search.
- Save the collected data in CSV format.
- Utilizes `poetry` for package management.

## Dependencies
This project is built using Python and relies on several packages for functionality. These dependencies are managed using `poetry`.
## Installation
To install Gatherer, make sure you have `poetry` installed on your machine. If not, install it first:


    pip install poetry
	Clone the repository: git clone https://github.com/edbezci/error-detection.git
	Navigate into the repository: cd error-detection
	Install dependencies: poetry install
    Activate poetry: poetry shell

## Usage
Place the input data CSV files in the data folder.
Navigate into 'src': cd src
Run the code: python gatherer.py
