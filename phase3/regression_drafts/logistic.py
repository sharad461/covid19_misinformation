import os, pickle
import pandas as pd
import numpy as np
import statsmodels.formula.api as smf
import statsmodels.api as sm
from datetime import date


main_cols = ["id", "retweet_count", "retweets_per_follower", "topic_log_probability", "topic_id", "topic_probability", "media", "user_verified", "user_created_at", "Anger_log", "Disgust_log", "Fear_log", "Joy_log", "Sadness_log", "Surprise_log", "Trust_log", "Anticipation_log"]

folder = "inference"

parts = []

count = 0

# for file in os.listdir(folder):
# 	df = pd.read_csv(os.path.join(folder, file))
# 	df = df[main_cols]
# 	df.dropna(subset=['topic_log_probability', "log_retweets_per_follower"], inplace=True)

# 	parts.append(df)
# 	count += 1

# 	if count > 5:
# 		break

# df = pd.concat(parts, ignore_index=True)

df = pd.read_csv("full_dataset/sentiments_001.csv")[main_cols]

# df.dropna(subset=['topic_log_probability', "log_retweets_per_follower"], inplace=True)

## Account age
def accountage(x):
	y = x.date()
	ref_date = date(2020, 12, 1)

	return (ref_date-y).days / 365

df["account_age"] = pd.to_datetime(df["user_created_at"], format='%a %b %d %H:%M:%S %z %Y').apply(accountage)

# df["has_been_retweeted"] = df["retweet_count"].notnull()
# df.has_been_retweeted.replace({True:1, False:0}, inplace=True)

df["has_been_retweeted"] = 0
df["has_been_retweeted"][df["retweet_count"] > 0] = 1

df["media_bool"] = df["media"].notnull()

topic_columns = ["topic_is_not_disinformation", "topic_is_trolling", "topic_is_out_of_scope", "topic_is_debatable", "topic_is_conspiracy_theory"]

for col in topic_columns:
	df[col] = False

topic_id_topic_cat_dict = pd.read_pickle("topic_id_topic_cat_dict")

for col in topic_columns:
	df["topic_type"] = df["topic_id"].map(topic_id_topic_cat_dict)
	df[col][df["topic_type"] == col] = True

correlation = df[["has_been_retweeted", "media_bool", "user_verified", "account_age"] + topic_columns].corr()

correlation.to_csv("correlation4.csv", index=False)

for typ in topic_columns:
	prominent_emotion_formula_log = f'''has_been_retweeted ~  
	Anger_log +
	Disgust_log +
	Fear_log +
	Joy_log +
	Sadness_log +
	Surprise_log + 
	Trust_log + 
	Anticipation_log + 
	{typ} +
	media_bool + 
	user_verified + 
	account_age'''

	log_reg = smf.logit(prominent_emotion_formula_log, data=df).fit()
	print(log_reg.summary())
