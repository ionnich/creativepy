import os

# Get the current directory
current_dir = os.getcwd()

# Get a list of all files in the current directory
files = os.listdir(current_dir)

# filter for files containing "campaign_names" in the name
campaign_names = [f for f in files if 'campaign_names' in f]

# Filter the list to only include only the first campaign_name
text_files = [f for f in campaign_names if f.endswith('.txt')]

# Get the path to the text file
path_to_file = os.path.join(current_dir, text_files[0])

# Open the text file for reading
with open(path_to_file, "r") as file:

    # Loop through each line in the file
    for line in file:
        if line != " " or line != "\n":
            line = line.strip()
            os.makedirs(line)
        # Create a directory with the name of the current line