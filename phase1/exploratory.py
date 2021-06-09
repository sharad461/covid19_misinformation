import pandas as pd
# import numpy as np
import os, re
from tqdm import tqdm

from config import ExploratoryVars
from helpers import final_in_list, savechunk, makedir


def prepare_data():
    files = os.listdir(ExploratoryVars.input_directory)
    samples_per_output_chunk = ExploratoryVars.output_chunk_size // 10

    makedir(ExploratoryVars.output_directory)
    print("collecting data for exploratory analysis")

    def count_mentions(x):
        return len(re.findall(r"(^|[^@\w])@(\w{1,15})\b", x))

    def count_unique_hashtags(x):
        return len(set(re.findall(r"(^|[^\#\w])\#(\w+)\b", x)))
        # The hashtags column is not very accurate
        # if x is not np.nan:
        #     return len(set(x.split(" ")))

    count = 1
    samples = []
    for file in tqdm(files):
        filename = f"{ExploratoryVars.input_directory}/{file}"

        df = pd.read_csv(filename)

        sample = df[
            [
                "parsed_created_at",
                "text",
                "hashtags",
                "media",
                "user_id",
                "user_verified",
            ]
        ]
        print(sample)
        mentions_count = sample.text.apply(count_mentions).rename(
            "mentions_count"
        )
        unique_hashtags_count = sample.text.apply(
            count_unique_hashtags
        ).rename("unique_hashtags_count")

        dates = pd.to_datetime(sample.parsed_created_at)
        weeks = dates.dt.isocalendar().week
        sample = pd.concat(
            [sample, weeks, mentions_count, unique_hashtags_count], axis=1
        )

        sample = sample.drop(
            [
                "text",
                "hashtags",
                # "media"
            ],
            axis=1,
        )

        samples.append(sample)

        if len(samples) > samples_per_output_chunk or final_in_list(
            file, files
        ):
            savechunk(ExploratoryVars, samples, count)

            count += 1
            samples = []
        del df


def weekly_breakdown():
    files = os.listdir("temp_weekly_data")

    makedir("weekly_data")
    print("loading data to break down into weeks")

    weeks_data = {}
    for file in files:
        filename = f"temp_weekly_data/{file}"

        df = pd.read_csv(filename)

        week_ids = df.week.unique()

        for week in week_ids:
            if week in weeks_data:
                weeks_data[week].append(df[df.week == week])
            else:
                weeks_data[week] = [df[df.week == week]]

        del df

    print("saving weekly data files")
    while weeks_data:
        week = list(weeks_data.keys())[-1]
        wkdata = pd.concat(weeks_data[week])
        wkdata.to_csv(f"weekly_data/week_{week}.csv", index=False)
        del weeks_data[week]
        del wkdata


def weekly_analysis():
    files = os.listdir("weekly_data")

    print("analysing weekly data")

    weeks_data = []
    tweets_count = 0
    tweets_percent_change = "N/A"
    for file in tqdm(files):
        filename = f"weekly_data/{file}"

        df = pd.read_csv(filename)

        prev_tweets_count = tweets_count

        # Total no of tweets in the week
        tweets_count = df.shape[0]

        # Number of unique tweeters
        num_unique_tweeters = df.user_id.unique().shape[0]

        # Percent change
        if prev_tweets_count:
            tweets_percent_change = (
                (tweets_count - prev_tweets_count) / prev_tweets_count
            ) * 100

        # mean number of hashtags
        mean_no_of_hashtags = df.unique_hashtags_count.mean()

        # Grouping data by date
        df["tweet_date"] = df.parsed_created_at.apply(
            lambda x: x.split(" ")[0]
        )

        verified = df[df.user_verified == True]
        unverified = df[df.user_verified == False]

        # Mean number of tweets by verified and unverified users
        mean_tweets_verified_user, mean_tweets_unverified_user = (
            verified.shape[0] / verified.user_id.unique().shape[0],
            unverified.shape[0] / unverified.user_id.unique().shape[0],
        )

        # Handle zero division:

        # try:
        #     mean_tweets_verified_user = verified.shape[0] / verified.user_id.unique().shape[0]
        # except ZeroDivisionError:
        #     mean_tweets_verified_user = 0
        #     print(verified.shape[0], verified.user_id.unique())

        
        # try:
        #     mean_tweets_unverified_user = unverified.shape[0] / unverified.user_id.unique().shape[0]
        # except ZeroDivisionError:
        #     mean_tweets_unverified_user = 0
        #     print(unverified.shape[0], unverified.user_id.unique())

        week_by_date = df.groupby(["tweet_date"]).count()
        week_by_date_date = week_by_date.parsed_created_at

        weeks_data.append(
            [
                os.path.splitext(file)[0][-2:],
                week_by_date_date.min(),
                week_by_date_date.max(),
                week_by_date_date.median(),
                week_by_date_date.mean(),
                num_unique_tweeters,
                tweets_percent_change,
                tweets_count,
                mean_no_of_hashtags,
                mean_tweets_verified_user,
                mean_tweets_unverified_user,
            ]
        )

    data = pd.DataFrame(
        weeks_data,
        columns=[
            "Week number (of year)",
            "Min (Tweets in a day)",
            "Max (Tweets in a day)",
            "Median (Tweets in a day)",
            "Mean (Tweets in a day)",
            "Unique tweeters",
            "Percent change",
            "Tweets count",
            "Mean (Hashtags in a tweet)",
            "Mean (Tweets per verified user)",
            "Mean (Tweets per unverified user)",
        ],
    )

    data.to_csv("exploratory.csv", index=False)


prepare_data()
weekly_breakdown()
weekly_analysis()
