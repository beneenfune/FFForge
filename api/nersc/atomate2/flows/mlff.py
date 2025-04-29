"""Flow for writing example files for a structure to use with PANNA surface."""

from dataclasses import dataclass
from jobflow import Flow, Job, Maker
from pymatgen.core.structure import Structure
from atomate2.vasp.jobs.core import StaticMaker
from pathlib import Path


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
    """

    name: str = "forge force field workflow"
    example_dir: str | Path | None = None
    
    def make(
        self,
        structure: Structure,# TODO: implement this parameter somehow -> structure_generator: function,
        max_structures: int | 20,
    ) -> Flow:
        """
        Generate a flow for writing example files for rattled scf structures.

        Parameters
        ----------
        structure: Structure
            A pymatgen structure object. The structure to be generate a MLFF for.
        max_structures: int or 20
            Number of structures to rattled to make the PANNA training set off of.
        example_dir: str or Path or None
            A directory to output the example files to.
        Returns
        -------
        Flow
            A flow object for writing the example files
        """ 

        jobs: list[Job] = [] # jobs = []
        # generate_scf_structures = structure_generator(*args)
        generate_rattled_structures = generate_rattled( # TODO: make generate_rattled // generate_slab
            structure_to_rattle = structure,
            num_structures = max_structures,
        ) # create_structures_job = generate_rattles_structures(user_input_structure)
        jobs += [generate_rattled_structures] # jobs += [create_structures_job]
        rattled_structures = generate_rattled_structures.output # rattled_structures = create_structures_job.output

        # understand run_adslab_jobs function and see how to "parallelizes" - function for running 300 jobs
        run_scf_calculation = run_scf_job( # TODO: make run_scf_job // run_adslabs_job
            scf_structures=rattled_structures,
        ) # scf_jobs_flow = Flow(scf_jobs)
        jobs +=  [run_scf_calculation]
        scf_outputs = run_scf_calculation.output

        write_examples = write_scf_examples( # no need to fetch since its all in the output attribute
            scf_data=scf_outputs,
            output_dir=example_dir, # TODO: check in sum like from_prev = prev_dir is not None if prev_dir is not None:
        ) # parse_data_scf_job = WriteExampleMaker.make(db_info, wtv arguments)
        jobs += [write_example_files] # jobs += [parse_data_scf_job]

        return Flow(
            jobs=jobs,
            output=write_example_files.output,
            name = self.name,
        )
