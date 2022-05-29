import pandas as pd
import os, tqdm

df = pd.read_excel("TopicLabelv1.xlsx")

topics_ = df[["#", "Type", "Topic", "Target"]]

data_dir = "new_full_dataset"

suspended = []
not_suspended = []

for file in tqdm.tqdm(os.listdir(data_dir)):
    data_df = pd.read_csv(os.path.join(data_dir, file))

    data_df.dropna(subset=["retweet_count"], inplace=True)

    data_df_suspended = data_df[data_df.suspended_tweet == True]
    # data_df_not_suspended = data_df[data_df.suspended_tweet == False]

    data_df_suspended = data_df_suspended[["id", "topic_id", "Emotion", "retweet_count"]]
    # data_df_not_suspended = data_df_not_suspended[["id", "topic_id", "Emotion", "retweet_count"]]
    
    suspended.append(data_df_suspended.join(topics_.set_index('#'), on='topic_id'))
    # not_suspended.append(data_df_not_suspended.join(topics_.set_index('#'), on='topic_id'))

    del data_df

suspended_full = pd.concat(suspended, ignore_index=True)
print(suspended_full.shape)
suspended_full.to_csv("topics_to_emotion_suspended.csv", index=False)

# not_suspended_full = pd.concat(not_suspended, ignore_index=True)
# not_suspended_full.to_csv("topics_to_emotion_not_suspended.csv", index=False)
# print(not_suspended_full.shape)