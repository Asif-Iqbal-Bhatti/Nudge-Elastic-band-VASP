#!/usr/bin/env python3
#--------------------------------------------------------------------------------------
AUTHOR :: Asif Iqbal
#--------------------------------------------------------------------------------------

from ase import Atoms
import ase.io
from ase.io import write, read
from ase.io.vasp import write_vasp, read_vasp
from ase.constraints import FixAtoms, FixScaled, FixedPlane, FixedLine, FixCartesian
from ase.visualize.plot import plot_atoms
import matplotlib.pyplot as plt

#--------------------------------------------------------------------------------------
# Read initial and final states:
initial = read_vasp('POSCAR')
pos = initial.get_positions()
ucell = initial.get_cell()
atoms = Atoms(positions=pos, symbols='AxBxCxDxEx',cell=ucell, pbc=[True,True,True])
#--------------------------------------------------------------------------------------
c = []
#c = FixAtoms(indices=[atom.index for atom in atoms if atom.symbol == 'Hf'])

# """Constrain an atom index *a* to move in a given plane only.

for atom in atoms:
  c.append( FixedPlane( atom.index, ( 0, 0, 1) ) )
atoms.set_constraint(c)

write_vasp("OUT.vasp", atoms=atoms, vasp5=True, ignore_constraints=False)
#print (c)

fig, ax = plt.subplots()
ax.set(xlim=(-1, 1), ylim = (-1, 1))
a_circle = plt.Circle((23, 11.5), 2.8, alpha = 0.5, capstyle='butt')
ax.add_artist(a_circle)
plot_atoms(atoms, ax, radii=0.5, rotation=('00x,00y,00z'))
plt.show()




