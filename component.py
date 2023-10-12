# This file is going to ask a few question about the component
# and then create a component file in the components folder
# With all the information that was given
# The component file will be a .py file
# The component file will also have a class in it
# The class will have the same name as the component

# Imports
import os

# Variables
component_name = ""
component_description = ""
component_author = "StrangeParadox"
component_version = "0.0.1"

# Functions
def ask_questions():
    global component_name
    global component_description
    global component_author
    global component_version

    component_name = input("What is the name of the component? ")
    component_description = input("What is the description of the component? ")
    

def create_component_file():
    global component_name
    global component_description
    global component_author
    global component_version

    # Create the component file
    component_file = open("components/" + component_name.lower() + ".py", "w+")

    # Write the component file
    component_file.write("# Component: " + component_name.title() + "\n")
    component_file.write("# Description: " + text_to_chunks(component_description, 10) + "\n")
    component_file.write("# Author: " + component_author + "\n")
    component_file.write("# Version: " + component_version + "\n")
    component_file.write("\n\n")
    component_file.write("class " + component_name.title() + ":\n")
    component_file.write("    def __init__(self):\n")
    component_file.write("        pass\n")
    component_file.write("\n")

    # Close the component file
    component_file.close()

def text_to_chunks(text, chunk_size) -> str:
    # Split the text into words
    words = text.split(" ")

    # Check if words is empty or <= chunk_size
    if len(words) <= chunk_size:
        return " ".join(words)
    
    # Create the chunks
    chunks = []

    # Loop through the words
    for i in range(0, len(words), chunk_size):
        # Get the chunk
        chunk = words[i:i + chunk_size]

        # Add the chunk to the chunks list
        chunks.append(" ".join(chunk))

    # Return the chunks
    return "\n#              ".join(chunks)


# Create the components folder if it doesn't exist
if not os.path.exists("components"):
    os.makedirs("components", exist_ok=True)

# Main
def main():
    ask_questions()
    create_component_file()

# Run the main function if this file is being run
if __name__ == "__main__":
    main()
