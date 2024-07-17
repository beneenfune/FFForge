To start

### Install and Activate Venv

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
. .venv/bin/activate
pip3 install -r requirements.txt
```

## Running the App
- Run the `api.py` file when in the `api` directory: `python3 api.py`
- Run `npm run dev` when in the `frontend` directory