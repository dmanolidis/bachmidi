#!/bin/bash

# Creating the directories, if they don't exist
mkdir -p chords
mkdir -p notes
mkdir -p csv
mkdir -p strings


# Process the .midi files to produce the related .csv files
for FILE in `ls ./midi/*.mid`
do
	echo "Processing file ${FILE}"
	./create_csv.sh $FILE
done


# Process the .csv files produced in the previous step through a python script
# The output is three files with the count of notes, the count of chords and a 
# document with the progression of the chords as a string of words 
for PYTHON_INPUT_FILE in `ls *.csv`
do
	echo "Creating summary files of ${PYTHON_INPUT_FILE}"
	python process_midi.py $PYTHON_INPUT_FILE
done


# Archive .csv files
echo "Arching .csv files..."
cp *.csv ./csv/
rm *.csv


# Produce the total files for chords, notes and chord strings
echo "Concatenating files..."
cat ./chords/*.csv > chords_total.csv
cat ./notes/*.csv > notes_total.csv
cat ./strings/*.csv > strings_total.csv
