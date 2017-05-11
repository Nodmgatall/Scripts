export include_string_old=$1
export include_string_new=$2
export dir=$3
export files=$4
perl -e 'print "    Changing includes for: $ENV{'include_string_old'} \/ $ENV{'include_string_new'} in $ENV{dir}*.cpp $ENV{dir}*.hpp \n"'
perl  -p -i  -e "s[\Q$include_string_old\E\b][$include_string_new]g" $dir*.cpp $dir*.hpp $dir*.c $dir*.h Makefile.am


