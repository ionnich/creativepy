import os

# Get the current directory
current_dir = os.getcwd()

# Get a list of all files in the current directory
files = os.listdir(current_dir)

# Filter the list to only include text files
text_files = [f for f in files if f.endswith(".txt")]

# select the file named folder_names.txt
folder_names = [f for f in text_files if f == "folder_names.txt"]

# Get the path to the text file
path_to_file = os.path.join(current_dir, folder_names[0])

# Open the text file for reading
with open(path_to_file, "r") as file:

    # Loop through each line in the file
    for line in file:
        if line != " " or line != "\n":
            line = line.strip()
            os.makedirs(line)
        # Create a directory with the name of the current line