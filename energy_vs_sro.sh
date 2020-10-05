#!/bin/bash
#--------------------------------------------------------------------------------------------
#### sqsgenerator code has been modified such that this script can read and parse in a
#### systematic way.
#### ONLY 1st and 2nd shells have been considered.
#### This scripte extract and computes the Energy and SRO value and then rearrange and 
#### sort the file with reference to the Acceptance criterion generated with python 
#### script. FLOWCHART ::
#### FIRST RUN :: SRO_vs_energy.py script then this script.
#### "Accept.dat" file is generated from SRO_vs_energy.py script.
#--------------------------------------------------------------------------------------------
echo > ratio.dat
for d in $(seq -f "%03g" 1 1599); do
f=${d%/}; ext=${d##*-}
E=`grep "free  energy   TOTEN  =" POS_$d/OUTCAR | tail -1 | awk '{printf "%f", $5 }'`
SRO=`sqsgenerator alpha sqs POS_$d/CONTCAR --weight=1 --verbosity=3`
  #echo $d $E $SRO | awk '{printf "%s" "\t" "%f" "\t" "%s\n", $1, $2, $3 }' >> ratio.dat
echo "POS_"$f";" $E";" $SRO  >> ratio.dat
done
##--------------------------------------------------------------------------------------------
input="ratio.dat" ; sed -i '/^[[:space:]]*$/d' $input
while IFS= read -r line
do
printf '%s\n' "$line" | awk -F\; '{print $1, $2, $3}' >> .tmp1
printf '%s\n' "$line" | awk -F\; '{for(i=1;i<=NF;i++) {if($i ~ /Ti-Nb|Nb-Ti/){print $i}}}' >> .tmp2
printf '%s\n' "$line" | awk -F\; '{for(i=1;i<=NF;i++) {if($i ~ /Ti-Zr|Zr-Ti/){print $i}}}' >> .tmp3
printf '%s\n' "$line" | awk -F\; '{for(i=1;i<=NF;i++) {if($i ~ /Ta-Hf|Hf-Ta/){print $i}}}' >> .tmp4
printf '%s\n' "$line" | awk -F\; '{for(i=1;i<=NF;i++) {if($i ~ /Ta-Ti|Ti-Ta/){print $i}}}' >> .tmp5
printf '%s\n' "$line" | awk -F\; '{for(i=1;i<=NF;i++) {if($i ~ /Ta-Nb|Nb-Ta/){print $i}}}' >> .tmp6
printf '%s\n' "$line" | awk -F\; '{for(i=1;i<=NF;i++) {if($i ~ /Ta-Zr|Zr-Ta/){print $i}}}' >> .tmp7
printf '%s\n' "$line" | awk -F\; '{for(i=1;i<=NF;i++) {if($i ~ /Hf-Ti|Ti-Hf/){print $i}}}' >> .tmp8
printf '%s\n' "$line" | awk -F\; '{for(i=1;i<=NF;i++) {if($i ~ /Hf-Nb|Nb-Hf/){print $i}}}' >> .tmp9
printf '%s\n' "$line" | awk -F\; '{for(i=1;i<=NF;i++) {if($i ~ /Hf-Zr|Zr-Hf/){print $i}}}' >> .tmp10
printf '%s\n' "$line" | awk -F\; '{for(i=1;i<=NF;i++) {if($i ~ /Nb-Zr|Zr-Nb/){print $i}}}' >> .tmp11
printf '%s\n' "$line" | awk -F\; '{for(i=1;i<=NF;i++) {if($i ~ /Ti-Ti/){print $i}}}' >> .tmp12
printf '%s\n' "$line" | awk -F\; '{for(i=1;i<=NF;i++) {if($i ~ /Nb-Nb/){print $i}}}' >> .tmp13
printf '%s\n' "$line" | awk -F\; '{for(i=1;i<=NF;i++) {if($i ~ /Ta-Ta/){print $i}}}' >> .tmp14
printf '%s\n' "$line" | awk -F\; '{for(i=1;i<=NF;i++) {if($i ~ /Hf-Hf/){print $i}}}' >> .tmp15
printf '%s\n' "$line" | awk -F\; '{for(i=1;i<=NF;i++) {if($i ~ /Zr-Zr/){print $i}}}' >> .tmp16
done < "$input"

paste -d " " .tmp1 .tmp2 .tmp3 .tmp4 .tmp5 .tmp6 .tmp7 .tmp8 .tmp9 .tmp10 .tmp11 .tmp12 .tmp13 .tmp14 .tmp15 .tmp16 > energy_vs_sro.dat
sed -i 's/=/ /g' energy_vs_sro.dat
awk -F' ' 'NR==FNR{c[$1$2]++;next};c[$1$2] > 0' accept.dat energy_vs_sro.dat | sort -n -k2 | tee FINAL.dat
rm .tmp*

