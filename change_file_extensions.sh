usage() { echo "usage" 1>&2; exit 1; }

change_file_endings()
{
    echo "renamed $1 to $2"
    $3 mv -- "$1" "$2"
}

# sets option so that if the patterns are not found it will not be used as literal string
shopt -s nullglob
recursive=false""
git=""
only_subdirs=false
while getopts "rgi" o; do
    case "${o}" in
        r)
            recursive=true
            echo "recursive selected"
            ;;
        g)
            git="git"
            echo "git mv used"
            ;;
        i)
            only_subdirs=true;
            recursive=true;
            echo "only subdirs"
            ;;
    esac
done

shift $((OPTIND -1))
export old_name_extension=$1
export new_name_extension=$2
echo ${old_name_extension} ${new_name_extension}
if [ ${only_subdirs} == false ] 
then
    echo "=============starting============="
    change_count=0
    for file in *.${old_name_extension} ; do
        export old_name=${file}
        export new_name="${file%.${old_name_extension}}.${new_name_extension}"
         echo "renamed ${old_name} to ${new_name}" ""
        ${git} mv "${old_name}" "${new_name}" 
        ./name_change.sh ${old_name} ${new_name} ""
        change_count=$((${change_count} + 1 ))
    done
    echo "  changed ${change_count} files in folder "
fi
if [ ${recursive} == true ]
then
    echo "========starting recursive========"
    current_dir=""
    for dir in */ ; do
        export current_dir=$dir
        echo ${current_dir}
        for file in ${dir}*.${old_name_extension} ; do
            export old_name=${file}
            export new_name="${file%.${old_name_extension}}.${new_name_extension}"
            echo "renamed ${old_name} to ${new_name}"
            ${git} mv "${old_name}" "${new_name}"       
            echo ${current_dir}
            ./name_change.sh "${old_name##*/}" "${new_name##*/}" ${current_dir}
            ./name_change.sh ${old_name} ${new_name} "" 

            change_count=$((${change_count} + 1 ))
        done
    echo "  changed ${change_count} files in folder ${dir}"
    done
fi

