import glob
import os

if __name__=="__main__":
    filenames=[]
    for filename in glob.glob("/home/adelina/cern/analysis/*.deps", recursive=False):
        if "raw"  in filename:
            filenameChanged=filename.replace("raw", "")
            filenameChanged=filenameChanged.replace(".deps","raw.deps")
            os.rename(filename, filenameChanged)
