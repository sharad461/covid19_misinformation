import os
import pandas as pd
import numpy as np
from tqdm import tqdm

inference = "inference"
rtperfollower = "rtperfollow"
output = "inference_merged"

# suspended_ids = pd.DataFrame()

for file in tqdm(os.listdir(rtperfollower)):
    df_main = pd.read_csv(os.path.join(rtperfollower, file))
    df_inf = pd.read_csv(os.path.join(inference, file))[["id", "topic_id", "probability", "log_probability"]]
    df_inf.rename(columns = {'probability':'topic_probability', 'log_probability':'topic_log_probability'}, inplace = True)

    rows_pre_join = df_main.shape[0]

    df_main = df_main.join(df_inf.set_index('id'), on='id')

    assert df_main.shape[0] == rows_pre_join, "unequal no of rows"
    df_main.to_csv(os.path.join(output, file), index=False)

    
# suspended_ids.to_csv("suspended_ids.csv", index=False)