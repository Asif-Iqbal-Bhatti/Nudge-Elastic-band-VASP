#!/usr/bin/env python3
import ase.io
from ase.io import write, read
from ase.constraints import FixAtoms, FixScaled, FixedPlane, FixedLine
from ase.neb import NEB
import os, sys, shutil, subprocess

# Read initial and final states:
initial = ase.io.read('CONTCAR_1')
final   = ase.io.read('CONTCAR_2')

# Make a band consisting of 8 images:
images  = [initial]
images += [initial.copy() for _ in range(4)]
images += [final]
print (images, end="\n")

# improvedtangent, eb, aseneb :: Interpolate linearly the positions of the three middle images:
neb = NEB(images, method='improvedtangent', dynamic_relaxation=True, fmax=0.01, 
climb=True, parallel=True, remove_rotation_and_translation=True)
neb.interpolate(method='idpp')

for dd, image in enumerate(images[:15]):
	shutil.rmtree(f'{str(dd).zfill(2)}', ignore_errors=True)
	os.mkdir(f'{str(dd).zfill(2)}')
	os.chdir(f'{str(dd).zfill(2)}')
	write('POSCAR', image, ignore_constraints=True, vasp5=True,sort=True, direct=True)
	subprocess.call(['../selective.sh',], shell = False)
	subprocess.call(
		['cp', '-r', 'POSCAR', f'../POS_{str(dd).zfill(3)}'], shell=False
	)

	os.chdir('../')	


