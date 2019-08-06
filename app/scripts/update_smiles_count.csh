#!/bin/csh -f 
foreach i (*.src.txt)
	setenv t $i:r:r
	echo $i $t 
	@ j = `wc -l $i | awk '{print $1}' `
	@ j = $j - 1 
	echo $j $1
	psql -h mem -U test zinc15 -c "update catalog set original_size= $j where short_name = '$t' "
end
