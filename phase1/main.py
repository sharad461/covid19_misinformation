# from sample import sample_dataset
from filter import filter_sampled_data
from visualization import (
    prepare_viz_data,
    lineplot_tweets_daily,
    lineplots_exploratory_data,
)
from exploratory import prepare_weekly_data, weekly_breakdown, weekly_analysis


if __name__ == "__main__":
    # Phase 1

    # sample_dataset()
    filter_sampled_data()

    prepare_viz_data()
    lineplot_tweets_daily()

    prepare_weekly_data()
    weekly_breakdown()
    weekly_analysis()
    lineplots_exploratory_data()

    # End of Phase 1
