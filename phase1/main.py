# from sample import sample_dataset
# from filter import filter_sampled_data
from visualization import (
    prepare_viz_data,
    lineplot_tweets_daily,
    lineplots_exploratory_data,
)
from exploratory import prepare_weekly_data, weekly_breakdown, weekly_analysis
import sys


if __name__ == "__main__":
    hydrated = False

    try:
        if sys.argv[1] == "hydrated":
            hydrated = True
    except Exception:
        pass
    
    args = {
        "hydrated": hydrated
    }

    print(f"Hydrated {args['hydrated']}")

    # Phase 1

    # sample_dataset()
    # filter_sampled_data()

    prepare_viz_data(args)
    lineplot_tweets_daily()

    prepare_weekly_data(args)
    weekly_breakdown()
    weekly_analysis(args)
    lineplots_exploratory_data()

    # End of Phase 1
