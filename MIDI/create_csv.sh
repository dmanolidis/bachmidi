#!/bin/bash

INPUT_FILENAME=$1
echo "Processing file ${INPUT_FILENAME}"

# Get the suffix of the input filename to be used in the output filename
FILE_SUFFIX=$( echo $INPUT_FILENAME | cut -d"/" -f3 | cut -d"." -f1)
OUTPUT_FILENAME="${FILE_SUFFIX}.csv"

# Convert the .midi input file to a .csv file and keep only the relevant fields
./mid2asc -c $INPUT_FILENAME | grep "NT" | awk '{print $2","$4","$6", \
			"$8","$10","$12","$13}' > $OUTPUT_FILENAME
