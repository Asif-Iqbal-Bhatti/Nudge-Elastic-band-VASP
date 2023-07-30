# Calculate Peierls Barrier for High Entropy Alloys (HEAs) using Nudge Elastic Band or Drag Method

**This script is compatible with Python 3 or higher versions.**

[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://GitHub.com/Naereen/StrapDown.js/graphs/commit-activity)  
![pypi](https://img.shields.io/pypi/v/pybadges.svg)  
![versions](https://img.shields.io/pypi/pyversions/pybadges.svg)  
[![GPLv3 license](https://img.shields.io/badge/License-GPLv3-blue.svg)](http://perso.crans.org/besson/LICENSE.html)  

NB: The settings for the NEB calculations can be tricky at times; therefore, caution should be taken while using the provided code.

The barrier obtained (Ta: 46.3 meV/b) with this setup agrees favorably with the values given in the references. Hence, I can be sure my setup is right, and I can extend this approach to High Entropy Alloys.

## Instructions:
- Initial and final geometries should be fully relaxed.
- Generate the transition path (initial guess path) between the initial and final configurations using ASE-NEB by interpolating linearly or using idpp.
- The intermediate images should be constrained and relaxed accordingly.

## NEB Calculation:

To perform the Nudge Elastic Band (NEB) calculation:
1. Ensure that the initial and final geometries are fully relaxed.
2. Use ASE-NEB to generate the transition path (initial guess path) between the two configurations.
3. Constrain the intermediate images in the transition path.
4. Perform relaxation perpendicular to the screw dislocation line on the plane using VASP5 format (T T F).
5. The script `neb_vasp.py` calls the `selective_dynamics.sh` bash file to append T T F to the POSCAR file.

## Drag Method:

For the Drag Method:
1. Constrain the atoms according to the problem.
2. Perform relaxation perpendicular to the screw dislocation line on the plane using VASP5 format (T T F).

NB: Calling a script from Python is not a good idea. Instead, consider internally calling the function using the "ase" module (https://wiki.fysik.dtu.dk/ase/).

## Example Code Snippet:

```python
# ----------------- Constraining the atoms ---------------------
# shutil.copyfile('POSCAR_'+str(cnt).zfill(2), 'POSCAR' )
initial = read('POSCAR_'+str(cnt).zfill(2))
p_pos = initial.get_positions()
p_ucell = initial.get_cell()
p_type = initial.get_chemical_symbols()
p_ll = Atoms(positions=p_pos, symbols=p_type, cell=p_ucell, pbc=(1, 1, 1))
# for atom in p_ll:
#   p_constr.append(FixedPlane(atom.index, (0, 0, 1)))
p_constr = [FixedPlane(atom.index, (0, 0, 1)) for atom in p_ll]
p_ll.set_constraint(p_constr)
write_vasp("POSCAR", atoms=p_ll, vasp5=True, ignore_constraints=False)
# subprocess.call(['../selective.sh'], shell=False)
os.chdir('../')
cnt += 1
