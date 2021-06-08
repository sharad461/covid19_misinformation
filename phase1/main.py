from sample import sample_dataset
from filter import filter_sampled_data
from visualization import prepare_viz_data, lineplot_tweets_daily


if __name__ == "__main__":
    # sample_dataset()
    filter_sampled_data()
    prepare_viz_data()
    lineplot_tweets_daily()