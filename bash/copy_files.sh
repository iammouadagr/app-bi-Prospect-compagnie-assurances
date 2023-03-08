#!/bin/bash

# Specify the source folder
src_folder=$1

input="input"
#file extension
extension=$2

echo $HADOOP_HOME
# Check if the variable is not null
if [ -n "$src_folder" ] && [ -n "$extension" ]; then
    #remove all file with the giving extension
    $HADOOP_HOME/bin/hdfs dfs -rm -r $input
    $HADOOP_HOME/bin/hdfs dfs -mkdir $input
    $HADOOP_HOME/bin/hdfs dfs -put $src_folder/*.$extension $input

    $HADOOP_HOME/bin/hdfs dfs -ls $input

    echo "Copy terminé"

else
    # If the condition is false, print a different message
    echo "The variable is null."
fi





