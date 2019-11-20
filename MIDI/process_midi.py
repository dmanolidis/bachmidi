import pandas as pd
import numpy as np
import re
import sys


def create_dataframe(filename):
    """
    This function creates the initial dataframe from the raw .csv file, as created by mid2asc
    :param filename: The name of the file
    :return: A dataframe
    """

    # The .csv contains seven fields
    df = pd.read_csv(filename, names=["time", "bar",
                                      "time_bar", "track", "channel", "note", "end_time"])

    # Making sure the columns are string columns before eval
    df[["time", "time_bar", "end_time"]] = df[["time", "time_bar", "end_time"]].astype("str")

    # The "time" column is time the note started playing as the number of quarter notes from
    # the beginning of the track. The column is in a fraction form. We use eval to convert
    # it to a float. Multiplying by 16 we can convert to sixty-fourth notes.
    # Since sixty-fourth notes is the lowest note value the number should always be an integer.
    df["int_time"] = (df.time.apply(eval)*16).astype("int")

    # Removing extra ")" characters
    df["int_time_bar"] = df.time_bar.apply(lambda x: x.replace(")", ""))

    # The "time_bar" column is time the note started playing as the number of quarter notes from
    # the beginning of the bar this note belongs to. The column is in a fraction form.
    # We use eval to convert it to a float. Multiplying by 16 we can convert to sixty-fourth notes.
    # Since sixty-fourth notes is the lowest note value the number should always be an integer.
    df["int_time_bar"] = (df.int_time_bar.apply(eval)*16).astype("int")

    # The "end_time" column is time the note stopped playing as the number of quarter notes from
    # the time the note started playing, shown in the "time" column. The column is in a
    # fraction form. We use eval to convert it to a float. Multiplying by 16 we can convert to
    # sixty-fourth notes. Since sixty-fourth notes is the lowest note value the number should
    # always be an integer.
    df["int_end_time"] = (df.end_time.apply(eval)*16).astype("int")

    # The duration of a note is the "end_time" as defined above
    df["dur"] = df["int_end_time"]
    # We convert the "end_time" to be the time the note stopped playing counting from the
    # beginning of the track
    df["int_end_time"] = df.int_end_time + df.int_time

    return df


def create_arrays(raw_df):
    """
    This function extracts the notes array, the start time array and the end time array
    from the dataframe
    :param raw_df: The dataframe containing all the necessary columns
    :return: Three numpy arrays
    """

    # Extracting the arrays
    notes_array = np.array(raw_df["note"])
    start_array = np.array(raw_df["int_time"])
    end_array = np.array(raw_df["int_end_time"])

    return notes_array, start_array, end_array


def create_notes_dic(raw_df):
    """
    This functions creates a dictionary with keys the time elapsed since the beginning of the track
    in sixty-four notes intervals. The values of each key are lists of the notes that are played
    during that time of the track.
    :param raw_df: The initial dataframe
    :return: A dictionary as described above
    """

    # First we extract the relevant columns from the initial dataframe
    notes_array, start_array, end_array = create_arrays(raw_df)
    n = end_array[-1]
    nums_dic = {}

    # A note is included in a key's list, if the key (the sixty-fourth note since the beginning
    # of the track) is within the interval the note is played (end_time - start_time)
    for num in range(0, n+1):
        common_indexes = np.logical_and(end_array > num, start_array <= num)
        nums_dic[num] = [notes_array[common_indexes]]

    return nums_dic


def convert_notes(note_list):
    """
    This function converts a list of notes with pitch indicators (such as ' or -) to a list of notes
    with no indication of pitch. Only unique notes are included in the final list.
    :param note_list: The initial list of notes
    :return: The converted list of notes as a tuple
    """

    conv_set = set()
    for item in note_list:
        note = re.sub('[\'-]+', '', item)
        conv_set.add(note)
    conv_list = list(conv_set)
    conv_list.sort()

    return tuple(conv_list)


def create_final_df(df_dic):
    """
    This function creates a dataframe using the dictionary created by the create_notes_dic function.
    Also, the "notes" column is converted using the convert_notes function
    :param df_dic: A dictionary which is the output of the create_notes_dic function
    :return: The final dataframe to be used by export_csv functions
    """
    ndf = pd.DataFrame.from_dict(df_dic, orient='index', columns=["notes"])
    ndf["converted_notes"] = ndf.notes.apply(lambda x: convert_notes(x))
    ndf["chords"] = ndf["converted_notes"].apply(" ".join)

    return ndf


def export_notes_csv(df, filename, outfilename):
    """
    This function exports a .csv file with the notes' counts.
    :param df: An already processed dataframe
    :param filename: The filename of the input file of the script
    :param outfilename: The filename of the exported .csv file

    """
    df["notes_clean"] = df.note.apply(lambda x: re.sub('[\'-]+', '', x))
    notes_counts_df = (df.groupby("notes_clean").sum()["dur"] / 16).sort_values(
        ascending=False).reset_index()

    notes_counts_df["title"] = filename
    notes_counts_df.to_csv(outfilename, sep=";", index=False, header=False)


def export_chords_csv(df, filename, outfilename):
    """
    This function exports a .csv file with the chords' counts.
    :param df: An already processed dataframe
    :param filename: The filename of the input file of the script
    :param outfilename: The filename of the exported .csv file

    """
    comb_counts_df = (df.groupby('chords')['notes'].count() / 16).sort_values(
        ascending=False).reset_index()
    comb_counts_df["title"] = filename
    comb_counts_df.to_csv(outfilename, sep=";", index=False, header=False)


def export_chords_string(df, filename, outfilename):
    """
    This function exports a .csv file with the a string of the progression of chords.
    The file is formatted as .csv with the first field being the input filename and the second field
    being the string
    :param df: An already processed dataframe
    :param filename: The filename of the input file of the script
    :param outfilename: The filename of the exported .csv file

    """
    mask = df.converted_notes != df.converted_notes.shift()
    progr_df = df[mask].copy()
    progr_df["word_chords"] = progr_df["converted_notes"].apply("".join)
    string = " ".join(progr_df["word_chords"]).strip()
    dic = {'file': filename, 'string': string}
    fin_df = pd.DataFrame(dic, index=[0])
    fin_df.to_csv(outfilename, sep=";", index=False, header=False)



########################## MAIN ##########################


# Get the filename
file = sys.argv[1]

# Create the output file names for notes, chords and chords string
notes_outfile = "./notes/notes_" + file
chords_outfile = "./chords/chords_" + file
chords_string_file = "./strings/strings_" + file


####### Initial processing #######

# Create the initial dataframe
initial_df = create_dataframe(file)

# Create the notes dictionary
notes_dic = create_notes_dic(initial_df)

# Create the final dataframe
final_df = create_final_df(notes_dic)


####### Export the files #######

# Create the notes file
export_notes_csv(initial_df, file, notes_outfile)
# Create the chords file
export_chords_csv(final_df, file, chords_outfile)
# Create the chords string file
export_chords_string(final_df, file, chords_string_file)