from jobflow import Flow, Response, job
from pymatgen.core import Structure
from atomate2.vasp.jobs.core import StaticMaker
from pymatgen.io.cif import CifParser

# different generators -> error handlers try execpt raiseerror
@job # TODO: make generate_rattled // generate_slab
def generate_rattled(
    structure_to_rattle: Structure,
    num_structures: int,
) -> list[Structure]:
    """Generate the rattled structures for the training set.

    Parameters
    ----------
    structure_to_rattle: Structure
        The structure to rattled.
    num_structures: int
        The number of rattled structures to generate.

    Returns
    -------
    list[Structure]
        Rattled structures.
    """
    """
    # TODO: convert cif file to Structure? depends on implementation
    from pymatgen.io.cif import CifParser
    parser = CifParser("mycif.cif")
    structure = parser.get_structures()[0]
    """

    # old: structure_file = fw_spec['structure_file']

    # Create a temporary file for the .cif file
    with tempfile.NamedTemporaryFile(suffix=".cif", delete=False) as temp_cif_file:
        cif_file_path = temp_cif_file.name
    try:
        # # Convert structure file to .cif using openbabel
        # file_extension = structure_file.split('.')[-1]
        # mol = pybel.readfile(file_extension, structure_file).__next__()
        # mol.write(format='cif', filename=cif_file_path, overwrite=True)
        # # Parse .cif file using CifParser from pymatgen
        # parser = CifParser(cif_file_path)
        # structures = parser.parse_structures(primitive=True)
        
        # # Check if structures were successfully parsed
        # if not structures:
        #     raise ValueError("No structures found in the CIF file.")
        #^ TODO adjust
        structure = structures[0]
        rattled_structures = []
        # Generate rattled structures
        for i in range(num_structures):
            # Determine standard deviation based on index
            std_dev = 0.005 if i < num_structures // 2 else 0.01
            # Create ASE Atoms object from pymatgen structure
            element_symbols = [site.specie.symbol for site in structure]
            atom_positions = structure.cart_coords
            atoms = Atoms(symbols=element_symbols, positions=atom_positions)
            # Apply random displacements using ASE's built-in 'rattle' function
            atoms.rattle(stdev=std_dev)
            # Convert back to pymatgen structure
            rattled_structure = Structure(
                lattice=structure.lattice,
                species=element_symbols,
                coords=atoms.get_positions(),
                site_properties=structure.site_properties,
            )
            rattled_structures.append(rattled_structure)
    
    finally:
        # Clean up temporary .cif file
        if os.path.isfile(cif_file_path):
            os.remove(cif_file_path)

    # rattled_structures: list of pymatgen.core.structure.Structure objects          
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
        The list of all possible configurations of slab structures with adsorbates.
    Returns
    -------
    Flow
        The flow of the scf calculations.
    """
    scf_jobs = []
    scf_outputs = defaultdict(list) # output of the flow

    for i, scf_structure in enumerate(scf_structures):
        scf_job = static_maker.make(structure=scf_structure, prev_dir=None)
        # scf_jobs.append_name(f"scfconfig_{i}")

        scf_jobs.append(scf_job)
        # scf_outputs["configuration_number"].append(i)
        scf_outputs["generated_hash"].append(scf_job.uuid)
        scf_outputs["energy_in_eV"].append(scf_job.output.output.energy)
        scf_outputs["sites"].append(scf_job.output.structure.sites)
        scf_outputs["forces"].append(scf_job.output.output.forces)
        scf_outputs["dirs"].append(scf_job.output.dir_name)
        scf_outputs["lattice_matrix"].append(scf_job.output.output.structure.lattice.matrix)


    scf_flow = Flow(scf_jobs, scf_outputs)
    return Response(replace=scf_flow)


@job # TODO: make write_scf_examples // adsorption_calculations
def write_scf_examples(
    scf_data: dict[str, list],
    output_dir: str | Path | None = None,
):
    """Write the example files from the scf calculations for PANNA usage.

    Parameters
    ----------
    scf_data : dict[str, list]
        Dictionary containing data of the scf calculations.
    output_dir : str or Path or None
        A directory to output the example files for PANNA to use

    Returns
    -------
    Nothing
    """