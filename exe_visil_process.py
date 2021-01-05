import sys
import subprocess

if __name__ == "__main__":
    folder_name = ""

    for arg in sys.argv:
        if "folder=" in arg:
            folder_name = arg.split("folder=")[1]
    
    if folder_name == "":
        print("please check arg \"folder=(foldername)\" exist")
        exit(0)

    with open('command.txt', 'r') as f:
        commands = f.readlines()
        for command in commands:
            command = command.replace('$(queries_path)', 'upload/' + folder_name)
            command = command.replace('$(database_path)', 'database')
            command = command.replace('$(results)', folder_name)

            print('Start command:')
            print('\t ' + command)
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
            process.wait()
            print('End command')