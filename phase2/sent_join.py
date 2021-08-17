import os, random
import pandas as pd

# Make sure the files align
merged = "merged"
sentiments = "sentiments"
joined = "filter"


def join(merged, sentiments, outputname):
    def check(ix):
        check = merged.text[ix] == sentiments.Tweet[ix]

        return check

    merged = pd.read_csv(merged)
    sentiments = pd.read_csv(sentiments)

    # merged = merged.drop(["favorite_count", "retweet_count"], axis=1)

    assert merged.shape[0] == sentiments.shape[0], "Not equal no of rows"

    for i in range(10):
        ix = random.choice(range(merged.shape[0]))
        assert check(ix) == True, f"Assertion failed at index {ix}"

    # merged = merged.drop_duplicates(subset=["id"])
    # sentiments = sentiments.drop_duplicates(subset=["id"])

    sentiments = sentiments.drop(["Tweet"], axis=1)

    joined = merged.join(sentiments.set_index("id"), on="id")
    
    merged = merged.drop_duplicates(subset=["id"])
    joined = joined.drop_duplicates(subset=["id"])
    
    print(merged.shape[0], sentiments.shape[0], joined.shape[0])
    
    # assert merged.shape[0] == sentiments.shape[0] == joined.shape[0], "Output doesn't have equal no of rows"

    joined.to_csv(outputname, index=False)


if __name__ == "__main__":
    print("joining merged and sentiments files")
    for i, (m, s) in enumerate(zip(os.listdir(merged), os.listdir(sentiments))):
        print(f"{m} <====> {s}")
        join(
            f"{merged}/{m}",
            f"{sentiments}/{s}",
            f"{joined}/sentiments_%03d.csv" % (i + 1),
        )
