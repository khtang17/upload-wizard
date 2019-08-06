#!/bin/csh -fx

set catname=$1
echo "This is catname: $catname"

#source /nfs/soft/jchem/current/env.csh
source /nfs/soft/mitools/env.csh
source /nfs/soft/www/apps/zinc15/envs/edge/env.csh
setenv ZINC_CONFIG_ENV admin
setenv ZINC_CONFIG_SETUP_SKIP blueprints 
#setenv ZINC_CONFIG_ENV admin-private
#tmp...
#setenv ZINC_TAUTOMERIZE 'zincload-tautomerize --rules=/nfs/scratch/A/xyz/load2d/taut.txt'


#find outputs -name '51-*-ids.tsv' | xargs sort -n -u > list
#find outputs -name '*.filtered' | xargs cat > filtered
#find outputs -name '14-neutralize.log' |xargs cat | grep -v processed > errors
#sort -n  list > list2

zinc-manage -e admin admin catalogs deplete -C 10000 $catname list2
~khtang/ex9/move.csh 

#find outputs -name '33-found.tsv' | xargs sort -n -u > zincids
