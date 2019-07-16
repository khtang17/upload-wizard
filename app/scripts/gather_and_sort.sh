#!/usr/bin/env -f
#$ -clear
#$ -S /bin/sh
#$ -cwd
#$ -o stdout
#$ -e stderr
#$ -P DB-4
# upload_wizard collect results from outputs and sort

cmd="sh gather_and_sort.sh <zinc_load_finished job> "


if [ "$#" -ne 1 ]; then
        echo "Incorrect arguments supplied!!"
        echo "Usage: $cmd"
        exit 1
fi

cd $1

#find outputs -name '51-*-ids.tsv' | xargs sort -n -u > list
#find outputs -name '*.filtered' | xargs cat > filtered
#find outputs -name '14-neutralize.log' |xargs cat | grep -v processed > errors
#sort -n  list > list2

size=$(wc -l list | tr -dc '0-9')
echo "Smiles count : $size"

filtered=$(wc -l filtered | tr -dc '0-9')
echo "Smiles filtered : $filtered"

errors=$(wc -l errors | tr -dc '0-9')
echo "Errors: $errors"


#some lines to call upload-wizard api to write to the 
#curl -S -i -k -H "Accept: application/json" -H "Content-Type: application/json" -X POST -d '{"history_id" : $history_ID, "size" :$size, “filtered”: $filtered, “errors”: $errors}' -H "Authorization: Bearer $token" gimel.compbio.ucsf.edu:5020/api/_write_job_results




