# DMAx Website

**DMAx Website** TODO: summary

DMAx website is an on-going project and is its the early stages of development.

## Setting Up the Development Environment

### Install Required Software

- [Install](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm) `Node.js` and `npm`
- [Install](https://materialsproject.github.io/fireworks/installation.html) `Fireworks`
- Install Python 3.10

### Set up a Virtual Environment

#### Windows

```bash
cd api
py -3 -m venv .venv
. .venv\Scripts\activate
pip install -r requirements.txt
```

#### MacOS/Linux

```bash
cd api
python3 -m venv .venv
. .venv/bin/activate  # or use .venv/Scripts/activate on some setups
pip3 install -r requirements.txt
```

=======
### Install Node.js Dependencies

```bash
cd frontend
npm install
```

## Running the Application

### Note: Security Clearance Level

- .env in `api` directory needs to have Red clearance with the following example values:

```
SFAPI_CLIENT_ID='randmstrgz'
SFAPI_SECRET='{"kty": "RSA", "n": ...}'
SFAPI_PRIVATE_KEY="PEM Long string"
```

- Run the `run.py` file when in the `api` directory

```
python3 run.py
# or nodemon run.py
```

Run `npm run dev` when in the `frontend` directory

```
npm run dev
```
