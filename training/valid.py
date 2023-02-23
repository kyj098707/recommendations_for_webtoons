import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader

import albumentations as A
from albumentations.pytorch.transforms import ToTensorV2

import cv2
from glob import glob
from tqdm.auto import tqdm

from sentence_transformers import util
import timm

from util import *


def valid(model):
    device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
    classes_set = set(get_classes())

    trained_sims_list = []
    untrained_sims_list = []
    folder_list = list(map(lambda x: x.split('\\')[-1], glob("./data/*")))
    test_transform = A.Compose([A.Resize(480, 480),
                                    A.Normalize(mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225), max_pixel_value=255.0, always_apply=False, p=1.0),
                                    ToTensorV2()])
    backbone = EfficientV2Backbone(model)
    for folder in tqdm(folder_list):
        img = sorted(glob(f"./data/{folder}/*.jpg"))[1:]
        if len(img) < 10:
            continue
        test_dataset = CustomDataset(img, None, test_transform)
        test_loader = DataLoader(test_dataset, batch_size = 16, shuffle=False)
        
        preds = infer(backbone, test_loader, device)
        similarity = util.cos_sim(preds,preds)
        mean_similarity = similarity.numpy().mean()
        if folder in classes_set:
            trained_sims_list.append(mean_similarity)
        else:
            untrained_sims_list.append(mean_similarity)

    return trained_sims_list,untrained_sims_list

if __name__ == "__main__":
    model = torch.load("./ckpt/comic_165label.pth")
    trained_sims_list,untrained_sims_list = valid(model)
    print(f"학습된 데이터에 대한 유사도 평균 : {sum(trained_sims_list)/len(trained_sims_list)}")
    print(f"학습되지 않은 데이터에 대한 유사도 평균 : {sum(untrained_sims_list)/len(untrained_sims_list)}")