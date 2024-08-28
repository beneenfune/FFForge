import os
import subprocess
import shutil

def mlff_trj_gen(structure_name, calc_dir, temperature_range, master_input, master_data, master_slurm):
    """
    Demonstrate input generator

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
    os.chdir("../")

def zip_dir(source_folder, output_path):
    """
    Zip a directory with subdirectories
    
    Parameters
    ----------
    source_folder : str
        Path to directory to zip recursively
    output_path : str
        Path to the output zip file (without the .zip extension)
    
    Returns
    -------
    zip_path : str
        Path to the created zip file
    """
    shutil.make_archive(output_path, 'zip', source_folder)
    return output_path + '.zip'

def remove_dir(directory_path):
    """
    Remove the specified directory and all its contents.

    Parameters
    ----------
    directory_path : str
        Path to the directory to remove.
    """
    if os.path.exists(directory_path) and os.path.isdir(directory_path):
        shutil.rmtree(directory_path)
        print(f"Directory {directory_path} has been removed.")
    else:
        print(f"Directory {directory_path} does not exist.")