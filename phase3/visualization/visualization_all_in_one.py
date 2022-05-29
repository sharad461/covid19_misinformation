
##### This is the working draft version, please refer to viz_manual_sample.py and viz_full_sample.py
##### for files that handle the manual sample and the full dataset separately.

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import textwrap
import matplotlib.text as mpl_text


sns.set_theme()


def wrap_labels(ax, width, break_long_words=False):
    labels = []
    for label in ax.get_yticklabels():
        text = label.get_text()
        labels.append(
            textwrap.fill(text, width=width, break_long_words=break_long_words)
        )
    ax.set_yticklabels(labels, rotation=0)


def generate_and_save_fig(table, type_column, title):
    # fig, ax = plt.subplots(figsize=(8, 6))

    # order = table.sort_values(by="Frequency", ascending=False)

    # ax = sns.barplot(
    #     y=type_column, x="Frequency", data=table, order=order[type_column]
    # )

    # ax.bar_label(ax.containers[0])
    # wrap_labels(ax, 10)

    # colors = sns.color_palette()
    # pie = plt.pie(table.Frequency, colors=colors)

    # labels = [l for l in zip(table[type_column], )]
    # labels = ["\n".join(textwrap.wrap(l, 35)) for l in table[type_column]]

    # plt.legend(
    #     pie[0],
    #     labels,
    #     bbox_to_anchor=(1, 0.5),
    #     bbox_transform=plt.gcf().transFigure,
    #     loc="center right",
    #     fontsize=10,
    # )
    # plt.subplots_adjust(left=0.0, bottom=0.1, right=0.7)

    # pie = plt.pie(table.Frequency, colors=colors)

    table["labels"] = [
        "<br>".join(textwrap.wrap(l, 40)) for l in table[type_column]
    ]

    fig = px.pie(
        table,
        values="Frequency",
        names="labels",
        title=title,
    )

    fig.update_layout(
        legend={
            "yanchor": "middle",
            "y": 0.54,
            "x": 1.15,
            "xanchor": "right",
        },
        title={
            "x": 0.5,
            "xanchor": "center",
            "yanchor": "top",
        },
    )

    fig.show()
    # f = ax.get_figure()
    # plt.savefig(f"{type_column}_out.png")


class AnyObject(object):
    def __init__(self, text, color):
        self.my_text = text
        self.my_color = color


class AnyObjectHandler(object):
    def legend_artist(self, legend, orig_handle, fontsize, handlebox):
        x0, y0 = handlebox.xdescent, handlebox.ydescent
        width, height = handlebox.width, handlebox.height
        patch = mpl_text.Text(
            x=0,
            y=0,
            text=orig_handle.my_text,
            color=orig_handle.my_color,
            verticalalignment="baseline",
            horizontalalignment="left",
            multialignment=None,
            fontproperties=None,
            rotation=0,
            linespacing=None,
            rotation_mode=None,
        )
        handlebox.add_artist(patch)
        return patch


# df = pd.read_stata("ConAn15KMerge.dta")

titles = {
    ## PIE CHARTS
    "TYPE1": "Prevalence of Disinformation<br>Manually Annotated Sample (n=14,881)",
    "TYPE2": "Prevalence of Disinformation - Not disinformation vs disinformation<br>Manually Annotated Sample (n=6,639)",
    "TYPE": "Prevalence of Disinformation by Disinformation Categories<br>Manually Annotated Sample (n=2,216)",
    "Type1_FULL": "Prevalence of Disinformation<br>Full Sample (n=20,014,503)",
    "Type2_FULL": "Prevalence of Disinformation - Not disinformation vs disinformation<br>Full Sample (n=8,923,971)",
    "Type1_sus": "Prevalence of Disinformation<br>Not Suspended Tweets Sample (n=16,609,000)",
    "Type2_sus": "Prevalence of Disinformation - Not disinformation vs disinformation<br>Not Suspended Tweets Sample (n=7,336,360)",

    "Type": "Prevalence of Disinformation by Disinformation Categories<br>Not Suspended Tweets Sample (n=2,323,232)",
    "TARGET": "Prevalent Targets of Disinformation<br>Manually Annotated Sample (n=2,216)",
    "TOPIC": "Prevalent Topics of Disinformation<br>Manually Annotated Sample (n=2,216)",
    # "Target": "Prevalent Targets of Disinformation (n=20014503)",
    # "Topic": "Prevalent Topics of Disinformation (n=20014503)",
    "USER": "Prevalent Users Tweeting Disinformation<br>Manually Annotated Sample (n=2,216)",

    "emotion": "Prevalent Emotions in Tweets with Disinformation<br>Manually Annotated Sample (n=2,216)",
    "Emotion": "Prevalent Emotions in Tweets with Disinformation<br>Not Suspended Tweets Sample (n=2,323,232)",
    
    ## HEATMAPS
    "TARGET_hm_col": "Prevalent Targets Across Information Categories\nManually Annotated Sample (n=6,639)",
    "TOPIC_hm_col": "Prevalent Topics Across Information Categories\nManually Annotated Sample (n=6,639)",
    "TARGET_hm_row": "Prevalent Targets Within Information Categories\nManually Annotated Sample (n=6,639)",
    "TOPIC_hm_row": "Prevalent Topics Within Information Categories\nManually Annotated Sample (n=6,639)",
    # "Target_hm_FULL": "Prevalent Targets - Not Disinformation vs Disinformation Categories (n=20014503)",
    # "Topic_hm_FULL": "Prevalent Topics - Not Disinformation vs Disinformation Categories (n=20014503)",
    "USER_hm_col": "Prevalent Users Across Information Categories\nManually Annotated Sample (n=6,639)",
    "USER_hm_row": "Prevalent Users Within Information Categories\nManually Annotated Sample (n=6,639)",
    "emotion_hm_col": "Prevalent Emotions Across Information Categories\nManually Annotated Sample (n=6,639)",
    "emotion_hm_row": "Prevalent Emotions Within Information Categories\nManually Annotated Sample (n=6,639)",
    
    "emotion_hm_FULL_col": "Prevalent Emotions Across Information Categories\nFull Sample (n=8,923,971)",
    "emotion_hm_FULL_row": "Prevalent Emotions Within Information Categories\nFull Sample (n=8,923,971)",
    "emotion_hm_sus_col": "Prevalent Emotions Across Information Categories\nSuspended Tweets Sample (n=1,587,611)",
    "emotion_hm_sus_row": "Prevalent Emotions Within Information Categories\nSuspended Tweets Sample (n=1,587,611)",

    "emotion_retweets_col": "Retweets and Emotions Across Information Categories\nManually Annotated Sample (n=14,881)",
    "emotion_retweets_FULL_col": "Retweets and Emotions Across Information Categories\nFull Sample (n=8,923,971)",
    "emotion_retweets_row": "Retweets and Emotions Within Information Categories\nManually Annotated Sample (n=14,881)",
    "emotion_retweets_FULL_row": "Retweets and Emotions Within Information Categories\nFull Sample (n=8,923,971)",
    
    "emotion_retweets_sus_col": "Retweets and Emotions Across Information Categories\nNot Suspended Tweets Sample (n=7,336,360)",
    "emotion_retweets_sus_row": "Retweets and Emotions Within Information Categories\nNot Suspended Tweets Sample (n=7,336,360)",
    "100TOPICS_1": "Prevalence of Disinformation Topics<br>Topic Label Sample (n=100)",
    "100TOPICS_2": "Prevalence of Disinformation Topics - Not disinformation vs disinformation<br>Topic Label Sample (n=37)",
    "100TOPICS": "Prevalence of Disinformation Topics<br>Topic Label Sample (n=12)",
}

#### PIECHARTS

def prepare_counts(df, column_name):
    disinfo = df[column_name].value_counts().reset_index()
    disinfo.columns = [column_name, "Frequency"]
    disinfo.replace(
        to_replace="Not-disinformation",
        value="Not Disinformation",
        inplace=True,
    )
    return disinfo


# disinfo = prepare_counts(df, "TYPE")
# generate_and_save_fig(disinfo, "TYPE", titles["TYPE1"])


# df = df[df.TYPE != "Out of Scope"]
# disinfo = prepare_counts(df, "TYPE")
# generate_and_save_fig(disinfo, "TYPE", titles["TYPE2"])


# df = df[df.TYPE != "Not-disinformation"]
# for type in ("TYPE", "TARGET", "TOPIC", "USER", "emotion"):
#     disinfo = prepare_counts(df, type)
#     generate_and_save_fig(disinfo, type, titles[type])

#### END OF

#### Beginning of "overall" tasks

# for type in ("USER", "TOPIC", "TARGET", "EMOTION"):
#     df[f"{type} TYPES"] = df[type].apply(
#         lambda x: "".join(w[0] for w in x.split() if w[0].isupper())
#     )

# topics_by_cat = df[["TYPE", "TOPIC TYPES"]].pivot_table(
#     index="TYPE", columns="TOPIC TYPES", aggfunc="value_counts"
# )
# targets_by_cat = df[["TYPE", "TARGET TYPES"]].pivot_table(
#     index="TYPE", columns="TARGET TYPES", aggfunc="value_counts"
# )

#### End of "overall" tasks

# # #### Emotions by disinfo type first iteration (original code)


# ### Heatmaps

# df = df[df.TYPE != "Out of Scope"]

# df["TYPE"].replace(
#     to_replace="Not-disinformation",
#     value="Not Disinformation",
#     inplace=True,
# )

# emotions_by_cat = df[["TYPE", "emotion"]].pivot_table(
#     index="TYPE", columns="emotion", aggfunc="value_counts"
# )

# emotions_by_cat = emotions_by_cat.loc[~(emotions_by_cat == 0).all(axis=1)]
# emotions_by_cat_row = emotions_by_cat.apply(lambda x: x / x.sum() * 100, axis=1)

# f, ax = plt.subplots(figsize=(11, 6))
# sns.heatmap(
#     emotions_by_cat_row, annot=True, fmt=".2f", linewidths=0.5, ax=ax
# )

# wrap_labels(ax, 10)

# ax.set_title(titles["emotion_hm_row"])
# # ax.set_title(titles["emotion_hm_FULL"])
# plt.xlabel("Emotions")
# plt.ylabel("Disinformation Types")

# f = ax.get_figure()
# f.savefig(f"emotion_by_cat_out_1.png", bbox_inches="tight")


# ## ACROSS

# emotions_by_cat_col = emotions_by_cat.apply(lambda x: x / x.sum() * 100, axis=0)

# f, ax = plt.subplots(figsize=(11, 6))
# sns.heatmap(
#     emotions_by_cat_col, annot=True, fmt=".2f", linewidths=0.5, ax=ax
# )

# wrap_labels(ax, 10)

# ax.set_title(titles["emotion_hm_col"])
# # ax.set_title(titles["emotion_hm_FULL"])
# plt.xlabel("Emotions")
# plt.ylabel("Disinformation Types")

# f = ax.get_figure()
# f.savefig(f"emotion_by_cat_out_1_col.png", bbox_inches="tight")


# # ## USER, TARGET, TOPIC

# import re
# for type in ("USER", "TARGET", "TOPIC"):  # topics_by_cat, targets_by_cat)
#     if type == "TOPIC":
#         df["TOPIC"].replace("Out of Scope", "General", inplace=True)

#     full_labels = df[type]
#     full_labels = full_labels.drop_duplicates()
#     full_labels.dropna(inplace=True)

#     abbrv = full_labels.apply(
#         lambda x: "".join(w[0] for w in re.sub('[()]', "", x).title().split())[:3],
#     )

#     df[type] = df[type].apply(
#         lambda x: "".join(w[0] for w in re.sub('[()]', "", x).title().split())[:3]
#     )

#     obj_by_cat = df[["TYPE", type]].pivot_table(
#         index="TYPE", columns=type, aggfunc="value_counts"
#     )

#     obj_by_cat = obj_by_cat.loc[~(obj_by_cat == 0).all(axis=1)]
#     for t in ("row", "col"):
#         if t == "row":
#             Obj_ = obj_by_cat.apply(lambda x: x / x.sum() * 100, axis=1)
#         else:
#             Obj_ = obj_by_cat.apply(lambda x: x / x.sum() * 100, axis=0)

#         f, ax = plt.subplots(figsize=(18, 6))
#         sns.heatmap(Obj_, annot=True, fmt=".2f", linewidths=0.5, ax=ax)

#         wrap_labels(ax, 10)

#         ax.set_title(titles[f"{type}_hm_{t}"])
#         plt.xlabel(f"{type.capitalize()} Types")
#         plt.ylabel("Disinformation Types")

#         # wrapped_labels = [
#         #     "\n".join(textwrap.wrap(l, 40)) for l in full_labels.astype("str")
#         # ]
#         labels = [AnyObject(abbr, "black") for abbr in abbrv]

#         plt.legend(
#             labels,
#             full_labels.astype("str"),
#             handler_map={x: AnyObjectHandler() for x in labels},
#             loc="upper left",
#             bbox_to_anchor=(1.18, 1),
#         )

#         f = ax.get_figure()
#         f.savefig(f"{type}_by_cat_out_1_{t}.png", bbox_inches="tight")

#### End of


#### DISINFO in 100 TOPICS

# df = pd.read_excel("TopicLabelv1.xlsx")

# # Clean the data
# df["Type"].replace(
#     to_replace="out of scope", value="Out of Scope", inplace=True
# )
# df["Type"].replace(
#     to_replace="not disinformation", value="Not Disinformation", inplace=True
# )


# def prepare_counts_topics(df, column_name):
#     disinfo = (
#         df[["Terms", column_name]].value_counts([column_name]).reset_index()
#     )
#     disinfo.columns = [column_name, "Frequency"]

#     return disinfo


# disinfo = prepare_counts_topics(df, "Type")
# generate_and_save_fig(disinfo, "Type", titles["100TOPICS_1"])

# df = df[df.Type != "Out of Scope"]
# disinfo = prepare_counts_topics(df, "Type")
# generate_and_save_fig(disinfo, "Type", titles["100TOPICS_2"])

# df = df[df.Type != "Not Disinformation"]
# disinfo = prepare_counts_topics(df, "Type")
# generate_and_save_fig(disinfo, "Type", titles["100TOPICS"])

#### END OF


### RETWEET % for EMOTIONS

# df = pd.read_csv("topics_to_emotion_suspended.csv")

# df = df[df.TYPE != "Out of Scope"]

# # df["retweet_count"] = df["retweet_count"].combine_first(df["retweet_count_before_susp"])

# print(df["retweet_count"].isnull().sum())

# df["TYPE"].replace(
#     to_replace="Not-disinformation",
#     value="Not Disinformation",
#     inplace=True,
# )

# emotions_labels = [
#     "Anger",
#     "Anticipation",
#     "Disgust",
#     "Fear",
#     "Joy",
#     "Sadness",
#     "Surprise",
#     "Trust",
# ]

# print(df.shape)

# emotions_by_cat = df[["TYPE", "emotion", "retweet_count"]].pivot_table(
#     index="TYPE", columns="emotion", aggfunc="sum"
# )
# emotions_by_cat = emotions_by_cat.loc[~(emotions_by_cat == 0).all(axis=1)]

# emotions_by_cat.to_csv("output.csv")
    
# for t in ("row", "col"):
#     if t == "row":
#         Obj_ = emotions_by_cat.apply(lambda x: x / x.sum() * 100, axis=1)
#     else:
#         Obj_ = emotions_by_cat.apply(lambda x: x / x.sum() * 100, axis=0)

#     f, ax = plt.subplots(figsize=(11, 6))
#     sns.heatmap(
#         Obj_,
#         xticklabels=emotions_labels,
#         annot=True,
#         fmt=".2f",
#         linewidths=0.5,
#         ax=ax,
#     )

#     wrap_labels(ax, 10)

#     ax.set_title(titles[f"emotion_retweets_{t}"])
#     plt.xlabel("Emotions")
#     plt.ylabel("Disinformation Types")

#     f = ax.get_figure()
#     f.savefig(f"retweet_emotion_by_cat_out_1_{t}.png", bbox_inches="tight")

#### End of


#### FULL Dataset
#### PIECHARTS

df = pd.read_csv("topics_to_emotion_not_suspended.csv")

# print(df.shape)
df["Type"] = df["Type"].apply(lambda x: x.title())
df["Target"] = df["Target"].apply(lambda x: x.title())
df["Topic"] = df["Topic"].apply(lambda x: x.title())
col_name = "Type"

# disinfo = prepare_counts(df, col_name)
# generate_and_save_fig(disinfo, col_name, titles["Type1_sus"])


df = df[df.Type != "Out Of Scope"]
# print(df.shape)
# disinfo = prepare_counts(df, col_name)
# generate_and_save_fig(disinfo, col_name, titles["Type2_sus"])

df_ = df[df.Type != "Not Disinformation"]
print(df_.shape)
for type in ("Type", "Emotion"):
    disinfo = prepare_counts(df_, type)
    generate_and_save_fig(disinfo, type, titles[type])

# # #### END OF


# emotions_by_cat = df[["Type", "Emotion"]].pivot_table(
#     index="Type", columns="Emotion", aggfunc="value_counts"
# )

# emotions_by_cat = emotions_by_cat.loc[~(emotions_by_cat == 0).all(axis=1)]

# for t in ("row", "col"):
#     if t == "row":
#         Obj_ = emotions_by_cat.apply(lambda x: x / x.sum() * 100, axis=1)
#     else:
#         Obj_ = emotions_by_cat.apply(lambda x: x / x.sum() * 100, axis=0)

#     f, ax = plt.subplots(figsize=(11, 3))
#     sns.heatmap(
#         Obj_, annot=True, fmt=".2f", linewidths=0.5, ax=ax
#     )

#     wrap_labels(ax, 10)

#     ax.set_title(titles[f"emotion_hm_sus_{t}"])
#     plt.xlabel("Emotions")
#     plt.ylabel("Disinformation Types")

#     f = ax.get_figure()
#     f.savefig(f"emotion_by_cat_out_1_{t}.png", bbox_inches="tight")



# import re
# for type in ("Target", "Topic"):  # topics_by_cat, targets_by_cat)
#     if type == "Topic":
#         df["Topic"].replace("Out Of Scope", "General", inplace=True)

#     full_labels = df[type]
#     full_labels = full_labels.drop_duplicates()
#     full_labels.dropna(inplace=True)

#     abbrv = full_labels.apply(
#         lambda x: "".join(w[0] for w in re.sub('[()]', "", x).title().split())[:3],
#     )

#     df[type] = df[type].apply(
#         lambda x: "".join(w[0] for w in re.sub('[()]', "", x).title().split())[:3]
#     )

#     obj_by_cat = df[["Type", type]].pivot_table(
#         index="Type", columns=type, aggfunc="value_counts"
#     )

#     obj_by_cat = obj_by_cat.loc[~(obj_by_cat == 0).all(axis=1)]
#     obj_by_cat = obj_by_cat.apply(lambda x: x / x.sum() * 100, axis=1)

#     f, ax = plt.subplots(figsize=(18, 3))
#     sns.heatmap(obj_by_cat, annot=True, fmt=".2f", linewidths=0.5, ax=ax)

#     wrap_labels(ax, 10)

#     ax.set_title(titles[f"{type}_hm_FULL"])
#     plt.xlabel(f"{type.capitalize()} Types")
#     plt.ylabel("Disinformation Types")

#     # wrapped_labels = [
#     #     "\n".join(textwrap.wrap(l, 40)) for l in full_labels.astype("str")
#     # ]
#     labels = [AnyObject(abbr, "black") for abbr in abbrv]

#     plt.legend(
#         labels,
#         full_labels.astype("str"),
#         handler_map={x: AnyObjectHandler() for x in labels},
#         loc="upper left",
#         bbox_to_anchor=(1.18, 1),
#     )

#     f = ax.get_figure()
#     f.savefig(f"{type}_by_cat_out_1.png", bbox_inches="tight")

#####

# emotions_labels = [
#     "Anger",
#     "Anticipation",
#     "Disgust",
#     "Fear",
#     "Joy",
#     "Sadness",
#     "Surprise",
#     "Trust",
# ]

# emotions_by_cat = df[["Type", "Emotion", "retweet_count"]].pivot_table(
#     index="Type", columns="Emotion", aggfunc="sum"
# )
# emotions_by_cat = emotions_by_cat.loc[~(emotions_by_cat == 0).all(axis=1)]

# for t in ("row", "col"):
#     if t == "row":
#         Obj_ = emotions_by_cat.apply(lambda x: x / x.sum() * 100, axis=1)
#     else:
#         Obj_ = emotions_by_cat.apply(lambda x: x / x.sum() * 100, axis=0)

#     f, ax = plt.subplots(figsize=(11, 3))
#     sns.heatmap(
#         Obj_,
#         xticklabels=emotions_labels,
#         annot=True,
#         fmt=".2f",
#         linewidths=0.5,
#         ax=ax,
#     )

#     wrap_labels(ax, 10)

#     ax.set_title(titles[f"emotion_retweets_sus_{t}"])
#     plt.xlabel("Emotions")
#     plt.ylabel("Disinformation Types")

#     f = ax.get_figure()
#     f.savefig(f"retweet_emotion_by_cat_out_1_{t}.png", bbox_inches="tight")