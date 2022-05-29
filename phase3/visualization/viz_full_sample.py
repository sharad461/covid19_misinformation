import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from imports import wrap_labels, AnyObject, AnyObjectHandler, generate_and_save_fig
from titles import titles

sns.set_theme()

##### FULL Dataset

### PIECHARTS

# This file can be generated using topic_leveller.py
df = pd.read_csv("topics_to_emotion_not_suspended.csv")

def prepare_counts(df, column_name):
    disinfo = df[column_name].value_counts().reset_index()
    disinfo.columns = [column_name, "Frequency"]
    disinfo.replace(
        to_replace="Not-disinformation",
        value="Not Disinformation",
        inplace=True,
    )
    return disinfo

df["Type"] = df["Type"].apply(lambda x: x.title())
df["Target"] = df["Target"].apply(lambda x: x.title())
df["Topic"] = df["Topic"].apply(lambda x: x.title())
col_name = "Type"

disinfo = prepare_counts(df, col_name)
generate_and_save_fig(disinfo, col_name, titles["Type1_sus"])

df = df[df.Type != "Out Of Scope"]
disinfo = prepare_counts(df, col_name)
generate_and_save_fig(disinfo, col_name, titles["Type2_sus"])

df_ = df[df.Type != "Not Disinformation"]
for type in ("Type", "Emotion"):
    disinfo = prepare_counts(df_, type)
    generate_and_save_fig(disinfo, type, titles[type])

### END OF PIECHARTS

### HEATMAPS

# For Emotions
df = pd.read_csv("topics_to_emotion_not_suspended.csv")

emotions_by_cat = df[["Type", "Emotion"]].pivot_table(
    index="Type", columns="Emotion", aggfunc="value_counts"
)

emotions_by_cat = emotions_by_cat.loc[~(emotions_by_cat == 0).all(axis=1)]

for t in ("row", "col"):
    if t == "row":
        Obj_ = emotions_by_cat.apply(lambda x: x / x.sum() * 100, axis=1)
    else:
        Obj_ = emotions_by_cat.apply(lambda x: x / x.sum() * 100, axis=0)

    f, ax = plt.subplots(figsize=(11, 3))
    sns.heatmap(
        Obj_, annot=True, fmt=".2f", linewidths=0.5, ax=ax
    )

    wrap_labels(ax, 10)

    ax.set_title(titles[f"emotion_hm_sus_{t}"])
    plt.xlabel("Emotions")
    plt.ylabel("Disinformation Types")

    f = ax.get_figure()
    f.savefig(f"emotion_by_cat_out_1_{t}.png", bbox_inches="tight")


# For Targets and Topics:
import re
for type in ("Target", "Topic"):  # topics_by_cat, targets_by_cat)
    if type == "Topic":
        df["Topic"].replace("Out Of Scope", "General", inplace=True)

    full_labels = df[type]
    full_labels = full_labels.drop_duplicates()
    full_labels.dropna(inplace=True)

    abbrv = full_labels.apply(
        lambda x: "".join(w[0] for w in re.sub('[()]', "", x).title().split())[:3],
    )

    df[type] = df[type].apply(
        lambda x: "".join(w[0] for w in re.sub('[()]', "", x).title().split())[:3]
    )

    obj_by_cat = df[["Type", type]].pivot_table(
        index="Type", columns=type, aggfunc="value_counts"
    )

    obj_by_cat = obj_by_cat.loc[~(obj_by_cat == 0).all(axis=1)]
    obj_by_cat = obj_by_cat.apply(lambda x: x / x.sum() * 100, axis=1)

    f, ax = plt.subplots(figsize=(18, 3))
    sns.heatmap(obj_by_cat, annot=True, fmt=".2f", linewidths=0.5, ax=ax)

    wrap_labels(ax, 10)

    ax.set_title(titles[f"{type}_hm_FULL"])
    plt.xlabel(f"{type.capitalize()} Types")
    plt.ylabel("Disinformation Types")

    # wrapped_labels = [
    #     "\n".join(textwrap.wrap(l, 40)) for l in full_labels.astype("str")
    # ]
    labels = [AnyObject(abbr, "black") for abbr in abbrv]

    plt.legend(
        labels,
        full_labels.astype("str"),
        handler_map={x: AnyObjectHandler() for x in labels},
        loc="upper left",
        bbox_to_anchor=(1.18, 1),
    )

    f = ax.get_figure()
    f.savefig(f"{type}_by_cat_out_1.png", bbox_inches="tight")

# For Retweets and Emotions
emotions_labels = [
    "Anger",
    "Anticipation",
    "Disgust",
    "Fear",
    "Joy",
    "Sadness",
    "Surprise",
    "Trust",
]

emotions_by_cat = df[["Type", "Emotion", "retweet_count"]].pivot_table(
    index="Type", columns="Emotion", aggfunc="sum"
)
emotions_by_cat = emotions_by_cat.loc[~(emotions_by_cat == 0).all(axis=1)]

for t in ("row", "col"):
    if t == "row":
        Obj_ = emotions_by_cat.apply(lambda x: x / x.sum() * 100, axis=1)
    else:
        Obj_ = emotions_by_cat.apply(lambda x: x / x.sum() * 100, axis=0)

    f, ax = plt.subplots(figsize=(11, 3))
    sns.heatmap(
        Obj_,
        xticklabels=emotions_labels,
        annot=True,
        fmt=".2f",
        linewidths=0.5,
        ax=ax,
    )

    wrap_labels(ax, 10)

    ax.set_title(titles[f"emotion_retweets_sus_{t}"])
    plt.xlabel("Emotions")
    plt.ylabel("Disinformation Types")

    f = ax.get_figure()
    f.savefig(f"retweet_emotion_by_cat_out_1_{t}.png", bbox_inches="tight")

### END OF HEATMAPS

##### END OF FULL Dataset