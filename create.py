# File: Create
# Description: Creates new python files using a specific layout.
# Author: StrangeParadox
# Version: 0.0.1

# Imports
import os


class Create:
    """
    Creates new python files using a specific layout.
    """

    def __init__(self):
        """
        Initialize the class.
        Set the variables.
        """
        self.file_name = ""
        self.file_description = ""
        self.file_author = "StrangeParadox"
        self.file_version = "0.0.1"
        self.file_imports = []
        self.file_directory = ""
        self.extends = ""

    def ask(self):
        """
        Ask the user some questions about the new file to create.
        """

        self.file_directory = input("Is this file in any subdirectories? Enter the directory path: ")
        self.file_name = input("What is the name of the file? ")
        self.file_description = input("What is the description of the file? ")
        self.file_imports = input("What are the imports of the file? ").split(" ")
        self.extends = input("What does the file extend? ")

    def create(self):
        # Create the path
        path = os.getcwd()

        # Check the file directory to see if anything was passed
        if self.file_directory != "" or self.file_directory != "None":
            # Create the path
            path = os.path.join(path, self.file_directory)
            # Make the dirs if exists_ok
            os.makedirs(path, exist_ok=True)

        # Create the file
        file = open(os.path.join(path, self.file_name + ".py"), "w+")

        # Write the file
        file.write("# File: " + self.file_name.title() + "\n")
        file.write("# Description: " + self.text_to_chunks(self.file_description, 10) + "\n")
        file.write("# Author: " + self.file_author + "\n")
        file.write("# Version: " + self.file_version + "\n")
        file.write("\n")
        file.write("# Imports\n")
        if self.file_imports != [""] or self.file_imports != ["None"]:
            for import_ in self.file_imports:
                if not "#" in import_:
                    # Check if there's a ; in the import
                    if ";" in import_:
                        # Split by the ;
                        name = import_.split(";")

                        # Do a import with an as
                        file.write("import " + name[0] + " as " + name[-1].strip() + "\n")
                    
                    else:
                        file.write("import " + import_.strip() + "\n")

                else:
                    # Split by the #
                    split_import = import_.split("#")

                    # Check if there's a ; in the second part
                    if ";" in split_import[1]:
                        # Split by the ;
                        name = split_import[1].split(";")[-1]

                        # Do a from import with an as
                        file.write("from " + split_import[0].strip() + " import " + split_import[1].strip() + " as " + name.strip() + "\n")
                    
                    else:
                        # Do a from import 
                        file.write("from " + split_import[0].strip() + " import " + split_import[1].strip() + "\n")
        file.write("\n\n")
        if self.extends != "" or self.extends != "None":
            file.write("class " + self.file_name.title() + "(" + self.extends + "):\n")
            file.write("    \"\"\"\n")
            file.write("    " + self.text_to_chunks(self.file_description, 10, False) + "\n")
            file.write("    \"\"\"\n")
            file.write("\n")
            file.write("    def __init__(self, *args, **kwargs):\n")
            file.write("        super().__init__(*args, **kwargs)\n")
        else:
            file.write("class " + self.file_name.title() + ":\n")
            file.write("    \"\"\"\n")
            file.write("    " + self.text_to_chunks(self.file_description, 10, False) + "\n")
            file.write("    \"\"\"\n")
            file.write("\n")
            file.write("    def __init__(self):\n")
            file.write("        pass\n")
        file.write("\n")

        # Close the component file
        file.close()

        # Tell the user the file was created and where it's located
        print("Created file: " + os.path.join(path, self.file_name.lower()) + ".py")

    def text_to_chunks(self, text, chunk_size, default: bool = True) -> str:
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
        return "\n#              ".join(chunks) if default else "\n    ".join(chunks)
    

if __name__ == '__main__':
    # Create the class
    create = Create()

    # Ask the user some questions
    create.ask()

    # Create the file
    create.create()