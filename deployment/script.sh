#!/usr/bin/env -f
#$ -clear
#$ -S /bin/sh
#$ -cwd
#$ -o stdout
#$ -e stderr
#$ -P DB-4

export AnException=100
export AnotherException=101


scriptDir="/nfs/ex5/vendoruploads/script/"
userDir=$1
# ${parameter/pattern/string}
idNumber="${2/,/ }"
IFS=',' read -r -a mandatoryCols <<< "$3"
IFS=',' read -r -a optionalCols <<< "$4"
token=$5
historyID=$6
apiUrl="http://0.0.0.0:5001/api/job_logs"

echo "token:$token"
curl $apiUrl
curl -S -i -k -H "Accept: application/json" -H "Content-Type: application/json" -X POST -d '{"history_id":'$historyID', "status":"Job Started", "status_type":1}' -H "Authorization: Bearer $token" $apiUrl

echo "ID NUMBER: $idNumber"

cd "/nfs/ex5/vendoruploads/"
cd "$userDir"

filesInCurrentDir=`ls`

for file in $filesInCurrentDir; do
        if [ -f $file ] ; then
            case $file in
                *.tar.bz2)  tar xjf $file      ;;
                *.tar.gz)   tar xzf $file      ;;
                *.bz2)      bunzip2 $file      ;;
                *.gz)       gunzip $file       ;;
                *.tar)      tar xf $file       ;;
                *.tbz2)     tar xjf $file      ;;
                *.tgz)      tar xzf $file      ;;
                *.zip)      unzip $file        ;;
                *.Z)        uncompress $file   ;;
                *.7z)       7z x $file         ;;
                *.rar)      rar x $file        ;;  # 'rar' must to be installed
            esac
        else
            echo "'$file' is not a valid file"
            curl -S -i -k -H "Accept: application/json" -H "Content-Type: application/json" -X POST -d '{"history_id":'$historyID', "status":"'$file' is not a valid file", "status_type":2}' -H "Authorization: Bearer $token" $apiUrl
        fi
done

# loop through all directories and delete every directory
# after moves all files into the current directory
for d in */; do
        if [ -n "$(ls -A "$d" 2>/dev/null)" ]; then
                cd "$d"; mv * ../; cd ..
        fi
        rm -rf "$d"
done

# replace space in filenames with _
#rename -n 's/_/ /g' *
for f in *\ *; do
        # 2>/dev/null; true - this section ignore mv command error
        mv "$f" "${f// /_}" 2>/dev/null; true
done

#for i in *; do echo "$i"; echo ", "; done;

echo "============================================================================================================================"
echo "Validated Files:"
curl -S -i -k -H "Accept: application/json" -H "Content-Type: application/json" -X POST -d '{"history_id":'$historyID', "status":"Validation Started", "status_type":1}' -H "Authorization: Bearer $token" $apiUrl

newFilesInCurrentDir=`ls`

echo "============================================================================================================================"

for file in *; do
    ext=${file#*.}
    if [ "$ext" == "sdf" ]; then
        curl -S -i -k -H "Accept: application/json" -H "Content-Type: application/json" -X POST -d '{"history_id":'$historyID', "status":"'$file' is validating", "status_type":1}' -H "Authorization: Bearer $token" $apiUrl
        echo "$file: --- START ---"
        echo "============================================================================================================================"
        sed -f $scriptDir/tab2space $file > temp
        mv temp temp.ctrl_m
        sed -f $scriptDir/ctrl_m temp.ctrl_m > "$file"
        /bin/rm temp.ctrl_m

        source ~teague/.virtualenvs/zinc/env.sh
        zincload-sdf --id-field "$idNumber" "$file"
        curl -S -i -k -H "Accept: application/json" -H "Content-Type: application/json" -X POST -d '{"history_id":'$historyID', "status":"'$file' has been validated", "status_type":1}' -H "Authorization: Bearer $token" $apiUrl
        echo "$file: --- END ---"
        echo "============================================================================================================================"
    fi

    if [ "$ext" == "txt" ]; then
        curl -S -i -k -H "Accept: application/json" -H "Content-Type: application/json" -X POST -d '{"history_id":'$historyID', "status":"'$file' is validating", "status_type":1}' -H "Authorization: Bearer $token" $apiUrl
        echo "$file: --- START ---"
        echo "============================================================================================================================"
        counter=0
        delimiter="unknown"
        array=()
        while read -r line
        do
            if [ "$delimiter" == "unknown"  ]; then
                IFS=', ' read -r -a array1 <<< "$line"
                if [ ${#array1[@]} -gt 1  ]; then
                    delimiter=', '
                    array=("${array1[@]}")
                fi
                IFS=' ' read -r -a array2 <<< "$line"
                if [ ${#array2[@]} -gt 1  ]; then
                    delimiter=' '
                    array=("${array2[@]}")
                fi
                IFS=$'\t' read -r -a array3 <<< "$line"
                if [ ${#array3[@]} -gt 1  ]; then
                    delimiter='\t'
                    array=("${array3[@]}")
                fi
            fi
            if [ "$delimiter" == "unknown"  ]; then
                echo "Unknown delimiter error!"
                break
            fi
            ((counter++))
            if [ $counter -eq 100 ]; then
                break
            fi
            if [ $counter -eq 1 ]; then
                duplicate=$(printf '%s\n' "${array[@]}"|awk '!($0 in seen){t=seen[$0];next} 1')
                if [ ${#duplicate} -gt 0 ]; then
                        echo "RED: File title columns are not unique! Please check file."
                        curl -S -i -k -H "Accept: application/json" -H "Content-Type: application/json" -X POST -d '{"history_id":'$historyID', "status":"File title columns are not unique! Please check file.", "status_type":3}' -H "Authorization: Bearer $token" $apiUrl
                        break
                fi
                if [ ${#mandatoryCols[@]} -gt ${#array[@]}  ]; then
                        echo "============================================================================================================================"
                        echo "RED: There must be at least "${#mandatoryCols[@]}" column(s). Please check file."
                        curl -S -i -k -H "Accept: application/json" -H "Content-Type: application/json" -X POST -d '{"history_id":'$historyID', "status":"There must be at least '${#mandatoryCols[@]}' column(s). Please check file.", "status_type":3}' -H "Authorization: Bearer $token" $apiUrl
                        break
                else
                        diff=" ${mandatoryCols[*]} "
                        for item in ${array[@]}; do
                            diff=${diff/ ${item} / }
                        done
                        diff="$(echo -e "${diff}" | sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//')"
                        if [ ${#diff} -gt 0 ]; then
                            echo "RED: Please add mandatory file title column(s): $diff"
                            curl -S -i -k -H "Accept: application/json" -H "Content-Type: application/json" -X POST -d '{"history_id":'$historyID', "status":"Please add mandatory file title column(s): '$diff'", "status_type":2}' -H "Authorization: Bearer $token" $apiUrl
                            break
                        fi

                        diff=" ${optionalCols[*]} "
                        for item in ${array[@]}; do
                            diff=${diff/ ${item} / }
                        done
                        diff="$(echo -e "${diff}" | sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//')"
                        if [ ${#diff} -gt 0 ]; then
                            echo "Warning: Optional column(s) not found: $diff"
                            curl -S -i -k -H "Accept: application/json" -H "Content-Type: application/json" -X POST -d '{"history_id":'$historyID', "status":"Optional column(s) not found: '$diff'", "status_type":2}' -H "Authorization: Bearer $token" $apiUrl
                        fi
                fi
            fi
        done < "$file"
        curl -S -i -k -H "Accept: application/json" -H "Content-Type: application/json" -X POST -d '{"history_id":'$historyID', "status":"'$file' has been validated", "status_type":1}' -H "Authorization: Bearer $token" $apiUrl
        echo "============================================================================================================================"
        echo "$file"": --- END ---"
        echo "============================================================================================================================"
    fi
done

catch || {
    # now you can handle
    case $ex_code in
        $AnException)
            curl -S -i -k -H "Accept: application/json" -H "Content-Type: application/json" -X POST -d '{"history_id":'$historyID', "status":"Exception was thrown", "status_type":3}' -H "Authorization: Bearer $token" $apiUrl
            echo "AnException was thrown"
        ;;
        $AnotherException)
            curl -S -i -k -H "Accept: application/json" -H "Content-Type: application/json" -X POST -d '{"history_id":'$historyID', "status":"AnotherException was thrown", "status_type":3}' -H "Authorization: Bearer $token" $apiUrl
            echo "AnotherException was thrown"
        ;;
        *)
            curl -S -i -k -H "Accept: application/json" -H "Content-Type: application/json" -X POST -d '{"history_id":'$historyID', "status":"An unexpected exception was thrown", "status_type":3}' -H "Authorization: Bearer $token" $apiUrl
            echo "An unexpected exception was thrown"
            throw $ex_code # you can rethrow the "exception" causing the script to exit if not caught
        ;;
    esac
        curl -S -i -k -H "Accept: application/json" -H "Content-Type: application/json" -X POST -d '{"history_id":'$historyID', "status":"Finished with exception", "status_type":4}' -H "Authorization: Bearer $token" $apiUrl
}

curl -S -i -k -H "Accept: application/json" -H "Content-Type: application/json" -X POST -d '{"history_id":'$historyID', "status":"Finished", "status_type":4}' -H "Authorization: Bearer $token" $apiUrl

