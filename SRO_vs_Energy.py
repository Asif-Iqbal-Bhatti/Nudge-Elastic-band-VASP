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

out_files = ["profile.dat", "accept.dat"];
for f in out_files: 
	if os.path.exists(f):
		os.remove(f) #this deletes the file
				
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
		yes="Accept"
	else:
		# reject the move - restore the old coordinates
		nreject += 1
		print ("{}: {:10.3f}%".format ("Reject ratio", (nreject/sample)*100 )  )
		tot_energy = old_energy	
		yes="Reject"
	return tot_energy, naccept, nreject, yes

'''------------------------------------MAIN PROGRAM--------------------------'''
if __name__ == "__main__":
	# First obtain the ground/optimized energy of the current SQS or SRO structure
	naccept = 0; nreject = 0; 
	old_energy = calculate_energy();
	n_atoms, pos, firstline, alat, Latvec1,Latvec2,Latvec3, elementtype, atomtypes, Coordtype = read_poscar();
	print ("----> Initial system Energy: {:15.8f}".format(old_energy), end = '\n')
	
	with open('profile.dat', 'a') as fdata3:
		fdata3.write ("T={:4f} K Sample={:5d} Atoms={:5d}\n".format(T, sample, n_atoms))
		fdata3.write ("{:17s} {:11.12s} {:6.6s} {:6s} {:8s}\n".format(" ","Ediff", "SRO", "Accept[%]", "Reject[%]" ))
		
	for i in range(1, sample):
		os.chdir('POS_'+str(i).zfill(3))
		
		#SRO=subprocess.call(['sqsgenerator','alpha','sqs','CONTCAR'], shell = False)
		SRO=float(os.popen("sqsgenerator alpha sqs CONTCAR --weight=1,0.5 | head -n 1 " ).read()[0:8] )
		new_energy = calculate_energy(); # Calculate new energy of the swap atoms
		print('{:3d} Energy in POS_{:3s} folder: {:15.6f} {:13.6f}'.format(i, str(i).zfill(3), new_energy, SRO), end = '\t')
		tot_energy, naccept, nreject, yes = metropolis_MC(new_energy, old_energy, naccept, nreject)
		
		os.chdir('../')
		
		with open('profile.dat', 'a') as fdata3:
			fdata3.write ("{:3d} {:9.10s} {:11.8f} {:8.5f} {:8.3f} {:8.3f} {:s}\n" \
			.format(i, 'POS_'+str(i).zfill(3), new_energy-old_energy, SRO, (naccept/sample)*100, (nreject/sample)*100, yes ) )
	
		if (yes=='Accept'):
			with open('accept.dat', 'a') as fdata4:
				fdata4.write ("{:9.10s} {:11.6f} {:8.5f} {:8.3f} {:8.3f} {:s}\n" \
				.format('POS_'+str(i).zfill(3), new_energy, SRO, (naccept/sample)*100, (nreject/sample)*100, yes ) )
	
	print('Accepted:: {:3d}, Rejected:: {:3d}'.format(naccept, nreject), end = '\n')
	with open('profile.dat', 'a') as fdata3:
		fdata3.write ('Accepted:: {:3d}, Rejected:: {:3d}\n'.format(naccept, nreject) )
		
	
