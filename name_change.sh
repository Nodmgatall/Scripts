

usage() { echo "usage" 1>&2; exit 1; }

change_file_endings()
{
change_count=0
for file in $3*.$1 ; do
    echo "renamed "$file" to "${file%.$1}.$2""
    $4 mv "$file" "${file%.$1}.$2"
    echo "changed includes"
    ./include_change.pl ${file} ${file%.$1}.$2 
    change_count=$((${change_count} + 1 ))
done
echo "changed ${change_count} files in folder $3"
}
# sets option so that if the patterns are not found it will not be used as literal string
shopt -s nullglob
recursive=false
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
if [ ${only_subdirs} == false ] 
then
    change_file_endings $1 $2 "" ${git}
fi
if [ ${recursive} == true ]
then
    for dir in */ ; do
        echo ${dir}
        change_file_endings $1 $2 ${dir} ${git}
    done
fi
##clipping folder
#for file in clipping/*.c
#do
#    git mv -- "$file" "${file%.c}.cpp"
#done
#
#for file in clipping/*.h
#do
#    git mv -- "$file" "${file%.h}.hpp"
#done 
#
##kdtree folder
#for file in kdtreelib/*.c
#do
#    git mv -- "$file" "${file%.c}.cpp"
#done
#
#for file in kdtreelib/*.h
#do
#    git mv -- "$file" "${file%.h}.hpp"
#done 
#
##json folder
#for file in json/*.c
#do
#    git mv -- "$file" "${file%.c}.cpp"
#done
#
#for file in json/*.h
#do
#    git mv -- "$file" "${file%.h}.hpp"
#done 
#
