import gc
from sample import sample_dataset
from filter import filter_sampled_data


if __name__ == "__main__":
    sample_dataset()
    gc.collect()    # garbage collector
    filter_sampled_data()
    gc.collect()