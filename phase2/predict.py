import os, sys
import pandas as pd
from tqdm import tqdm
from shutil import move, rmtree


os.environ['KERAS_BACKEND'] = 'theano'

basedir = "predict"
srcdir = os.path.join(basedir, "merged")
tmpdir = os.path.join(basedir, "tmp")
outdir = os.path.join(basedir, "output")
donedir = os.path.join(basedir, "done")

# The variable howmany defines how many files to process in one run.
howmany = 90
# chunksize = 100


def makedir(path):
    """
    Creates a directory if it doesn't already exist
    """
    if not os.path.isdir(path):
        os.makedirs(path)


def main():
    print(f"no of files to process: {howmany}")
    # print(f"batches of {chunksize} sentences")


    # Creating all required folders
    for folder in (outdir, donedir):
        makedir(folder)

    from emotion_predictor import EmotionPredictor

    # Loading in the model
    model = EmotionPredictor(classification="plutchik", setting="mc")

    for file in tqdm(os.listdir(srcdir)[:howmany], desc="overall"):
        # Getting the "name" part of the file, i.e. without the extension
        filename = os.path.splitext(file)[0]
        # workingdir = os.path.join(tmpdir, filename)
        # makedir(workingdir)

        # for j, chunk in enumerate(
        #     tqdm(
        #         pd.read_csv(os.path.join(srcdir, file), chunksize=chunksize),
        #         desc="current chunk",
        #     )
        # ):
        df = pd.read_csv(os.path.join(srcdir, file))
        df = df[["id", "text"]]
        probs = model.predict_probabilities(df.text)

        final = pd.concat([df.id, probs], axis=1)

        #     final.to_csv(
        #         os.path.join(workingdir, "chunk_%03d.csv" % (j + 1)),
        #         index=False,
        #     )

        # dfs = []
        # for wkfile in os.listdir(workingdir):
        #     dfs.append(pd.read_csv(os.path.join(workingdir, wkfile)))

        # ready = pd.concat(dfs)
        final.to_csv(
            os.path.join(outdir, "sentiments_%03d.csv" % int(filename[-3:])), index=False
        )

        # Move the completed file to the donedir
        move(os.path.join(srcdir, file), os.path.join(donedir, file))
        # rmtree(workingdir)


if __name__ == "__main__":
    # These exception handlers enable the program to be run in either format:
    # python predict.py
    # or
    # python predict.py 8
    try:
        howmany = int(sys.argv[1])
    except Exception:
        pass

    # try:
    #     chunksize = int(sys.argv[2])
    # except Exception:
    #     pass

    main()
