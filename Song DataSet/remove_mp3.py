import os 

current_path = os.getcwd()

floders = os.listdir(current_path)

for floder in floders:
    if os.path.isdir(floder):
        files = os.listdir(floder)
        for file in files:
            if file.endswith(".mp3"):
                os.remove(floder + "/" + file)
                print("Remove file: " + floder + "/" + file)