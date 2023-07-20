#!/usr/bin/env python3

# https://zhuanlan.zhihu.com/p/397532659
# https://pymatgen.org/pymatgen.analysis.transition_state.html

import os, sys, shutil, subprocess
from ase.io import read, write
from ase.dyneb import DyNEB
from ase.neb import NEB, NEBTools
from ase.optimize import MDMin, FIRE, BFGS, GPMin, BFGSLineSearch
from ase.constraints import FixAtoms, FixScaled, FixedPlane, FixedLine


initial = read('CONTCAR_00')
final   = read('CONTCAR_0N')

images  = [initial]
images += [initial.copy() for i in range(5)]
images += [final]
print (f"{images}\n")

# improvedtangent, eb, aseneb :: 
neb = NEB(images, method='improvedtangent', allow_shared_calculator = True,
       climb = False, parallel = False, remove_rotation_and_translation = False)

#neb = DyNEB(images, k=0.1, fmax=0.01, climb=True, parallel=False, 
#        remove_rotation_and_translation=False, world=None, dynamic_relaxation=True, 
#        scale_fmax=0.0, method='improvedtangent', 
#        allow_shared_calculator=True, precon=None)
            
neb.interpolate(method='idpp')


for i, image in enumerate(images):
    dirname = str(i).zfill(2)
    shutil.rmtree(dirname, ignore_errors=True)
    os.mkdir(dirname)
    os.chdir(dirname)
    write('POSCAR', image, ignore_constraints=False, vasp5=True, sort=False, direct=True)
    #subprocess.call(['cp','-r','POSCAR','../POS_'+str(dd).zfill(3)], shell = False)    
    shutil.copy('POSCAR', f'../POS_{i:03d}')
    os.chdir('../')
    

def analyseResults():
    fig, ax = plt.subplots(1, 1, figsize=(8, 6))
    images = read('neb.traj@-7:')
    nebtools = NEBTools(images)
    
    Ef, dE = nebtools.get_barrier(fit=True, raw=False)
    max_force = nebtools.get_fmax()
    
    print(f"{'BARRIER ENERGY':30s}: {Ef:6.5f} eV")
    print(f"{'ELEMENTARY REACTION':30s}: {dE:6.5f} eV")
    print(f"{'MAX FORCE':30s}: {max_force:6.6f} eV/A")
    #ax = fig.add_axes((0.15, 0.15, 0.8, 0.75))
    fig = nebtools.plot_band(ax=ax)
    fig.savefig(outFile +'.png', dpi=300)
    nebtools.plot_bands(constant_x=False, constant_y=False, nimages=None, label='nebplots')
    
