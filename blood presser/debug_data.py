import os
import shutil

src = r"C:\Users\JAI SOLAR\Downloads\13100504.csv"
dst = r"d:\blood presser\13100504.csv"

if os.path.exists(src):
    if os.path.isdir(src):
        print(f"Source is a directory. Contents: {os.listdir(src)}")
        try:
            if os.path.exists(dst):
                if os.path.isdir(dst):
                    shutil.rmtree(dst)
                else:
                    os.remove(dst)
            shutil.copytree(src, dst)
            print("Directory copy successful")
        except Exception as e:
            print(f"Error copying directory: {e}")
    else:
        print("Source is a file.")
        try:
            shutil.copy2(src, dst)
            print("File copy successful")
        except Exception as e:
            print(f"Error copying file: {e}")
else:
    print("Source does not exist")
