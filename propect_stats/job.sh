#!/bin/bash 
generate_file="part-r-00000"
job_name=$1
rm *.class
$HADOOP_HOME/bin/hadoop com.sun.tools.javac.Main  $job_name.java
rm *.jar
jar cf $job_name.jar  $job_name*.class
$HADOOP_HOME/bin/hdfs dfs -rm -r  output
$HADOOP_HOME/bin/hadoop jar $job_name.jar  $job_name input output
rm $generate_file
$HADOOP_HOME/bin/hadoop fs -get output/$generate_file .

echo "file $generate_file"
