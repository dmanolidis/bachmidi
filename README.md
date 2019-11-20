# bachmidi
## An analysis of Bach's works using midi files

In this analysis, we rank the notes and chords used in the works of J.S Bach. Furthermore, we group works in clusters according to their chords.

The `creat-csv.sh` script converts a *.midi* file to a *.csv* file with the help of `mid2asc` script. The code of `mid2asc` was copied from [this site](http://www.archduke.org/midi/). Only the compiled file is included here.

The midi files should be put in the `midi` folder. The files where downloaded from [The Mutopia Project](https://www.mutopiaproject.org/). Only a few example files are included here.


The `make_all_csv.sh` scripts converts all the *.midi* files to *.csv* files and produces summary files for the notes, the chords and the chord progression of each midi files. In the end, the files are concatanated to summary files.

These summary files are analyzed in the jupyter notebook `process_total_files`. The notebook also uses the `keys.csv` file, which includes the music key of each work of Bach (indexed by their Bach works catalogue number) as scrapped from [Wikipedia](https://en.wikipedia.org/wiki/List_of_compositions_by_Johann_Sebastian_Bach#Works_in_Bach's_catalogues_and_collections).
