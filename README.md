# tamuGPT


### Prerequisites
* Install Python (>3.9)


### Project Installation
1. Clone the repository - `git clone <remote-url>`
1. Go to the project directory - `cd <cloned-repo>`
1. Set up the environment:
    * Create a virtual environment - `python3 -m venv venv`
    * Activate the virtual environment:
      * Linux: `source venv/bin/activate`
      * Windows: `venv\Scripts\activate`
1. Install the dependencies - `pip3 install -r requirements.txt`
1. Install pre-commit - `pre-commit install`
1. Copy contents of `.env.example` to a new file `.env` - `cp .env.example .env`
    * Fill in the below environment variables
      * `OPENAI_API_KEY`: Get OpenAI API key [here](https://platform.openai.com/signup/)
      * `GOOGLE_CSE_ID`: Get Google Custom Search JSON API [here](https://developers.google.com/custom-search/v1/overview)
      * `GOOGLE_CSE_API_KEY`: Get Google Search Engine ID [here](https://support.google.com/programmable-search/answer/12499034?hl=en)
1. Configure `config.py` file if needed


### Code formatting
Pre-commit hooks automatically format the code using autopep8 when you do `git commit`.
