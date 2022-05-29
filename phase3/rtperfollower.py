# Adds retweet per follower column to the dataset

import os
import pandas as pd
import numpy as np
from tqdm import tqdm

folder = "files"
output = "rtperfollow"

suspended_ids = pd.DataFrame()

joined = pd.read_csv("joined.csv")

for file in tqdm(os.listdir(folder)):
    df = pd.read_csv(os.path.join(folder, file))

    df["suspended_tweet"] = pd.isna(df["retweet_count"])

    df = df.join(joined.set_index('id'), on='id')

    df["retweets_per_follower"] = df.retweet_count.divide(
        df.user_followers_count
    )

    df.loc[
        ~np.isfinite(df["retweets_per_follower"]), "retweets_per_follower"
    ] = np.nan

    df["log_retweets_per_follower"] = np.log10(df["retweets_per_follower"])
    
    df.loc[
        ~np.isfinite(df["log_retweets_per_follower"]), "log_retweets_per_follower"
    ] = np.nan

    data = df.loc[pd.isna(df["retweet_count"]), :][["id", "retweet_count"]]
    suspended_ids = suspended_ids.append(data, ignore_index=True)

    df.to_csv(os.path.join(output, file), index=False)

    # break

    
# suspended_ids.to_csv("suspended_ids.csv", index=False)