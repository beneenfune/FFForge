# FFForge

TODO: Insert Project Summary here

## Setting Up the Development Environment

### Install Required Software

- [Install](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm) `Node.js` and `npm`
- Install Python 3.10

### Set up a Virtual Environment

#### Windows

```bash
cd api
py -3 -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

#### MacOS/Linux

```bash
cd api
python3 -m venv .venv
. .venv/bin/activate  # or use .venv/Scripts/activate on some setups
pip3 install -r requirements.txt
```

### Install Node.js Dependencies

```bash
cd frontend
npm install
```

## Running the Application

- Run the `run.py` file when in the `api` directory

```
python3 run.py
```

- Run `npm run dev` when in the `frontend` directory

```
npm run dev
```
