# FFForge

**FFForge** is an open-source platform for generating machine-learned force fields for polymers and other materials, leveraging HPC systems like Perlmutter. Users can submit structures (e.g., `.bgf`, `.pdb`, `.mol2`, SMILES) via a web app, specify forcefield purposes (e.g., equilibration, adsorption analysis), and run workflows managed by [FireWorks](https://docs.nersc.gov/jobs/workflow/fireworks/), integrating tools like [ASE](https://wiki.fysik.dtu.dk/ase/), [Pymatgen](https://pymatgen.org/), [PSP AmorphousBuilder](https://github.com/Ramprasad-Group/PSP), [VASP](https://www.vasp.at/), and [PANNA](https://www.researchgate.net/publication/370938051_PANNA_20_Efficient_neural_network_interatomic_potentials_and_new_architectures?_tp=eyJjb250ZXh0Ijp7InBhZ2UiOiJzY2llbnRpZmljQ29udHJpYnV0aW9ucyIsInByZXZpb3VzUGFnZSI6bnVsbH19).

FFForge is an on-going project and is its the early stages of development.

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
### Install Node.js Dependencies

```bash
cd frontend
npm install
```

## Running the Application

Run the `run.py` file when in the `api` directory

```
python3 run.py
```

Run `npm run dev` when in the `frontend` directory

```
npm run dev
```
