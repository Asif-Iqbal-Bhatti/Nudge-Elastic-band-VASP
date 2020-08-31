#!/bin/sh

sed -i '7aSelective Dynamics' POSCAR

for j in $(seq 10 279) # add "F F T" to the end of the line

do
	sed -i "${j}s/$/&  T T F/g" POSCAR
done

#sed -i 's/^M/ /g' POSCAR

