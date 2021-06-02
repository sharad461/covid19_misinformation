import os
import time
import pandas as pd


def final_in_list(obj, list):
    return True if obj is list[-1] else False


def makedir(path):
    if not os.path.isdir(path):
        os.makedirs(path)


def savechunk(varsclass, samples, count, index=False):
    chunkname = f"{varsclass.output_prefix}_%03d.csv" % count
    chunk = pd.concat(samples)

    chunk.to_csv(f"{varsclass.output_directory}/{chunkname}", index=index)

    del chunk


def generate_report(numrowsdict, processtype):
    makedir("reports")

    subfolder = time.strftime("reports/%Y%m%d")
    makedir(subfolder)

    filename = f"{subfolder}/{processtype}.csv"

    file_rows = pd.DataFrame(
        numrowsdict.items(), columns=["Filepath", "No of tweets"]
    )
    file_rows.to_csv(filename, index=False)
