import os, gc
from tqdm import tqdm
import pandas as pd

from config import SampleVars, seed
from helpers import final_in_list, makdir, savechunk


def sample_dataset():
    files = os.listdir(SampleVars.input_directory)
    samples_per_output_chunk = SampleVars.output_chunk_size // 18
    makdir(SampleVars.output_directory)

    print("reading dataset files and sampling...")

    count = 1
    samples = []
    for file in tqdm(files):
        df = pd.read_csv(f"{SampleVars.input_directory}/{file}")
        sample = df.sample(frac=SampleVars.samplepct, random_state=seed)

        samples.append(sample)

        if len(samples) > samples_per_output_chunk or final_in_list(
            file, files
        ):
            # Create chunk if samples_per_output_chunk or end of list is reached
            savechunk(SampleVars, samples, count)

            count += 1
            samples = []
        del df
        gc.collect()  # Free up memory after deleting temp variables


if __name__ == "__main__":
    sample_dataset()
