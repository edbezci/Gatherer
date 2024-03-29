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

This project depends on GPT-4. To replicate the results, it is required to have openai_api_key in .env file in the root directory.

## Installation
To install Gatherer, make sure you have `poetry` installed on your machine. If not, install it first:


    pip install poetry
	Clone the repository: git clone
	Navigate into the repository: cd gatherer
	Install dependencies: poetry install
    Activate poetry: poetry shell
	Navigate into src: cd src
	Execute the command: cd python gatherer.py




## Usage

![Searching Arxiv](media/step_1.png)

![Critical Evaluation](media/step_2.png)
