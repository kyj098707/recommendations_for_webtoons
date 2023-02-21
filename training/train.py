import pandas as pd
import numpy as np
import os
import argparse
from copy import deepcopy
from valid import valid

import torch.optim as optim
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader

import albumentations as A
from albumentations.pytorch.transforms import ToTensorV2

from tqdm.auto import tqdm

import timm

import cv2

import random
import wandb
import warnings
warnings.filterwarnings(action='ignore') 


def seed_everything(seed):
    random.seed(seed)
    os.environ['PYTHONHASHSEED'] = str(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = True
    

def get_labels(df):
    return df.iloc[:,2:].values

class EfficientV2(nn.Module):
    def __init__(self, num_classes=165):
        super().__init__()
        self.backbone = timm.create_model('tf_efficientnetv2_m', pretrained=True, num_classes=num_classes)
        nn.init.xavier_normal_(self.backbone.classifier.weight)
    def forward(self, x):
        x = torch.sigmoid(self.backbone(x))
        return x

class EfficientV2Tiny(nn.Module):
    def __init__(self, num_classes=165):
        super().__init__()
        self.backbone = timm.create_model('tf_efficientnetv2_s', pretrained=True, num_classes=num_classes)
        nn.init.xavier_normal_(self.backbone.classifier.weight)
    def forward(self, x):
        x = torch.sigmoid(self.backbone(x))
        return x

class CustomDataset(Dataset):
    def __init__(self, img_path_list, label_list, transforms=None):
        self.img_path_list = img_path_list
        self.label_list = label_list
        self.transforms = transforms
        
    def __getitem__(self, index):
        img_path = self.img_path_list[index]
        
        image = cv2.imread(img_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        if self.transforms is not None:
            image = self.transforms(image=image)['image']
        
        if self.label_list is not None:
            label = torch.FloatTensor(self.label_list[index])
            return image, label
        else:
            return image
        
    def __len__(self):
        return len(self.img_path_list)

def validation(model, criterion, val_loader, device):
    model.eval()
    val_loss = []
    val_acc = []
    classes_acc = []
    with torch.no_grad():
        for imgs, labels in tqdm(iter(val_loader)):
            imgs = imgs.float().to(device)
            labels = labels.to(device)
            
            probs = model(imgs)
            
            loss = criterion(probs, labels)
            
            probs  = probs.cpu().detach().numpy()
            labels = labels.cpu().detach().numpy()
            
            preds = probs > 0.5
            batch_acc = (labels == preds).mean()
            class_acc = [labels[i] == preds[i] for i in range(len(labels))]

            val_acc.append(batch_acc)
            val_loss.append(loss.item())
            classes_acc.append(np.mean(class_acc,axis=0))
        
        _classes_acc = np.mean(classes_acc, axis=0)
        _val_loss = np.mean(val_loss)
        _val_acc = np.mean(val_acc)
    
    return _val_loss, _val_acc, _classes_acc


def train(args):
    CLASSES = ['N_103759', 'N_112931', 'N_113119', 'N_119874', 'N_131385',\
            'N_15441', 'N_15938', 'N_160469', 'N_169080', 'N_183559', 'N_21815',\
            'N_22043', 'N_22052', 'N_226807', 'N_23182', 'N_24530', 'N_25613',\
            'N_259893', 'N_26671', 'N_297796', 'N_316909', 'N_316914', 'N_318995',\
            'N_325630', 'N_325631', 'N_332797', 'N_374973', 'N_400739', 'N_471283',\
            'N_502673', 'N_51006', 'N_51007', 'N_517252', 'N_524520', 'N_528785', 'N_52946',\
            'N_551650', 'N_552960', 'N_570503', 'N_570506', 'N_579352', 'N_597447', 'N_597478',\
            'N_602910', 'N_602916', 'N_616239', 'N_61731', 'N_626949', 'N_641253', 'N_642598', 'N_644112',\
            'N_644180', 'N_646358', 'N_648419', 'N_64997', 'N_650305', 'N_651664', 'N_651665', 'N_651675',\
            'N_654138', 'N_654774', 'N_654809', 'N_655746', 'N_659934', 'N_667573', 'N_670140', 'N_670143',\
            'N_670145', 'N_671421', 'N_676695', 'N_678494', 'N_679543', 'N_682637', 'N_687915', 'N_695796',\
            'N_698918', 'N_701535', 'N_701700', 'N_702608', 'N_703630', 'N_703839', 'N_703844', 'N_703846',\
            'N_708453', 'N_710747', 'N_710751', 'N_711422', 'N_712362', 'N_714834', 'N_717481', 'N_719508',\
            'N_721433', 'N_721948', 'N_723046', 'N_724431', 'N_724815', 'N_72497', 'N_725586', 'N_725829',\
            'N_727188', 'N_728126', 'N_728128', 'N_728750', 'N_729036', 'N_729047', 'N_729963', 'N_729964',\
            'N_730174', 'N_730425', 'N_730607', 'N_730656', 'N_730657', 'N_730694', 'N_732021', 'N_732036',\
            'N_732988', 'N_733034', 'N_733074', 'N_733277', 'N_733280', 'N_735661', 'N_735979', 'N_736277',\
            'N_737628', 'N_738174', 'N_738487', 'N_738694', 'N_739115', 'N_740034', 'N_741449', 'N_741825',\
            'N_741891', 'N_742351', 'N_743139', 'N_743838', 'N_745589', 'N_745654', 'N_745876', 'N_746534',\
            'N_746833', 'N_746834', 'N_746857', 'N_747269', 'N_747271', 'N_748105', 'N_748535', 'N_748536',\
            'N_750184', 'N_750558', 'N_750826', 'N_751168', 'N_751993', 'N_751999', 'N_753304', 'N_753478',\
            'N_753839', 'N_754876', 'N_755668', 'N_758150', 'N_759567', 'N_761461', 'N_762035', 'N_790713', 'N_81482', 'N_89097']

    device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
    early_stop = 0

    ## 데이터 셋 설정
    df = pd.read_csv('./comic.csv')
    df = df.sample(frac=1)
    
    train_labels = get_labels(df)
    
    
    train_transform = A.Compose([
                            A.Resize(args.img_size,args.img_size),
                            A.Normalize(mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225), max_pixel_value=255.0, always_apply=False, p=1.0),
                            ToTensorV2()
                        ])
    
    train_dataset = CustomDataset(df['img_path'].values, train_labels, train_transform)
    train_loader = DataLoader(train_dataset, batch_size = args.batch_size, shuffle=True, num_workers=args.num_workers)

    
    model = EfficientV2Tiny()
    model.to(device)
    
    optimizer = optim.Adam(params = model.parameters(), lr = args.lr)
    scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer=optimizer,
                                                     mode='max',
                                                     factor=0.5,
                                                     patience=3,
                                                     cooldown=5,
                                                     min_lr=1e-9,
                                                     threshold_mode='abs',
                                                     )

    best_similarity = 0
    best_model = None
    
    criterion = nn.BCELoss().to(device)
    print(optimizer.param_groups[0]['lr'])


    for epoch in range(1, args.epochs+1):
        model.train()
        train_loss = []
        for imgs, labels in tqdm(iter(train_loader)):
            imgs = imgs.float().to(device)
            labels = labels.to(device)
            
            optimizer.zero_grad()
            
            output = model(imgs)
            loss = criterion(output, labels)
            
            loss.backward()
            nn.utils.clip_grad_norm_(model.parameters(), args.clip)
            optimizer.step()
            
            train_loss.append(loss.item())
                    
        _trained_artworks_similarity, _untrained_artworks_similarity = valid(model)
        _train_loss = np.mean(train_loss)
        
        print(f'Epoch [{epoch}], Train Loss : [{_train_loss:.5f}] Val Loss : [{_trained_artworks_similarity:.5f}] Val ACC : [{_untrained_artworks_similarity:.5f}]')
        
            
        if best_similarity < _untrained_artworks_similarity:
            best_similarity = _untrained_artworks_similarity
            best_model = deepcopy(model)
            early_stop = 0
        else:
            early_stop += 1
        log_dic = {}
            
        log_dic["trained similarity"] = _trained_artworks_similarity
        log_dic["untrained similarity"] = _untrained_artworks_similarity
        wandb.log(log_dic)
        
        if early_stop > 5:
            break

    torch.save(best_model, f'./tiny_comic_165abel_{epoch}.pth')

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--seed', type=int, default=777)
    parser.add_argument('--epochs', type=int, default=20)
    parser.add_argument('--lr', type=float, default=3e-4)
    parser.add_argument('--img_size', type=int, default=384)
    parser.add_argument('--num_workers', type=int, default=4) 
    parser.add_argument('--batch_size', type=int, default=32)
    parser.add_argument('--model_name', default="ConvNext")
    parser.add_argument('--detail', default="xlarge_384")
    parser.add_argument('--makecsvfile', type=bool ,default=False)
    parser.add_argument('--ckpt', default=None)
    parser.add_argument('--clip', default=1)
    # parser.add_argument('--checkpoints', default="microsoft/beit-base-patch16-224-pt22k-ft22k")
    args = parser.parse_args()
    
    seed_everything(args.seed)
    
    wandb.init(
        entity="aivle_comic",
        project=args.model_name,
        name=args.detail,
        config={"epochs": args.epochs, "batch_size": args.batch_size}
    )
      
    train(args)