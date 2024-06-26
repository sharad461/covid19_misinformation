import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import os, time
from tqdm import tqdm
from collections import Counter

from config import VizVars, charts_folder
from helpers import final_in_list, makedir, savechunk, generate_report

sns.set_theme(style="darkgrid")


def prepare_viz_data(args):
    files = os.listdir(VizVars.input_directory)
    samples_per_output_chunk = VizVars.output_chunk_size // 2
    makedir(VizVars.output_directory)
    print("profiling filtered data for visualization")

    datecol = (
        ["created_at", "%a %b %d %H:%M:%S %z %Y"]
        if args["hydrated"]
        else ["parsed_created_at", None]
    )

    count = 1
    samples, numrows = [], {}
    for file in tqdm(files):
        filename = f"{VizVars.input_directory}/{file}"

        df = pd.read_csv(filename)
        numrows[filename] = df.shape[0]

        dates = pd.to_datetime(df[datecol[0]], format=datecol[1])
        dates = dates.apply(lambda x: str(x).split(" ")[0]).rename(
            "created_at"
        )

        samples.append(dates)

        if len(samples) > samples_per_output_chunk or final_in_list(
            file, files
        ):
            # Create chunk if samples_per_output_chunk or end of list is reached
            savechunk(VizVars, samples, count)

            count += 1
            samples = []
        del df

    generate_report(numrows, "filtered")


def lineplot_tweets_daily(save=True):
    counter = Counter()

    print("counting no of tweets over days")
    for file in tqdm(os.listdir(VizVars.output_directory)):
        filename = f"{VizVars.output_directory}/{file}"

        df = pd.read_csv(filename)

        chunk = Counter(df.created_at.T.values.tolist())
        counter += chunk

        del df

    counter = sorted(counter.items())

    tweets = pd.DataFrame(counter, columns=["days", "no of tweets"])

    plt.figure(figsize=(12, 8))

    line = sns.lineplot(
        data=tweets,
        x="days",
        y="no of tweets",
        linewidth=1,
    )

    days = tweets.days

    # Retain label if it is the fifteeth of the month, otherwise empty
    xlabels = days.apply(lambda x: "" if "-15" not in x else x[:-3])

    line.set_xticklabels(xlabels)
    line.set_xlabel("months")

    if save:
        makedir(charts_folder)
        fig = line.get_figure()
        figname = time.strftime("lineplot_tweets_daily_%Y%m%d_%H%M%S.png")
        fig.savefig(f"{charts_folder}/{figname}")

    plt.show()


def lineplots_exploratory_data(save=True):
    df = pd.read_csv("exploratory.csv")

    makedir(charts_folder)

    subfolder = time.strftime("%Y%m%d")
    makedir(f"{charts_folder}/{subfolder}")

    def saveplot(plot, filename):
        fig = plot.get_figure()
        fig.savefig(f"{charts_folder}/{subfolder}/{filename}")

    percent_change = df[["Index", "Percent change"]]
    min_max = df[
        [
            "Index",
            "Min (Tweets in a day)",
            "Max (Tweets in a day)",
            "Median (Tweets in a day)",
            "Mean (Tweets in a day)",
        ]
    ]
    tweet_numbers = df[
        [
            "Index",
            "Unique tweeters",
            "Tweets count",
        ]
    ]
    hashtags_media = df[
        [
            "Index",
            "Mean (Tweets with link or media)",
            "Mean (Hashtags in a tweet)",
        ]
    ]
    verified_unverified = df[
        [
            "Index",
            "Mean (Tweets per verified user)",
            "Mean (Tweets per unverified user)",
        ]
    ]

    data = [
        min_max,
        hashtags_media,
        tweet_numbers,
        verified_unverified,
    ]

    f, axes = plt.subplots(2, 2, figsize=(14, 14))

    xlabels = []
    for i, x in enumerate(list(df["Month"])):
        if (i + 2) % 4 == 0:
            xlabels.append(x)
        else:
            xlabels.append("")

    for i, d in enumerate(data):
        line = sns.lineplot(
            x="Index",
            y="no of tweets",
            hue="type",
            data=pd.melt(
                d,
                ["Index"],
                var_name="type",
                value_name="no of tweets",
            ),
            ax=axes.flat[i],
        )

        line.set_xlabel("months")
        line.set_xticklabels(xlabels)

    plt.figure()

    line = sns.lineplot(
        x="Index",
        y="Percent change",
        data=percent_change,
    )

    line.set_xlabel("months")
    line.set_xticklabels(xlabels)

    if save:
        saveplot(f, time.strftime("lineplots_%Y%m%d_%H%M%S.png"))
        saveplot(line, time.strftime("lineplot_pc_change_%Y%m%d_%H%M%S.png"))

    plt.show()


if __name__ == "__main__":
    prepare_viz_data()
    lineplot_tweets_daily()
    # lineplots_exploratory_data()
