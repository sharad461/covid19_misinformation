import pandas as pd
import os, re
from tqdm import tqdm

from config import ExploratoryVars
from helpers import final_in_list, savechunk, makedir
from visualization import lineplots_exploratory_data


months = ["Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def prepare_weekly_data(args):
    files = os.listdir(ExploratoryVars.input_directory)
    samples_per_output_chunk = ExploratoryVars.output_chunk_size // 10

    makedir(ExploratoryVars.output_directory)
    makedir("tweet_ids")

    print("collecting data for exploratory analysis")

    datecol = (
        ["created_at", "%a %b %d %H:%M:%S %z %Y"]
        if args["hydrated"]
        else ["parsed_created_at", None]
    )

    def count_mentions(x):
        return len(re.findall(r"(^|[^@\w])@(\w{1,15})\b", x))

    def count_unique_hashtags(x):
        return len(set(re.findall(r"(^|[^\#\w])\#(\w+)\b", x)))
        # The hashtags column is not very accurate so we will
        # search for hashtags in the texts themselves
        # if x is not np.nan:
        #     return len(set(x.split(" ")))

    count = 1
    samples = []
    for i, file in enumerate(tqdm(files)):
        filename = f"{ExploratoryVars.input_directory}/{file}"

        df = pd.read_csv(filename)

        if "user_id" in df:
            df = df[
                [
                    "id",
                    datecol[0],
                    "text",
                    "hashtags",
                    "media",
                    "urls",
                    "user_id",
                    "user_verified",
                ]
            ]
        else:
            df = df[
                [
                    "id",
                    datecol[0],
                    "text",
                    "hashtags",
                    "media",
                    "urls",
                    "user_verified",
                ]
            ]

        # ids = df.id

        media_or_url = (df["media"].notnull() | df["urls"].notnull()).rename(
            "media_or_url"
        )

        mentions_count = df.text.apply(count_mentions).rename("mentions_count")

        unique_hashtags_count = df.text.apply(count_unique_hashtags).rename(
            "unique_hashtags_count"
        )

        dates = pd.to_datetime(df[datecol[0]], format=datecol[1])
        weeks = dates.dt.isocalendar().week
        
        tweet_date = dates.apply(
            lambda x: str(x).split(" ")[0]
        ).rename("tweet_date")

        sample = df.drop(
            [
                "id",
                datecol[0],
                "text",
                "hashtags",
                "media",
                "urls",
            ],
            axis=1,
        )

        sample = pd.concat(
            [
                tweet_date,
                sample,
                weeks,
                mentions_count,
                unique_hashtags_count,
                media_or_url,
            ],
            axis=1,
        )

        samples.append(sample)

        # ids.to_csv(f"tweet_ids/tweetids_{i}.csv", index=False, header=False)

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


def weekly_analysis(args):
    files = os.listdir("weekly_data")

    print("analysing weekly data")

    hydrated = args["hydrated"]

    month = 1
    weeks_data = []
    tweets_count = 0
    tweets_percent_change = "N/A"
    for i, file in enumerate(tqdm(files)):
        filename = f"weekly_data/{file}"

        df = pd.read_csv(filename)

        prev_tweets_count = tweets_count

        # Total no of tweets in the week
        tweets_count = df.shape[0]

        # Percent change
        if prev_tweets_count:
            tweets_percent_change = (
                (tweets_count - prev_tweets_count) / prev_tweets_count
            ) * 100

        # mean number of hashtags
        mean_no_of_hashtags = df.unique_hashtags_count.mean()

        verified = df[df.user_verified == True]
        unverified = df[df.user_verified == False]

        if not hydrated:
            # Number of unique tweeters
            num_unique_tweeters = df.user_id.unique().shape[0]

            # Mean number of tweets by verified and unverified users
            mean_tweets_verified_user, mean_tweets_unverified_user = (
                verified.shape[0] / verified.user_id.unique().shape[0],
                unverified.shape[0] / unverified.user_id.unique().shape[0],
            )
        else:
            num_unique_tweeters = "N/A"
            mean_tweets_verified_user = "N/A"
            mean_tweets_unverified_user = "N/A"

        # Handle zero division:

        # try:
        #     mean_tweets_verified_user = verified.shape[0]
        #       / verified.user_id.unique().shape[0]
        # except ZeroDivisionError:
        #     mean_tweets_verified_user = 0
        #     print(verified.shape[0], verified.user_id.unique())

        # try:
        #     mean_tweets_unverified_user = unverified.shape[0]
        #       / unverified.user_id.unique().shape[0]
        # except ZeroDivisionError:
        #     mean_tweets_unverified_user = 0
        #     print(unverified.shape[0], unverified.user_id.unique())

        # Mean no of tweets with url or media (images or video)
        mean_no_with_media_or_url = df.media_or_url.mean()

        # Grouping data by date
        week_by_date = df.groupby(["tweet_date"]).count()
        week_by_date_usrverified = week_by_date.user_verified

        weeks_data.append(
            [
                f"A{i+1}",
                months[month - 1],
                os.path.splitext(file)[0][-2:],
                week_by_date_usrverified.min(),
                week_by_date_usrverified.max(),
                week_by_date_usrverified.median(),
                week_by_date_usrverified.mean(),
                num_unique_tweeters,
                tweets_percent_change,
                tweets_count,
                mean_no_with_media_or_url,
                mean_no_of_hashtags,
                mean_tweets_verified_user,
                mean_tweets_unverified_user,
            ]
        )

        if (i + 1) % 4 == 0:
            month += 1

    data = pd.DataFrame(
        weeks_data,
        columns=[
            "Index",
            "Month",
            "Week number (of year)",
            "Min (Tweets in a day)",
            "Max (Tweets in a day)",
            "Median (Tweets in a day)",
            "Mean (Tweets in a day)",
            "Unique tweeters",
            "Percent change",
            "Tweets count",
            "Mean (Tweets with link or media)",
            "Mean (Hashtags in a tweet)",
            "Mean (Tweets per verified user)",
            "Mean (Tweets per unverified user)",
        ],
    )

    data.to_csv("exploratory.csv", index=False)


if __name__ == "__main__":
    # prepare_weekly_data()
    # weekly_breakdown()
    # weekly_analysis()
    lineplots_exploratory_data()
