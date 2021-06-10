# from sample import sample_dataset
from filter import filter_sampled_data
from visualization import prepare_viz_data, lineplot_tweets_daily
from exploratory import prepare_weekly_data, weekly_breakdown, weekly_analysis


if __name__ == "__main__":
    # sample_dataset()

    '''
    Place all your csv files inside data/ folder and run
    '''

    filter_sampled_data()

    prepare_viz_data()
    lineplot_tweets_daily()
    
    prepare_weekly_data()
    weekly_breakdown()
    weekly_analysis()
