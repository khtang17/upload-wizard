#!/bin/csh -f 
foreach i (*.filt.txt)
	setenv t $i:r:r
	echo $i $t 
	@ j = `wc -l $i | awk '{print $1}' `
	@ j = $j - 1 
	if ($j < 0) then
		@ j = 0
	endif
	echo $j $t
	psql -h mem -U test zinc15 -c "update catalog set num_filtered= $j where short_name = '$t' "
end
