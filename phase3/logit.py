import os, pickle
import pandas as pd
import numpy as np
import statsmodels.formula.api as smf
import statsmodels.api as sm
from datetime import date


main_cols = ["id", "log_retweets_per_follower", "retweets_per_follower", "topic_log_probability", "topic_id", "topic_probability", "media", "user_verified", "user_created_at", "Anger", "Disgust", "Fear", "Joy", "Sadness", "Surprise", "Trust", "Anticipation", "Anger_log", "Disgust_log", "Fear_log", "Joy_log", "Sadness_log", "Surprise_log", "Trust_log", "Anticipation_log"]

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

df.dropna(subset=['topic_log_probability', "log_retweets_per_follower"], inplace=True)

## Account age
def accountage(x):
	y = x.date()
	ref_date = date(2020, 12, 1)

	return (ref_date-y).days / 365

df["account_age"] = pd.to_datetime(df["user_created_at"], format='%a %b %d %H:%M:%S %z %Y').apply(accountage)
# df["Emotion_prob"] = df[["Anger", "Disgust", "Fear", "Joy", "Sadness", "Surprise", "Trust", "Anticipation"]].max(axis=1)

# df["Emotion_prob_log"] = np.log10(df["Emotion_prob"]) 

df["media_bool"] = df["media"].notnull()

topic_columns = ["topic_is_not_disinformation", "topic_is_trolling", "topic_is_out_of_scope", "topic_is_debatable", "topic_is_conspiracy_theory"]

for col in topic_columns:
	df[col] = False

topic_id_topic_cat_dict = pd.read_pickle("topic_id_topic_cat_dict")

for col in topic_columns:
	df["topic_type"] = df["topic_id"].map(topic_id_topic_cat_dict)
	df[col][df["topic_type"] == col] = True

# print(df[["id", "Emotion_prob", "Emotion_prob_log"]])

correlation = df[["log_retweets_per_follower", "topic_log_probability", "media_bool", "user_verified", "account_age"] + topic_columns].corr()

correlation.to_csv("correlation4.csv", index=False)

prominent_emotion_formula = '''retweets_per_follower ~ topic_probability + 
Emotion_prob + media_bool + user_verified + account_age +
topic_is_not_disinformation +
topic_is_trolling +
topic_is_out_of_scope +
topic_is_debatable +
topic_is_conspiracy_theory
'''

prominent_emotion_formula_log = '''log_retweets_per_follower ~ topic_log_probability + 
Emotion_prob_log + media_bool + user_verified + account_age +
topic_is_not_disinformation +
topic_is_trolling +
topic_is_out_of_scope +
topic_is_debatable +
topic_is_conspiracy_theory
'''

### Prominent Emotion only
## Log transformed linear regression
# X = df[["topic_log_probability", "media_bool", "user_verified"]]
# y = df[["log_retweets_per_follower"]]

# X = sm.add_constant(X)
# linreg = sm.OLS(y, X).fit()


# linreg = smf.ols(prominent_emotion_formula_log, data=df).fit()
# print(linreg.summary())

# ## Logistic regression
# # log_reg = smf.logit(prominent_emotion_formula_log, data=df).fit()
# # print(log_reg.summary())

# Negative Binomial Regression
# nbr = smf.glm(prominent_emotion_formula, data=df, family=sm.families.NegativeBinomial()).fit()
# print(nbr.summary())


# ### All emotions

# Negative Binomial
prominent_emotion_formula = '''retweets_per_follower ~
Anger +
Disgust +
Fear +
Joy +
Sadness +
Surprise + 
Trust + 
Anticipation + 
topic_is_not_disinformation +
topic_is_trolling +
topic_is_out_of_scope +
topic_is_debatable +
topic_is_conspiracy_theory +
media_bool + 
user_verified + 
account_age'''

prominent_emotion_formula_log = '''log_retweets_per_follower ~  
Anger_log +
Disgust_log +
Fear_log +
Joy_log +
Sadness_log +
Surprise_log + 
Trust_log + 
Anticipation_log + 
topic_is_not_disinformation +
topic_is_trolling +
topic_is_out_of_scope +
topic_is_debatable +
topic_is_conspiracy_theory +
media_bool + 
user_verified + 
account_age'''

# linreg = smf.ols(prominent_emotion_formula_log, data=df).fit()
# print(linreg.summary())

## Negative Binomial Regression
nbr = smf.glm(prominent_emotion_formula, data=df, family=sm.families.NegativeBinomial()).fit()
print(nbr.summary())
