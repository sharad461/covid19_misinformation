import os, gc
from tqdm import tqdm
import pandas as pd

from config import FilterVars
from helpers import makdir, final_in_list, savechunk


def filter_sampled_data():
    files = os.listdir(FilterVars.input_directory)

    # Around 83000 tweets are filtered out from every sample chunk
    samples_per_output_chunk = FilterVars.output_chunk_size // 80000

    makdir(FilterVars.output_directory)

    print("filtering sampled data...")

    count = 1
    samples = []
    for file in tqdm(files):
        df = pd.read_csv(f"{FilterVars.input_directory}/{file}")
        sample = df[(df.lang == "en") & (df.tweet_type == "original")]

        samples.append(sample)

        if len(samples) > samples_per_output_chunk or final_in_list(
            file, files
        ):
            # Create chunk if samples_per_output_chunk or end of list is reached
            savechunk(FilterVars, samples, count)

            count += 1
            samples = []
        del df
        gc.collect()  # Free up memory after deleting temp variables


if __name__ == "__main__":
    filter_sampled_data()
