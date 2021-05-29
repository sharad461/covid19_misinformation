import os
import pandas as pd


def final_in_list(obj, list):
    return True if obj is list[-1] else False


def makdir(path):
    if not os.path.isdir(path):
        os.makedirs(path)


def savechunk(varsclass, samples, count):
    chunkname = f"{varsclass.output_prefix}_%03d.csv" % count
    chunk = pd.concat(samples)

    chunk.to_csv(f"{varsclass.output_directory}/{chunkname}", index=False)

    del chunk
