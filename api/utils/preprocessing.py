import json
import sys
import subprocess
import os
import glob
import hashlib
import random
import numpy as np
import matplotlib.pyplot as plt
from math import ceil
import scipy as sp
import time
import ast
import math
from ase.io import read, write
import string
import time

def generate_random_string(length):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for i in range(length))

def generate_hash():
    current_time = str(time.time()).encode('utf-8')
    random_string = generate_random_string(10).encode('utf-8')
    hash_object = hashlib.sha256(current_time + random_string)
    return hash_object.hexdigest()

def generate_rattled_structures(input_structure, num_structures, output_dir, prefix=None, stdev=0.001):
    structure = read(input_structure)
    for i in range(num_structures):
        seed = random.randint(10000000, 99999999)
        copy_structure = structure.copy()
        copy_structure.rattle(stdev=stdev, seed=seed)
        if prefix:
            write(output_dir + prefix + "_" + generate_hash() + ".xyz", copy_structure)
        else:
            write(output_dir + generate_hash() + ".xyz", copy_structure)

import os

def xyz_to_qe(xyz_file_path, output_dir, boundary_extra=15):
    # Read the XYZ file and extract atomic positions
    with open(xyz_file_path, 'r') as xyz_file:
        lines = xyz_file.readlines()
    
    num_atoms = int(lines[0].strip())
    atom_coords = []
    
    for line in lines[2:2 + num_atoms]:
        parts = line.split()
        atom_coords.append(f"{parts[0]} {parts[1]} {parts[2]} {parts[3]}")
    
    atom_coords_str = "\n".join(atom_coords)
    
    bounds_info = subprocess.getoutput("/global/cfs/cdirs/m4537/rsb/codes/tod_scripts/scripts/getBounds.pl -b {}".format(xyz_file_path)).split()
    
    # Parse the bounds info to get alat, blat, clat
    xmin = float(bounds_info[bounds_info.index('X') + 1])
    xmax = float(bounds_info[bounds_info.index('X') + 2])
    ymin = float(bounds_info[bounds_info.index('Y') + 1])
    ymax = float(bounds_info[bounds_info.index('Y') + 2])
    zmin = float(bounds_info[bounds_info.index('Z') + 1])
    zmax = float(bounds_info[bounds_info.index('Z') + 2])
    
    alat = xmax - xmin + boundary_extra
    blat = ymax - ymin + boundary_extra
    clat = zmax - zmin + boundary_extra
    
    # Get the file name without extension
    file_name = os.path.basename(xyz_file_path).replace('.xyz', '')
    
    # Create the Quantum Espresso input file content
    qe_input_content = f"""
&control
    calculation = 'scf'
    restart_mode='from_scratch'
    prefix = '{file_name}'
    pseudo_dir = '/global/cfs/cdirs/m4537/rsb/qe/pseudo/sssp_precision/',
    outdir = './outdir',
    verbosity = 'high'
    tprnfor = .TRUE.,
/
&system
    ibrav           = 14
    a               = {alat},
    b               = {blat},
    c               = {clat},
    nat             = {num_atoms},
    ntyp            = 1,
    ecutwfc         = 50,
    ecutrho         = 500,
    occupations = 'smearing',
    smearing = 'gaussian',
    degauss = 0.011,
    nspin = 1,
    assume_isolated = 'mt',
/
&electrons
    electron_maxstep = 200
    conv_thr        = 1.0d-8
    mixing_beta     = 0.3
/
&IONS
/
&CELL
/
ATOMIC_SPECIES
Au 196.96657 Au_ONCV_PBE-1.0.oncvpsp.upf 

ATOMIC_POSITIONS (angstroms)
{atom_coords_str}

K_POINTS (gamma)
"""
    
    # Write the content to the output file
    output_file_path = os.path.join(output_dir, f"{file_name}.in")
    with open(output_file_path, 'w') as output_file:
        output_file.write(qe_input_content)
    
    #print(f"Quantum Espresso input file generated at: {output_file_path}")