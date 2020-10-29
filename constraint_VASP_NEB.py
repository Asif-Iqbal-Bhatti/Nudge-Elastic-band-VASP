#!/usr/bin/env python3
#-------------------------------------------------------------------------------------
# AUTHOR :: Asif Iqbal
# USAGE :: To constraint the atoms in the specific direction for DRAG calcualtions.
# Copyright Asif Iqbal
#-------------------------------------------------------------------------------------
from ase import Atoms
import ase.io
from ase.io import write, read
from ase.io.vasp import write_vasp, read_vasp
from ase.constraints import FixAtoms, FixScaled, FixedPlane, FixedLine, FixCartesian
from ase.visualize.plot import plot_atoms
import matplotlib.pyplot as plt


def data_for_cylinder_along_z(center_x,center_y,radius,height_z):
    z = np.linspace(0, height_z, 50)
    theta = np.linspace(0, 2*np.pi, 50)
    theta_grid, z_grid = np.meshgrid(theta, z)
    x_grid = radius*np.cos(theta_grid) + center_x
    y_grid = radius*np.sin(theta_grid) + center_y
    return x_grid,y_grid,z_grid
    
c = []
# Read initial and final states:
initial = read_vasp('POSCAR')
pos = initial.get_positions()
ucell = initial.get_cell()
type = initial.get_chemical_symbols()
atoms = Atoms(positions=pos, symbols=type, cell=ucell, pbc=[True,True,True])

#c = FixAtoms(indices=[atom.index for atom in atoms if atom.symbol == 'Hf'])

#                """Constrain an atom index *a* to move in a given plane only.
#for atom in atoms:
#	c.append( FixedPlane(atom.index, ( 0, 0, 1)) )
c = [ FixedPlane( atom.index, ( 0, 0, 1) )  for atom in atoms ]
atoms.set_constraint(c)

write_vasp("OUT.vasp", atoms=atoms, vasp5=True, ignore_constraints=False)
#print (c)
fig = plt.figure()
ax = fig.add_subplot(111)
#ax.set_aspect("auto")
ax.set(xlim=(-1, 1), ylim = (-1, 1) )
a_circle = plt.Circle((23, 11.7), 2.7, alpha = 0.5,fill=False, ec='red')
a1_circle = plt.Circle((23, 11.7), 0.2,fill=False, ec='red')
ax.add_artist(a_circle)
ax.add_artist(a1_circle)
plot_atoms(atoms, ax, radii=0.5, rotation=('0x,0y,00z'))
plt.savefig("test.eps", format="eps", dpi=600)
plt.show()




