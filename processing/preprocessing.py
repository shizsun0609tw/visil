from os import listdir
import cv2
import sys

# command example: python processing/preprocessing.py queries_path=upload/12_15_15_19_49 database_path=database

err_file_name = "errfile.txt"

queries_path = "queries/"
database_path = "database/"

queries_name = "queries.txt"
database_name = "database.txt"

def write_path(path, filename):
    files = listdir(path)
    err_files = []

    with open(filename, 'w') as f:
        for file in files:
            video = cv2.VideoCapture(path + file)

            if video.isOpened() == False:
                err_files.append(path + file)
                video.release()
                continue
            
            ret, frame = video.read()
            if len(frame) == 0:
                err_files.append(path + file)
                video.release()
                continue

            f.write(file.replace(".mp4", "") + " " + path + file + '\n')
            video.release()

    return err_files

def write_err(err_files, filename):
    with open(filename, 'w') as f:
        for err_file in err_files:
            f.write(err_file + '\n')

def parse_arg(queries_path, database_path):
    for arg in sys.argv:
        if 'queries_path=' in arg:
            queries_path = arg.split('queries_path=')[1] + '/'
        elif 'database_path=' in arg:
            database_path = arg.split('database_path=')[1] + '/'

    return queries_path, database_path

err_files = []

queries_path, database_path = parse_arg(queries_path, database_path)

err_files.extend(write_path(queries_path, queries_name))
err_files.extend(write_path(database_path, database_name))

write_err(err_files, err_file_name)