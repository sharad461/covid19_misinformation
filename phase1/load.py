import os, gc
from tqdm import tqdm
import pandas as pd

# Arguments:

directory = "data"  # Directory where all dataset files are
samplepct = 0.1  # Sample percentage, 0.1 for 10 pc
seed = 28982  # use 28982 to reproduce the exact same sampling results
output_chunk_size = 100  # Size of output chunks, in MB
output_prefix = "output"  # Prefix for output file names

# End of Arguments

samples_per_output_chunk = output_chunk_size // 18

samples = []

files = os.listdir(directory)


def final_in_list(obj, list):
    return True if obj is list[-1] else False


count = 1
for file in tqdm(files):
    df = pd.read_csv(f"{directory}/{file}")
    sample = df.sample(frac=samplepct, random_state=seed)

    samples.append(sample)

    if len(samples) > samples_per_output_chunk or final_in_list(file, files):
        chunkname = f"{output_prefix}_%03d.csv" % count
        chunk = pd.concat(samples)

        chunk.to_csv(f"output/{chunkname}")

        count += 1
        samples = []
        del chunk
    del df
    gc.collect()  # Delete temp variables and free memory
