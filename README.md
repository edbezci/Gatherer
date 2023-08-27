# Gatherer
Gatherer is a tool designed to collect and critically asses the research papers from ArXiv based on user inputs. It allows researchers, students, data scientists, and AI enthusiasts to automate the cumbersome process of searching and saving research data for future reference or further processing.
Moreover, the tool provides succint but valuable reports from academic and business perspective regarding the feasibility of the proposed research.


## Version
Gatherer is currently at version 0.2.
## License
This project is licensed under the terms of the MIT License.
## Features

- Gather research data from ArXiv.
- User input based search.
- Save the collected data in CSV format.
- Utilizes `poetry` for package management.
- Uses Generative AI to critically asses the searched research paper both academic and business perspective.

## Dependencies
This project is built using Python and relies on several packages for functionality. These dependencies are managed using `poetry`.
## Installation
To install Gatherer, make sure you have `poetry` installed on your machine. If not, install it first:


    pip install poetry
	Clone the repository: git clone
	Navigate into the repository: cd gatherer
	Install dependencies: poetry install
    Activate poetry: poetry shell

## Usage
The current version uses GPT-4. Please create a .env file in the root directory with your API-creds.
Navigate into 'src': cd src
Run the code: python gatherer.py
