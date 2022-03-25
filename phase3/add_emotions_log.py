import os
import pandas as pd
import numpy as np
from tqdm import tqdm

inference = "inference_merged"
output = "inference"

emotions = [
    "Anger",
    "Disgust",
    "Fear",
    "Joy",
    "Sadness",
    "Surprise",
    "Trust",
    "Anticipation",
]

columns_order = [
    "id",
    "tweet_url",
    "created_at",
    "parsed_created_at",
    "user_screen_name",
    "text",
    "tweet_type",
    "coordinates",
    "hashtags",
    "media",
    "urls",
    "in_reply_to_screen_name",
    "in_reply_to_status_id",
    "in_reply_to_user_id",
    "lang",
    "place",
    "possibly_sensitive",
    "reweet_or_quote_id",
    "retweet_or_quote_screen_name",
    "retweet_or_quote_user_id",
    "source",
    "user_id",
    "user_created_at",
    "user_default_profile_image",
    "user_description",
    "user_favourites_count",
    "user_followers_count",
    "user_friends_count",
    "user_listed_count",
    "user_location",
    "user_name",
    "user_statuses_count",
    "user_time_zone",
    "user_urls",
    "user_verified",
    "favorite_count",
    "retweet_count",
    "Anger",
    "Anger_log",
    "Disgust",
    "Disgust_log",
    "Fear",
    "Fear_log",
    "Joy",
    "Joy_log",
    "Sadness",
    "Sadness_log",
    "Surprise",
    "Surprise_log",
    "Trust",
    "Trust_log",
    "Anticipation",
    "Anticipation_log",
    "Emotion",
    "suspended_tweet",
    "retweet_count_before_susp",
    "favorite_count_before_susp",
    "retweets_per_follower",
    "log_retweets_per_follower",
    "topic_id",
    "topic_probability",
    "topic_log_probability",
]


# suspended_ids = pd.DataFrame()

for file in tqdm(os.listdir(inference)):
    df = pd.read_csv(os.path.join(inference, file))

    for emotion in emotions:
        df.loc[~np.isfinite(df[emotion]), emotion] = np.nan

        df[f"{emotion}_log"] = np.log10(df[emotion])

    # df_inf = pd.read_csv(os.path.join(inference, file))[["id", "topic_id", "probability", "log_probability"]]
    # df_inf.rename(columns = {'probability':'topic_probability', 'log_probability':'topic_log_probability'}, inplace = True)

    # rows_pre_join = df_main.shape[0]

    # df_main = df_main.join(df_inf.set_index('id'), on='id')

    df = df[columns_order]

    df.to_csv(os.path.join(output, file), index=False)


# suspended_ids.to_csv("suspended_ids.csv", index=False)
