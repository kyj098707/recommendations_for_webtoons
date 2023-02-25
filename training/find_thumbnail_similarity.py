import json
import numpy as np
import torch
import torch.nn as nn
import timm

from sentence_transformers import util
import albumentations as A

import cv2
from torch.utils.data import Dataset, DataLoader
from albumentations.pytorch.transforms import ToTensorV2
from glob import glob
from tqdm.auto import tqdm

from util import *


def infer(model, test_loader, device):
    model.to(device)
    model.eval()
    predictions = []
    with torch.no_grad():
        for imgs in test_loader:
            imgs = imgs.float().to(device)
            probs = model(imgs)
            probs  = probs.cpu().detach().numpy()
            preds = probs.astype(float)
            predictions += preds.tolist() 
    return predictions

def extract_features(model,device):
    ### json 형식으로 uid : 특성 값(1280차원)으로 저장
    folder_list = list(map(lambda x: x.split('\\')[-1], glob("./data/*")))
    features_dic = {}
    test_transform = A.Compose([A.Resize(480, 480),
                                    A.Normalize(mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225), max_pixel_value=255.0, always_apply=False, p=1.0),
                                    ToTensorV2()])
    for folder in tqdm(folder_list):
        img = sorted(glob(f"./data/{folder}/*"))[1:]
        test_dataset = CustomDataset(img, None, test_transform)
        test_loader = DataLoader(test_dataset, batch_size = 16, shuffle=False)
        
        preds = infer(model, test_loader, device)
        np_preds = np.array(preds).mean(axis=0)
        features_dic[folder] = np_preds

    with open('./json/thumbnail_features.json','w') as fp:
        json.dump(features_dic,fp)

def find_similarity_rank():
    # 썸네일 유사도 json으로 저장 uid : [(유사도, 작품),,*20]
    with open('./thumbnail_score.json') as fp:
        features_dic = json.load(fp)
    sims_rank = {}
    dummy = []
    for base_uid in tqdm(features_dic.keys()):
        tmp = []
        for compare_uid in features_dic.keys():
            if base_uid == compare_uid:
                continue
            if type(features_dic[compare_uid]) is not list:
                dummy.append(compare_uid)   
                features_dic[compare_uid] = [0.1 for _ in range(1280)]
            sim = find_sim(features_dic[base_uid],features_dic[compare_uid]).item()
            tmp.append((sim,compare_uid))
        tmp = sorted(tmp, reverse=True)[:20]
        sims_rank[base_uid] = tmp
    
    with open('./json/thumbnail_sims_rank.json','w') as fp:
        json.dump(sims_rank,fp)

if __name__ == "__main__":
    device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
    backbone = EfficientV2Backbone()
    extract_features(backbone, device)
    find_similarity_rank()