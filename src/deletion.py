import os
# Chemin vers le dossier contenant les fichiers PNG



def create_directory(directory):
    # create the directory if it does not exist
    if not os.path.exists(directory):
        os.makedirs(directory)
        print("Directory created")
    else:
        print("Directory already exists")

def remove_directory(directory,extension):
    if os.path.exists(directory):
        deletion_file(directory,extension)
        os.rmdir(directory)
        print("Directory removed")
    else:
        print("Directory does not exist")


def deletion_file(directory,extension):
    if os.path.exists(directory):
        for filename in os.listdir(directory):
            # Vérifie si le fichier est un fichier PNG
            if filename.endswith(extension) and filename != "base_prospect.csv":
                # Construit le chemin complet du fichier
                file_path = os.path.join(directory, filename)
                # Supprime le fichier
                os.remove(file_path)

directory = "../data/"
if __name__ == "__main__" :
    deletion_file("../data","csv")
    remove_directory("../fig/analyse_descriptive",".png") 
    remove_directory("../fig","png") 
    create_directory("../fig")  
    create_directory("../fig/analyse_descriptive")  
    
    


