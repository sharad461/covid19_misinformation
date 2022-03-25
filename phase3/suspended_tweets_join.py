import os
import pandas as pd
import numpy as np
from tqdm import tqdm


suspended_ids = pd.read_csv("suspended_ids.csv")[["id"]]
rtcounts = pd.read_csv("rtcounts.csv") # Has all retweets, need only for suspended
# so join ids x rtcounts

new = suspended_ids.join(rtcounts.set_index('id'), on='id')

new.loc[
    np.isnan(new["retweet_count_before_susp"]), "retweet_count_before_susp"
] = 0
new.loc[
    np.isnan(new["favorite_count_before_susp"]), "favorite_count_before_susp"
] = 0

new.to_csv("joined2.csv", index=False)