import os
import requests
from github import Github
import json
import pandas as pd
import logging

logger = logging.getLogger(__name__)
logger.setLevel("INFO")

def get_data():
    raw_df = load_data("./data/cs-train")
    pred_df = prep_data(raw_df)
    return pred_df

def load_data(local_folder, download = False):
    # download the data if needed
    if not download and os.path.exists(local_folder):
        logger.info("Using local folder")
    else:
        logger.info("Using downloading data ...")
        download_github_folder("aavail/ai-workflow-capstone", "cs-train", local_folder)
        logger.info("Using downloading data done")

    raw_df = pd.DataFrame()
    for fname in os.listdir(local_folder):
        fpath = os.path.join(local_folder, fname)
        with open(fpath, "rt") as f:
            data = json.load(f)
        raw_df = raw_df.append(pd.DataFrame(data))
    return raw_df

def handle_diff_spelling(df, main_spelling, second_spelling, default_val):
    df_new = df.copy()
    df_new[main_spelling] = df_new[main_spelling].fillna(default_val) + df_new[second_spelling].fillna(default_val)
    df_new = df_new.drop(second_spelling, axis=1)
    return df_new

def prep_data(raw_df):
    prep_df = raw_df.copy()
    prep_df = prep_df.reset_index(drop=True)
    prep_df["date"] = pd.to_datetime(pd.DataFrame(prep_df[["year", "month", "day"]]))
    # handle different spellings
    prep_df = handle_diff_spelling(prep_df, "times_viewed", "TimesViewed", 0)
    prep_df = handle_diff_spelling(prep_df, "stream_id", "StreamID", "")
    prep_df = handle_diff_spelling(prep_df, "price", "total_price", 0)
    return prep_df


def download_github_folder(repo_url, repo_path, local_folder):
    g = Github()
    # user = g.get_user("aavail")
    # for repo in user.get_repos():
    #     print(repo)
    repo = g.get_repo(repo_url)
    files = repo.get_contents(repo_path)
    if os.path.exists(local_folder):
        os.rmdir(local_folder)
    os.makedirs(local_folder)
    for file in files:
        resp = requests.get(file.download_url)
        if resp.ok:
            with open(os.path.join(local_folder,file.name),"wt") as f:
                json.dump(resp.json(),f)

if __name__ == '__main__':
    raw_df = load_data("cs-train")
    res =prep_data(raw_df)
