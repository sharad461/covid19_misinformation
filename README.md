# covid19_misinformation

## Setting up and running
Create folder `data` inside folder `phase1`. Copy all dataset csv files into `data/`. Then from `phase1` run 

    python main.py

`sample.py` reads the dataset and extracts samples and `filter.py` filters tweets based on `tweet_type` (original) and `lang` (en).

`phase1/config.py` has arguments like `samplepct` which can be changed to customize the operation.