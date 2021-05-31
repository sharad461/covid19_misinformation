import os
from tqdm import tqdm
import pandas as pd

from config import SampleVars, seed
from helpers import final_in_list, makedir, savechunk, generate_report


def sample_dataset():
    files = os.listdir(SampleVars.input_directory)

    # Supposing 10 pc of every csv file is 18 MB (csv is 180MB)
    samples_per_output_chunk = SampleVars.output_chunk_size // 18
    
    makedir(SampleVars.output_directory)

    print("reading dataset files and sampling...")

    count = 1
    samples, numrows = [], {}
    for file in tqdm(files):
        filename = f"{SampleVars.input_directory}/{file}"

        df = pd.read_csv(filename)
        numrows[filename] = df.shape[0]

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

    generate_report(numrows, "unprocessed")


if __name__ == "__main__":
    sample_dataset()
