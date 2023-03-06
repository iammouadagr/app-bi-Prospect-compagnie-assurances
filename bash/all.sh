#!/bin/bash
jar="jar.sh"

# ./copy_files.sh /home/tlamo/Desktop/java/input/ txt
# The second script to be called
copy_files="copy_files.sh"

# Specify the source folder
src_folder=$1


#file extension
extension=$2
# Call the first script
bash $jar
if [ $? -eq 0 ]; then
    # Call the second script
    echo "file one ok"
    
    bash $copy_files $src_folder $extension
else
    # If the first script failed, print an error message
    echo "Error: The first script ($script1) failed."
    exit 1
fi