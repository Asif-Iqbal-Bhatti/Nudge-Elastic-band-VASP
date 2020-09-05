#!/bin/bash
#### NB: sqsgenerator code has been modified such that this script can read and parse in a
####     systematic manner.
echo > ratio.dat
for d in */; 
do
f=${d%/}; #ext=${d##*-}
E=`grep "free  energy   TOTEN  =" $d/OUTCAR | tail -1 | awk '{printf "%f", $5 }'`
#SRO=`sqsgenerator alpha sqs $d/CONTCAR --weights=1,0.5 --verbosity=1 | grep "a =" | awk '{printf "%f", $3 }'`
SRO=`sqsgenerator alpha sqs $d/CONTCAR --weights=1,0.5 --verbosity=3`
#echo $d $E $SRO | awk '{printf "%s" "\t" "%f" "\t" "%s\n", $1, $2, $3 }' >> ratio.dat
echo $f";" $E";" $SRO  >> ratio.dat
done

input="ratio.dat"
sed -i '/^[[:space:]]*$/d' $input
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
	
done < "$input"

paste -d " " .tmp1 .tmp2 .tmp3 .tmp4 .tmp5 .tmp6 .tmp7 .tmp8 .tmp9 .tmp10 .tmp11 | tee energy_vs_sro.dat


rm .tmp*

