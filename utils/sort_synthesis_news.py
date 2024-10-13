
# import required module
import os, shutil


def sort_synthesis_news(directory = 'data/data_collection/'): 
    files_to_move = []
    count = 0
    # iterate over files in
    # that directory
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        # checking if it is a file
        if os.path.isfile(f):
            if '2024' in f and f.endswith('.log'):
                count += 1
                files_to_move.append(f)

    for file_path in files_to_move:
        new_file_path = file_path.replace("data_collection/", "data_collection/processed/")
        shutil.move(file_path, new_file_path)
        print(file_path, ' has been moved to ', new_file_path)


    # assign directory
    directory = 'data/'
    files_to_move = []

    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        # checking if it is a file
        if os.path.isfile(f):
            if 'news_synthesis_2024' in f and f.endswith('.json'):
                count += 1
                files_to_move.append(f)

    for file_path in files_to_move:
        new_file_path = file_path.replace("data/", "data/data_collection/processed/")
        shutil.move(file_path, new_file_path)
        print(file_path, ' has been moved to ', new_file_path)

    print("Finished, " + str(count) + " files have been moved.")



if __name__ == "__main__":
    sort_synthesis_news()