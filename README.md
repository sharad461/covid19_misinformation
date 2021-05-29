# covid19_misinformation

## Setting up
Create folder `data` inside folder `phase1` and copy all dataset csv files into `data/`. Then from `phase1` run 

`python main.py` 

Invididually, `sample.py` reads the dataset and extracts samples and `filter.py` filters tweets based on `tweet_type` (original) and `lang` (en).

`phase1/config.py` has arguments like `samplepct` which can be changed to customize the operation.