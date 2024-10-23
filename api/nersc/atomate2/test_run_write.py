from jobflow import Flow, Response, job, Maker
from pymatgen.core import Structure, Lattice
from atomate2.vasp.jobs.core import StaticMaker
from pymatgen.io.cif import CifParser
from jinja2 import Template
import os
import pytest
from pathlib import Path
from collections import defaultdict
from dataclasses import field

@job # TODO: make run_scf_job // run_adslabs_job
def run_scf_job(
    scf_structures: list[Structure],
    is_molecular: bool | str,
    static_maker: Maker | None = field(default_factory=StaticMaker),
) -> Response:
    """Workflow of running the scf calculations.

    Parameters
    ----------
    scf_structures: list[Structure]
        The list of rattled strctures to run scf calculations on.
    static_maker: StaticMaker
        The static maker for the rattled structures.
    is_molecular: bool or str
        True if structure is a molecular structure, false if it is not (e.g. crystal)
    Returns
    -------
    Flow
        The flow of the scf calculations.
    """
    scf_jobs = []
    scf_outputs = defaultdict(list) # output of the flow

    for i, scf_structure in enumerate(scf_structures):
        scf_job = static_maker.make(structure=scf_structure, prev_dir=None)

        scf_jobs.append(scf_job)
        scf_outputs["generated_hash"].append(scf_job.uuid) # good
        scf_outputs["energy_in_eV"].append(scf_job.output.output.energy) # good
        scf_outputs["sites"].append(scf_job.output.structure.sites) # process
        scf_outputs["forces"].append(scf_job.output.output.forces) # process
        scf_outputs["dirs"].append(scf_job.output.dir_name) # can use, currently not in use
        scf_outputs["lattice_matrix"].append(scf_job.output.output.structure.lattice.matrix) # process


    scf_flow = Flow(scf_jobs, scf_outputs)
    return Response(replace=scf_flow)


@job # TODO: make write_scf_examples // adsorption_calculations
def write_scf_examples(
    scf_data: dict[str, list],
    is_molecular: bool | str,
    output_dir: str | Path | None = None,
):
    """Write the example files from the scf calculations for PANNA usage.

    Parameters
    ----------
    scf_data : dict[str, list]
        Dictionary containing data of the scf calculations.
    output_dir : str or Path or None
        A directory to output the example files for PANNA to use
    is_molecular: bool or str
        True if structure is a molecular structure, false if it is not (e.g. crystal)
    Returns
    -------
    Nothing
    """

    # Debug: print the output directory and the data being processed
    print(f"Output directory: {output_dir}")
    print(f"Data received: {scf_data}")

    lattice_vectors = {}
    site_results = []

    # Get output data
    generated_hash = scf_data["generated_hash"]
    is_molecular = scf_data["is_molecular"]
    energy_in_eV = scf_data["energy_in_eV"]
    sites = scf_data["sites"]
    forces = scf_data["forces"]
    output_dir = '../output_files' # TODO: default output_dir is set for now to ./output_files -> can use the "dirs" key

    print("Type of generated_hash (ideal is string, might be list): ", type(generated_hash))
    print("The generated_hash value: ", generated_hash)

    # Process each site
    for index, site in enumerate(sites):
        atom = site['label']
        xcoord, ycoord, zcoord = map(float, site['xyz'])

        # Get the corresponding force for this atom and cast to float
        xforce, yforce, zforce = map(float, forces[index])

        # Append a dictionary with all relevant information
        site_results.append({
            "index": index,
            "atom": atom,
            "xcoord": xcoord,
            "ycoord": ycoord,
            "zcoord": zcoord,
            "xforce": xforce,
            "yforce": yforce,
            "zforce": zforce,
        })

    # If the structure is not molecular, get the lattice vector data
    if is_molecular == 'false' or is_molecular is False:
        lattice_matrix = scf_data["lattice_matrix"]

        # Extract and cast the elements from the lattice matrix
        x1, x2, x3 = map(float, lattice_matrix[0])
        y1, y2, y3 = map(float, lattice_matrix[1])
        z1, z2, z3 = map(float, lattice_matrix[2])

        # Store lattice vectors as a single dictionary
        lattice_vectors = {
            "x1": x1,
            "x2": x2,
            "x3": x3,
            "y1": y1,
            "y2": y2,
            "y3": y3,
            "z1": z1,
            "z2": z2,
            "z3": z3
        }

    print(f"energy_in_eV is {energy_in_eV}")
    print(f"generated_hash is {generated_hash}")
    print("sites:")
    for site in site_results:
        print(json.dumps(site,indent=4))
    print(f"lattice_vectors:")
    print(lattice_vectors)

    template_str = """{
    "key": "{{ generated_hash }}",{% if not is_molecular %}
    "lattice_vectors": [
        [
            {{ lattice_vectors['x1'] }},
            {{ lattice_vectors['x2'] }},
            {{ lattice_vectors['x3'] }}
        ],
        [
            {{ lattice_vectors['y1'] }},
            {{ lattice_vectors['y2'] }},
            {{ lattice_vectors['y3'] }}
        ],
        [
            {{ lattice_vectors['z1'] }},
            {{ lattice_vectors['z2'] }},
            {{ lattice_vectors['z3'] }}
        ]
    ],{% endif %}
    "atomic_position_unit": "cartesian",
    "unit_of_length": "angstrom",
    "energy": [
        {{ energy_in_eV }},
        "eV"
    ],
    "atoms": [{% for site in sites %}
        [
            {{ site['index'] }},
            "{{ site['atom'] }}",
            [
                {{ site['xcoord'] }},
                {{ site['ycoord'] }},
                {{ site['zcoord'] }}
            ],
            [
                {{ site['xforce'] }},
                {{ site['yforce'] }},
                {{ site['zforce'] }}
            ]
        ]{% if not loop.last %},{% endif %}{% endfor %}
    ]
}"""

    # Create the Jinja2 template object
    template = Template(template_str)

    # Render the template with provided arguments
    rendered_output = template.render(
        generated_hash=generated_hash,
        is_molecular=is_molecular == 'true',  # Convert to boolean
        lattice_vectors=lattice_vectors,
        energy_in_eV=energy_in_eV,
        sites=sites
    )

    # Define the output file path
    output_file_path = os.path.join(output_dir, f"{generated_hash}.example")

    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Write the rendered output to the file
    with open(output_file_path, 'w') as f:
        f.write(rendered_output)

    print(f"Template written to {output_file_path}")

@pytest.fixture
def mock_scf_data():
    """Fixture to provide mock SCF data."""
    return {
        "generated_hash": "mock_hash123",
        "is_molecular": False,
        "energy_in_eV": -10.5,
        "sites": [
            {
                "index": 1,
                "label": "H",
                "xyz": [0.0, 0.0, 0.0],
                "forces": [0.1, 0.2, 0.3],
            },
            {
                "index": 2,
                "label": "O",
                "xyz": [1.0, 1.0, 1.0],
                "forces": [-0.1, -0.2, -0.3],
            },
        ],
        "forces": [
            [0.1, 0.2, 0.3],
            [-0.1, -0.2, -0.3],
        ],
        "lattice_matrix": [
            [1.0, 0.0, 0.0],
            [0.0, 1.0, 0.0],
            [0.0, 0.0, 1.0],
        ],
    }

def test_write_scf_examples(mock_scf_data, tmpdir):
    """Test the write_scf_examples function."""
    output_dir = tmpdir.mkdir("output")  # Use pytest's tmpdir fixture to create a temporary directory

    # Call the function
    write_scf_examples(mock_scf_data, output_dir=str(output_dir), is_molecular=False)

    # Check if the output file exists
    output_file = Path(output_dir) / "mock_hash123.example"
    assert output_file.exists(), "The output file was not created."

    # Optionally check the contents of the file
    with open(output_file, 'r') as f:
        content = f.read()
        assert "energy" in content, "The output file does not contain expected data."

@pytest.fixture
def mock_scf_structures():
    """Fixture to provide mock SCF structures."""
    coords = [[0, 0, 0], [0.75,0.5,0.75]]
    lattice = Lattice.from_parameters(a=3.84, b=3.84, c=3.84, alpha=120,beta=90, gamma=60)
    struct = Structure(lattice, ["Si", "Si"], coords)
    return [struct]

@pytest.fixture
def mock_static_maker():
    """Fixture for StaticMaker."""
    class MockStaticMaker:
        def make(self, structure, prev_dir=None):
            return MockJob()

    return MockStaticMaker()

class MockJob:
    """Mock job to simulate SCF job behavior."""
    def __init__(self):
        self.uuid = "mock_uuid"
        self.output = MockOutput()

class MockOutput:
    """Mock output to simulate job outputs."""
    def __init__(self):
        self.energy = -10.5
        self.structure = MockStructure()
        self.forces = [[0.1, 0.2, 0.3], [-0.1, -0.2, -0.3]]

class MockStructure:
    """Mock structure output."""
    def __init__(self):
        self.sites = ["site1", "site2"]
        self.lattice = MockLattice()

class MockLattice:
    """Mock lattice structure."""
    def __init__(self):
        self.matrix = [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]

def test_run_scf_job(mock_scf_structures):
    """Test the run_scf_job function."""
    result = run_scf_job(scf_structures=mock_scf_structures, is_molecular=False)

    # Ensure the returned object is a Response
    assert isinstance(result.replace, Flow), "run_scf_job did not return a Flow as expected."
    
    # Check that the job flow was constructed
    assert len(result.replace.jobs) == len(mock_scf_structures), "Not all jobs were added to the flow."

    # Check the outputs in the result
    output = result.replace.output
    assert "energy_in_eV" in output, "The output does not contain expected energy data."

if __name__ == "__main__":
    pytest.main()