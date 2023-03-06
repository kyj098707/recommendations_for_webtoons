from sentence_transformers import SentenceTransformer, util
import pymysql
import re
import json
import copy

from util import *


if __name__ == "__main__":
    conn=pymysql.connect(host="kt-aivle.iptime.org",port=64010, user="aivle02", password="aivle02!", db="aivle02")
    cur = conn.cursor()
    cur.execute("SELECT * FROM recommendationapp_artwork")
    dic = {}

    for c in cur:
        dic[f"{c[1]}_{c[2]}"] = re.sub("[^ 0-9가-힣A-Za-z]","",c[5])

    sims_rank = {}
    base_list = list(dic.keys())
    compare_list = list(dic.keys())
    checkpoints = SentenceTransformer('snunlp/KR-SBERT-V40K-klueNLI-augSTS')


    base_story_list = checkpoints.encode(list(dic.values()))
    compare_story_list = copy.deepcopy(base_story_list)

    for base_uid, base_story in zip(base_list,base_story_list):
        tmp = []
        for comp_uid, comp_story in zip(compare_list,compare_story_list):
            if base_uid == comp_uid:
                continue
            sim = find_sim(base_story,comp_story).item()
            tmp.append((sim,comp_uid))
        tmp = sorted(tmp, reverse=True)[:20]
        sims_rank[base_uid] = tmp

    with open('./json/story_sims_rank.json','w') as fp:
        json.dump(sims_rank,fp)