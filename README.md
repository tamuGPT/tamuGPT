# tamuGPT


### Prerequisites
* Install Python (>3.9)


### Project Installation
1. Clone the repository - `git clone <remote-url>`
1. Go to the project directory - `cd <cloned-repo>`
1. Set up the environment:
    * Create a virtual environment - `python3 -m venv venv`
    * Activate the virtual environment - `source venv/bin/activate` (Linux) or  `venv\Scripts\activate` (Windows)
1. Install the dependencies - `pip3 install -r requirements.txt`
1. Install pre-commit - `pre-commit install`
1. Copy contents of `.env.example` to a new file `.env` - `cp .env.example .env`
    * Fill in the required environment variables
1. Configure the `config.py` file if needed


### Code formatting
Pre-commit hooks automatically format the code using autopep8 when you do `git commit`.
