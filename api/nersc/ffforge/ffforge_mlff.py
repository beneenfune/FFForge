from jobflow import Flow, Response, job, Maker, Job
from jobflow.utils.graph import to_mermaid
from jobflow.managers.local import run_locally
from jobflow.managers.fireworks import flow_to_workflow

from pymatgen.core import Structure, Lattice
from atomate2.vasp.jobs.core import StaticMaker
from pymatgen.io.cif import CifParser
from jinja2 import Template
import os
import pytest
from pathlib import Path
from collections import defaultdict
from dataclasses import field
from ase import Atoms
import json

from jobflow.managers.fireworks import flow_to_workflow
from fireworks import LaunchPad, FWorker
from fireworks.queue.queue_launcher import launch_rocket_to_queue
from fireworks.core.rocket_launcher import launch_rocket
from fireworks.utilities.fw_serializers import load_object_from_file

# different generators -> error handlers try execpt raiseerror
@job # TODO: make generate_rattled // generate_slab
def generate_rattled(
    structure_to_rattle: Structure,
    purpose: str = "Simple Equilibration",
    num_structures: int = 20,
) -> list[Structure]:
    """Generate the rattled structures for the training set.

    Parameters
    ----------
    structure_to_rattle: Structure
        The structure to rattled.
    purpose: str
        The purpose of generating the MLFF (TODO: list the allowed options). Default is Simple Equilibration
    num: int
        The number of rattled structures to generate.

    Returns
    -------
    rattled_strucutures: list[Structure]
        Rattled structures.
    """
    
    rattled_structures = []

    if purpose == "Simple Equilibration": 
        try:
            structure = structure_to_rattle
            # # Generate rattled structures
            # for i in range(num_structures):
            #     # Determine standard deviation based on index
            #     std_dev = 0.005 if i < num_structures // 2 else 0.01
            #     # Create ASE Atoms object from pymatgen structure
            #     element_symbols = [site.specie.symbol for site in structure]
            #     atom_positions = structure.cart_coords
            #     atoms = Atoms(symbols=element_symbols, positions=atom_positions)
            #     # Apply random displacements using ASE's built-in 'rattle' function
            #     atoms.rattle(stdev=std_dev)
            #     # Convert back to pymatgen structure
            #     rattled_structure = Structure(
            #         lattice=structure.lattice,
            #         species=element_symbols,
            #         coords=atoms.get_positions(),
            #         site_properties=structure.site_properties,
            #     )
            #     rattled_structures.append(rattled_structure)
            # TODO: remove and uncomment^
            rattled_structures.append(structure)
            rattled_structures.append(structure)
                
        except Exception as e:
            print(f"An error occurred while generating rattled structures for simple equilibration: {e}")
            # Optionally, raise the error if you want it to halt the process
            raise e
    print(rattled_structures)
    return rattled_structures

@job # TODO: make run_scf_job // run_adslabs_job
def run_scf_job(
    scf_structures: list[Structure],
    static_maker: StaticMaker,
) -> Response:
    """Workflow of running the scf calculations.

    Parameters
    ----------
    scf_structures: list[Structure]
        The list of rattled strctures to run scf calculations on.
    static_maker: StaticMaker
        The static maker for the rattled structures.
    is_molecular: bool # TODO remove? could be the dict being called
        True if structure is a molecular structure, false if it is not (e.g. crystal)
    Returns
    -------
    Flow
        The flow of the scf calculations.
    """
    scf_jobs = []
    scf_outputs = defaultdict(list) # Output of the flow

    for i, scf_structure in enumerate(scf_structures):
        scf_job = static_maker.make(structure=scf_structure, prev_dir=None)
        scf_jobs.append(scf_job)
        scf_outputs["generated_hash"].append(scf_job.uuid) 
        scf_outputs["energy_in_eV"].append(scf_job.output.output.energy) 
        scf_outputs["sites"].append(scf_job.output.output.structure.sites) 
        scf_outputs["forces"].append(scf_job.output.output.forces) 
        scf_outputs["lattice_matrix"].append(scf_job.output.output.structure.lattice.matrix) 

    # Check types before creating Flow and Response
    # print(f"scf_jobs type: {type(scf_jobs)}")
    # print(f"scf_outputs type: {type(scf_outputs)}")

    # Ensure Flow is constructed correctly
    scf_flow = Flow(jobs=scf_jobs, output=scf_outputs)
    # print(f"scf_flow type: {type(scf_flow)}")

    return Response(replace=scf_flow)

@job # TODO: make write_scf_examples // adsorption_calculations
def write_scf_examples(
    scf_data: dict[str, list], # This causes the values to be in a list, probably by design
    prefix: str = "Job",
    is_molecular: bool | str = False,
    output_dir: str | Path | None = None,
):
    """Write the example files from the scf calculations for PANNA usage.

    Parameters
    ----------
    scf_data : dict[str, list]
        Dictionary containing data of the scf calculations.
    prefix: str
        The identifier of the structure the forcefield is being generated for
    is_molecular: bool or str
        True if structure is a molecular structure, false if it is not (e.g. crystal)
    output_dir : str or Path or None
        A directory to output the example files for PANNA to use
    Returns
    -------
    None
    """

    lattice_vectors = {}
    site_results = []

    # Get output data
    generated_hash = scf_data["generated_hash"][0]
    energy_in_eV = scf_data["energy_in_eV"][0]
    sites = scf_data["sites"][0]
    forces = scf_data["forces"][0]
    output_dir = Path(f'./PANNA/examples_files') # TODO: change dir name from /PANNA/ -> /<fireworks_wf_id>_PANNA/
    
    # print("Type of generated_hash (ideal is string, might be list): ", type(generated_hash))
    # print("The generated_hash value: ", generated_hash)
    # print(f"Output directory: {output_dir}")
    # print(f"Data received: {scf_data}")

    # Process each site
    for i in range(len(sites)):
        
        site_dict = sites[i].as_dict(1)
        atom = site_dict["label"]
        xcoord, ycoord, zcoord = map(float, site_dict["xyz"])
        xforce, yforce, zforce = map(float, forces[0])

        # Append a dictionary with all relevant information
        site_results.append({
            "index": i,
            "atom": atom,
            "xcoord": xcoord,
            "ycoord": ycoord,
            "zcoord": zcoord,
            "xforce": xforce,
            "yforce": yforce,
            "zforce": zforce,
        })
        
    # If the structure is not molecular, get the lattice vector data
    if is_molecular is False:
        lattice_matrix = scf_data["lattice_matrix"][0]

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

    # print(f"energy_in_eV is {energy_in_eV}")
    # print(f"generated_hash is {generated_hash}")
    # print("sites:")
    # for site in site_results:
    #     print(json.dumps(site,indent=4))
    # print(f"lattice_vectors:")
    # print(lattice_vectors)

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
        is_molecular=is_molecular,  # Convert to boolean
        lattice_vectors=lattice_vectors,
        energy_in_eV=energy_in_eV,
        sites=site_results
    )

    # Ensure the output directory exists
    output_dir.mkdir(parents=True, exist_ok=True)

    # Define the output file path
    output_file_path = output_dir / f"{prefix}_{generated_hash}.example"

    # Write the rendered output to the file
    with open(output_file_path, 'w') as f:
        f.write(rendered_output)

    print(f"Template written to {output_file_path}")
    
"""Flow for writing example files for a structure to use with PANNA surface."""

from dataclasses import dataclass
from jobflow import Flow, Job, Maker
from pymatgen.core.structure import Structure
from atomate2.vasp.jobs.core import StaticMaker
from pathlib import Path
# TODO: import the functions from job.py

@dataclass
class MLForceFieldMaker(Maker):
    """
    Workflow that writes example files from SCF calculated, rattled structures.

    The flow consists of the following steps:
      1. Generate rattled structures
      2. Run scf vasp calculations on the generated structures
      3. Write example files to a specified directory

    Parameters
    ----------
    name: str
        Name of the flow.
    examples_dir : str or Path or None
        A directory to output the example files for PANNA to use
    """

    name: str = "forge force field workflow"
    static_maker: Maker = field(default_factory=StaticMaker)
    example_dir: str | Path | None = Path(f'./PANNA/examples_files') # TODO: change dir name from /PANNA/ -> /<fireworks_wf_id>_PANNA/

    def make(
        self,
        structure: Structure,
        prefix: str = "Job",
        max_structures: int = 20,
        is_molecular: bool = False,
        purpose: str = "Simple Equilibration",
        use_custodian: bool = True
    ) -> Flow:
        """
        Generate a flow for writing example files for rattled scf structures.

        Parameters
        -----------
        structure: Structure
            A pymatgen structure object. The structure to be generate a MLFF for.
        prefix: str
            The identifier of the structure the forcefield is being generated for.
        max_structures: int or 20
            Number of structures to rattled to make the PANNA training set off of.
        example_dir: str or Path or None
            A directory to output the example files to.
        is_molecular: bool
            True if structure is a molecular structure, False if it is not (e.g. crystal systems)
        use_custodian: bool
            True if user wants to use custodian when running VASP (recommended), else False to run VASP without custodian
        Returns
        --------
        Flow
            A flow object for writing the example files
        """

        # If custodian is not used, set `job_type` to `direct`
        if not use_custodian:
            self.static_maker.run_vasp_kwargs["job_type"] = "direct"

        jobs: list[Job] = []

        # Step 1: Generate rattled structures
        generate_rattled_structures = generate_rattled(
            structure_to_rattle = structure,
            purpose = 'Simple Equilibration',
            num_structures = max_structures,# TODO update parameters
        )
        jobs += [generate_rattled_structures]
        rattled_structures = generate_rattled_structures.output

        # Step 2: Run SCF calculations on rattled structures
        run_scf_calculation = run_scf_job( 
            scf_structures=rattled_structures,
            static_maker=self.static_maker,
        )
        jobs +=  [run_scf_calculation]
        scf_outputs = run_scf_calculation.output

        # Step 3: Write example files to the specified directory
        write_example_files = write_scf_examples(
            scf_data=scf_outputs,
            prefix=prefix,
            is_molecular=is_molecular,
            output_dir=self.example_dir,
        )
        jobs += [write_example_files]

        return Flow(
            jobs=jobs,
            output=write_example_files.output,
            name = self.name,
        )