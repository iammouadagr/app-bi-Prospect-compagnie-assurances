from clean_dataset import clean_supervised,clean_unsupervised

menu_options = {
    1: 'Analyse descriptive',
    2: 'Option 2',
    3: 'Option 3',
    4: 'Exit',
}

def print_menu():
    for key in menu_options.keys():
        print (key, '--', menu_options[key] )


def data_exploration():
    clean_dataset_for_supervised_classification = clean_supervised()
    clean_dataset_for_unsupervised_classification = clean_unsupervised()






if __name__ == "__main__" :
    while (True):
        print_menu()
        option = ''
        try:
            option = int(input('Enter your choice: '))
        except:
            print('Wrong input. Please enter a number ...')
        # Check what choice was entered and act accordingly
        if option == 1:
            data_exploration()
        elif option == 2:
            print('Thanks message before exiting')
            exit()
