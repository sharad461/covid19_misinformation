# covid19_misinformation

## Setting up and running
Create folder `sample_output` inside `phase1`. Copy all dataset csv files into `sample_output/`. If we are not sampling data from the larger set, copy the files into `filter_output/` folder. Then from `phase1` run 

    python main.py

A few columns are not present in hydrated data, run

    python main.py hydrated

for hydrated data.

`sample.py` reads the dataset and extracts samples and `filter.py` filters tweets based on `tweet_type` (original) and `lang` (en). The functions from `sample.py` are not being used because the data seems to have already been sampled. `visualization.py` has methods that will generate graphs. Currently it only has a method of creating a line graph. `exploratory.py` has methods that prepare the entire data for weekly analysis.

`main.py` imports all these methods and runs them.

After the code has run successfully, the results can be found in these folders and files:
- `figures` folder will have the graphs.
- `reports` folder will have row counts of the files.
- `exploratory.csv` will have detailed stats about the data.

`phase1/config.py` has arguments like `samplepct` which can be changed to customize the operation.

## Requirements
Packages used: seaborn, pandas, matplotlib, tqdm. Will update with the required versions soon, but the latest (as of Jun 2021) should do fine.