#!/usr/bin/perl
$old_name = ${ARGV[0};
$new_name = ${ARGV[1]};
print "perl -pi -e 's/#include(\s+)\"${old_name}\"/#include$1\"${new_name}\"/'  *.hpp *.cpp";
#perl -pi -e 's/#include(\s+)"${include_file_name}.${old_ending}"/#include$1"${include_file_name}.${new_ending}"/'  *.hpp *.cpp
