import pandas as pd
import os, tqdm

df = pd.read_excel("visualization/TopicLabelv1.xlsx")

topics_ = df[["#", "Type", "Topic", "Target"]]

data_dir = "inference"

new_list = []

for file in tqdm.tqdm(os.listdir(data_dir)):
    data_df = pd.read_csv(os.path.join(data_dir, file))

    data_df.dropna(subset=["topic_id"], inplace=True)
    data_df = data_df[["id", "topic_id", "Emotion", "retweet_count"]]
    
    new = data_df.join(topics_.set_index('#'), on='topic_id')

    new_list.append(new)

    del data_df

final = pd.concat(new_list, ignore_index=True)

final.to_csv("topics_to_emotion.csv", index=False)

# final[["id", "Type", "Emotion"]].to_csv("topics_emotion.csv", index=False)
# final[["id", "Type", "Topic"]].to_csv("topics_topic.csv", index=False)
# final[["id", "Type", "Target"]].to_csv("topics_target.csv", index=False)
