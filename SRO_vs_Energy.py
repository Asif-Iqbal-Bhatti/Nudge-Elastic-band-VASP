#!/usr/bin/env python3
#------------------------------------------------------------------------
# USAGE  :: python3 monte_carlo_HEA.py 
# Author :: Asif Iqbal
# DATED  :: 03/09/2020
# Metropolis Monte Carlo in a NVT (canonical) ensemble
# ADAPTED FROM:: https://chryswoods.com/intro_to_mc/part1/metropolis.html
# This script calculates the energy of the system by swapping the atoms
# and invoking the MC code to find the lowest structure.
#------------------------------------------------------------------------

import numpy as np
import os, sys, random, subprocess, shutil
import os.path, time

k = 8.617333262145E-5 # Boltzmann constant
T = 500 # Temperature in Kelvin
sample = 101 # Number of sample could be # of atoms to swap

if os.path.exists('profile.dat'):
	os.remove('profile.dat') #this deletes the file
				
def read_poscar():
	pos = []; kk = []; lattice = []; sum = 0
	file = open('CONTCAR','r')
	firstline  = file.readline() # IGNORE first line comment
	alat = float( file.readline() )# scale
	Latvec1 = file.readline().split(); #print("{:9.6f} {:9.6f} {:9.6f}".format(float(Latvec1[0]),float(Latvec1[1]),float(Latvec1[2])))
	Latvec2 = file.readline().split(); #print("{:9.6f} {:9.6f} {:9.6f}".format(float(Latvec2[0]),float(Latvec2[1]),float(Latvec2[2])))
	Latvec3 = file.readline().split(); #print("{:9.6f} {:9.6f} {:9.6f}".format(float(Latvec3[0]),float(Latvec3[1]),float(Latvec3[2]))) 
	elementtype= file.readline(); #print ("{}".format(elementtype.split() ))
	atomtypes  = file.readline(); #print ("{}".format(atomtypes.split() ))
	Coordtype  = file.readline().split()
	nat = atomtypes.split()
	nat = [int(i) for i in nat]
	for i in nat: sum = sum + i
	n_atoms = sum
	# print ("Number of atoms:", (n_atoms), end = '\n')	
	# Reading the Atomic positions				
	for x in range(int(n_atoms)):
		coord = file.readline().split()
		coord = [float(i) for i in coord]
		pos = pos + [coord]
	pos = np.array(pos)
	file.close()
	return n_atoms,pos,firstline,alat,Latvec1,Latvec2,Latvec3,elementtype,atomtypes,Coordtype

def calculate_energy():
	#old_energy = os.popen(" grep 'free  energy   TOTEN  =' OUTCAR | tail -1 | awk '{print $5 }' " ).read()
	#old_energy = float ( old_energy )
	f = open('OUTCAR',"r")
	lines = f.readlines()
	f.close()
	for i in lines:
		word = i.split()
		if "free  energy   TOTEN  =" in i:
			ii=lines.index(i)
	old_energy =  float(lines[ii].split()[4])
	return old_energy

def metropolis_MC(new_energy, old_energy, naccept, nreject):	
	tot_energy = []
	accept = False;
	# Accept if the energy goes down
	if (new_energy <= old_energy):
		accept = True
	else:
		# Apply the Monte Carlo test and compare
		# exp( -(E_new - E_old) / kT ) >= rand(0,1)
		x = np.exp( -(new_energy - old_energy) / (k*T) )
		#print (x)
		if (x >= random.uniform(0.0,1.0)):
			accept = True
		else:
			accept = False
	if accept:
		# Accept the move
		naccept += 1; 
		print ("{}: {:10.3f}%".format("Accept ratio", (naccept/sample)*100  )  )
		tot_energy = new_energy
	else:
		# reject the move - restore the old coordinates
		nreject += 1
		print ("{}: {:10.3f}%".format ("Reject ratio", (nreject/sample)*100 )  )
		tot_energy = old_energy	
	return tot_energy, naccept, nreject

'''------------------------------------MAIN PROGRAM--------------------------'''
	
# First obtain the ground/optimized energy of the current SQS or SRO structure
naccept = 0; nreject = 0; 
old_energy = calculate_energy();
n_atoms, pos, firstline, alat, Latvec1,Latvec2,Latvec3, elementtype, atomtypes, Coordtype = read_poscar();
print ("----> Initial system Energy: {:15.8f}".format(old_energy), end = '\n')

with open('profile.dat', 'a') as fdata3:
	fdata3.write ("T={:5f} Sample={:5d} Atoms={:5d}\n".format(T, sample, n_atoms))
with open('profile.dat', 'a') as fdata3:
	fdata3.write ("{:20s} {:15.12s} {:12s} {:12s} {:12s}\n".format(" ","Ediff", "SRO", "Acceptance", "Rejection" ))
	
for i in range(1, sample):

	os.chdir('POS_'+str(i).zfill(3))
	
	#SRO=subprocess.call(['sqsgenerator','alpha','sqs','CONTCAR'], shell = False)
	
	SRO=float ( os.popen("sqsgenerator alpha sqs CONTCAR | grep 'a =' | cut -d'=' -f 2 " ).read()[0:12] )
	
	shell_1=float ( os.popen("sqsgenerator alpha sqs CONTCAR | grep 'a =' | cut -d'=' -f 2 " ).read())
	
	new_energy = calculate_energy(); # Calculate new energy of the swap atoms
	
	print('{:3d} Energy in POS_{:3s} folder: {:15.6f} {:15.12f}'.format(i, str(i).zfill(3), new_energy, SRO), end = '\t')
	
	tot_energy, naccept, nreject = metropolis_MC(new_energy, old_energy, naccept, nreject)
	
	os.chdir('../')
	
	with open('profile.dat', 'a') as fdata3:
		fdata3.write ("{:3d} {:15.15s} {:15.8f} {:22.12f} {:12.3f}% {:12.3f}%\n".format(i, 'POSCAR_'+str(i).zfill(3), new_energy-old_energy, SRO, (naccept/sample)*100, (nreject/sample)*100 ))


print('Accepted:: {:3d}, Rejected:: {:3d}'.format(naccept, nreject), end = '\n')

	
