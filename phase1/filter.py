import os
from tqdm import tqdm
import pandas as pd

from config import FilterVars
from helpers import makedir, final_in_list, savechunk, generate_report


def filter_sampled_data():
    files = os.listdir(FilterVars.input_directory)

    # Around 83000 tweets are filtered out from every sample chunk of 150000
    samples_per_output_chunk = FilterVars.output_chunk_size // 80000

    makedir(FilterVars.output_directory)

    print("filtering sampled data...")

    count = 1
    samples, numrows, numrows_filtered = [], {}, {}
    for file in tqdm(files):
        filename = f"{FilterVars.input_directory}/{file}"

        df = pd.read_csv(filename)
        numrows[filename] = df.shape[0]

        sample = df[(df.lang == "en") & (df.tweet_type == "original")]

        samples.append(sample)

        if len(samples) > samples_per_output_chunk or final_in_list(
            file, files
        ):
            # Create chunk if samples_per_output_chunk or end of list is reached
            name, count = savechunk(FilterVars, samples, count)

            numrows_filtered[f"filter_output/{name}"] = count

            count += 1
            samples = []
        del df

    generate_report(numrows, "sampled")
    generate_report(numrows_filtered, "filtered")


if __name__ == "__main__":
    filter_sampled_data()
