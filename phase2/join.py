import os
import pandas as pd

# Make sure the files align
unhydrated = "unhydrated"
hydrated = "hydrated"
merged = "merged"


def join(unhy, hy, outputname):
    unhyd = pd.read_csv(unhy)
    hyd = pd.read_csv(hy)

    unhyd = unhyd.drop(["favorite_count", "retweet_count"], axis=1)
    hyd = hyd[["id", "favorite_count", "retweet_count"]]

    merged = unhyd.join(hyd.set_index("id"), on="id")

    merged.to_csv(outputname, index=False)


if __name__ == "__main__":
    print("joining hydrated and unhydrated files")
    for i, (unhy, hy) in enumerate(zip(os.listdir("unhydrated"), os.listdir("hydrated"))):
        print(f"{unhy} <====> {hy}")
        join(
            f"{unhydrated}/{unhy}",
            f"{hydrated}/{hy}",
            f"{merged}/merged_%03d.csv" % (i + 1),
        )
