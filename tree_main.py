
from handlers.reader import get_files

def main(source_directory, destination_directory):
    files = get_files(source_directory, destination_directory, fresh_build=True)



if __name__ == "__main__":
    
    main()