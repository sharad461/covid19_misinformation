import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from imports import wrap_labels, AnyObject, AnyObjectHandler, generate_and_save_fig
from titles import titles

sns.set_theme()

##### Manually Annotated Sample

### PIECHARTS

df = pd.read_stata("ConAn15KMerge.dta")


def prepare_counts(df, column_name):
    disinfo = df[column_name].value_counts().reset_index()
    disinfo.columns = [column_name, "Frequency"]
    disinfo.replace(
        to_replace="Not-disinformation",
        value="Not Disinformation",
        inplace=True,
    )
    return disinfo

# All types
disinfo = prepare_counts(df, "TYPE")
generate_and_save_fig(disinfo, "TYPE", titles["TYPE1"])

# Exclude Out of Scope tweets
df = df[df.TYPE != "Out of Scope"]
disinfo = prepare_counts(df, "TYPE")
generate_and_save_fig(disinfo, "TYPE", titles["TYPE2"])

# Exclude Not disinformation tweets
df = df[df.TYPE != "Not-disinformation"]
for type in ("TYPE", "TARGET", "TOPIC", "USER", "emotion"):
    disinfo = prepare_counts(df, type)
    generate_and_save_fig(disinfo, type, titles[type])

### END OF PIECHARTS

### HEATMAPS

# For Emotions
df = pd.read_stata("ConAn15KMerge.dta")
df = df[df.TYPE != "Out of Scope"]

df["TYPE"].replace(
    to_replace="Not-disinformation",
    value="Not Disinformation",
    inplace=True,
)

emotions_by_cat = df[["TYPE", "emotion"]].pivot_table(
    index="TYPE", columns="emotion", aggfunc="value_counts"
)

emotions_by_cat = emotions_by_cat.loc[~(emotions_by_cat == 0).all(axis=1)]

for t in ("row", "col"):
    if t == "row":
        Obj_ = emotions_by_cat.apply(lambda x: x / x.sum() * 100, axis=1)
    else:
        Obj_ = emotions_by_cat.apply(lambda x: x / x.sum() * 100, axis=0)

    f, ax = plt.subplots(figsize=(11, 6))

    sns.heatmap(
        Obj_, annot=True, fmt=".2f", linewidths=0.5, ax=ax
    )

    wrap_labels(ax, 10)

    ax.set_title(titles[f"emotion_hm_{t}"])
    plt.xlabel("Emotions")
    plt.ylabel("Disinformation Types")

    f = ax.get_figure()
    f.savefig(f"emotion_by_cat_{t}.png", bbox_inches="tight")


# For Users, Targets, Topics
import re
for type in ("USER", "TARGET", "TOPIC"):
    if type == "TOPIC":
        df["TOPIC"].replace("Out of Scope", "General", inplace=True)

    full_labels = df[type]
    full_labels = full_labels.drop_duplicates()
    full_labels.dropna(inplace=True)

    abbrv = full_labels.apply(
        lambda x: "".join(w[0] for w in re.sub('[()]', "", x).title().split())[:3],
    )

    df[type] = df[type].apply(
        lambda x: "".join(w[0] for w in re.sub('[()]', "", x).title().split())[:3]
    )

    obj_by_cat = df[["TYPE", type]].pivot_table(
        index="TYPE", columns=type, aggfunc="value_counts"
    )

    obj_by_cat = obj_by_cat.loc[~(obj_by_cat == 0).all(axis=1)]

    for t in ("row", "col"):
        if t == "row":
            Obj_ = obj_by_cat.apply(lambda x: x / x.sum() * 100, axis=1)
        else:
            Obj_ = obj_by_cat.apply(lambda x: x / x.sum() * 100, axis=0)

        f, ax = plt.subplots(figsize=(18, 6))
        sns.heatmap(Obj_, annot=True, fmt=".2f", linewidths=0.5, ax=ax)

        wrap_labels(ax, 10)

        ax.set_title(titles[f"{type}_hm_{t}"])
        plt.xlabel(f"{type.capitalize()} Types")
        plt.ylabel("Disinformation Types")

        labels = [AnyObject(abbr, "black") for abbr in abbrv]

        plt.legend(
            labels,
            full_labels.astype("str"),
            handler_map={x: AnyObjectHandler() for x in labels},
            loc="upper left",
            bbox_to_anchor=(1.18, 1),
        )

        f = ax.get_figure()
        f.savefig(f"{type}_by_cat_out_1_{t}.png", bbox_inches="tight")

### END OF HEATMAPS

##### END OF Manually Annotated Sample