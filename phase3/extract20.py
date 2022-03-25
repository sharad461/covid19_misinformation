import os
import pandas as pd
import numpy as np
from tqdm import tqdm

folder = "rtperfollow"
samplepct = 0.2

allofit = []

for file in tqdm(os.listdir(folder)):
    df = pd.read_csv(os.path.join(folder, file))[["id", "text"]]
    slice_at = int(samplepct * df.shape[0])

    texts = df.iloc[:slice_at].text

    allofit += list(texts)

    # df["suspended_tweet"] = pd.isna(df["retweet_count"])

    # df = df.join(joined.set_index('id'), on='id')

    # df["retweets_per_follower"] = df.retweet_count.divide(
    #     df.user_followers_count
    # )

    # df.loc[
    #     ~np.isfinite(df["retweets_per_follower"]), "retweets_per_follower"
    # ] = np.nan

    # df["log_retweets_per_follower"] = np.log10(df["retweets_per_follower"])
    
    # df.loc[
    #     ~np.isfinite(df["log_retweets_per_follower"]), "log_retweets_per_follower"
    # ] = np.nan

    # data = df.loc[pd.isna(df["retweet_count"]), :][["id", "retweet_count"]]
    # suspended_ids = suspended_ids.append(data, ignore_index=True)

    # df.to_csv(os.path.join(output, file), index=False)

allo = pd.DataFrame(allofit, columns=["text"])
allo.to_csv("train.csv", index=False)
    
# suspended_ids.to_csv("suspended_ids.csv", index=False)