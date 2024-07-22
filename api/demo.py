import os
import subprocess

def mlff_trj_gen(structure_name, calc_dir, temperature_range, master_input, master_data, master_slurm):
    """
    To demonstrate input generator

    Parameters
    ----------
    structure_name : str
        Name of the structure
    calc_dir : str
        Path to the calculations directory
    temperature_range : iterable of floats
        Range of temperatures for calculations
    master_input : str
        Path to the master input file
    master_data : str
        Path to the master data file
    master_slurm : str
        Path to the master slurm file
    
    Changes:
    "../../" + 
    """
    os.chdir(calc_dir)
    for temp in temperature_range:
        os.mkdir(str(temp))
        os.chdir(str(temp))
        subprocess.call('cp {} in.{}'.format( "../../" + master_input, structure_name), shell=True)
        subprocess.call('cp {} data.{}'.format("../../" + master_data, structure_name), shell=True)
        subprocess.call('cp {} {}.slurm'.format("../../" + master_slurm, structure_name), shell=True)
        subprocess.call("sed -i 's/master/{}/g' in.*".format(structure_name), shell=True)
        sed_string = "sed -i -e 's/master_jobname/{}/g ; s/master_prefix/{}/g ; s/master_temperature/{}/g' *.slurm".format(structure_name, structure_name, temp)
        subprocess.call(sed_string, shell=True)
        os.chdir("../")

def zip_dir(dir_to_zip):
    """
    To zip a directory with subdirectories
    
    Parameters
    ----------
    dir_to_zip : str
        Path to directory to zip recursively
    
    Returns
    -------
    zip_path : str
        Path to the zip file
    """
    zip_name = 'demo.zip'
    zip_path = os.path.join(dir_to_zip, zip_name)
    
    # Execute the zip command
    result = subprocess.call(f'zip -r {zip_path} {dir_to_zip}', shell=True)
    
    # Handle potential errors
    if result != 0 or not os.path.exists(zip_path):
        raise RuntimeError(f"Failed to create zip file at {zip_path}")
    
    return zip_path