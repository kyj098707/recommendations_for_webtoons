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

class EfficientV2Base(nn.Module):
    def __init__(self, num_classes=5):
        super().__init__()
        self.backbone = timm.create_model('tf_efficientnetv2_m', pretrained=True)

    def forward(self, x):
        x = torch.sigmoid(self.backbone(x))
        return x

class EfficientV2(nn.Module):
    def __init__(self, num_classes=165):
        super().__init__()
        self.backbone = timm.create_model('tf_efficientnetv2_m', pretrained=True, num_classes=num_classes)
        nn.init.xavier_normal_(self.backbone.classifier.weight)
    def forward(self, x):
        x = torch.sigmoid(self.backbone(x))
        return x

class EfficientV2Backbone(nn.Module):
    def __init__(self, num_classes=5):
        super().__init__()
        self.backbone = torch.load("./comic_165abel_3.pth")
        self.backbone.backbone.classifier = nn.Identity()

    def forward(self, x):
        x = self.backbone(x)
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

if __name__ == "__main__":
    folder_list = list(map(lambda x: x.split('\\')[-1], glob("./data/*")))
    device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
    model = torch.load("./comic_165label.pth")
    newmodel = EfficientV2Backbone(model)
    features_dic = {}
    img1 = sorted(glob(f"./data/N_15439/*.jpg"))[1:]
    img2 = sorted(glob(f"./data/N_15441/*.jpg"))[1:]
    #print(img1)
    test_transform = A.Compose([A.Resize(480, 480),
                                A.Normalize(mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225), max_pixel_value=255.0, always_apply=False, p=1.0),
                                ToTensorV2()])
    test_dataset1 = CustomDataset(img1, None, test_transform)
    test_loader1 = DataLoader(test_dataset1, batch_size = 16, shuffle=False)
    test_dataset2 = CustomDataset(img2, None, test_transform)
    test_loader2 = DataLoader(test_dataset2, batch_size = 16, shuffle=False)

    preds1 = infer(newmodel, test_loader1, device)
    preds2 = infer(newmodel, test_loader2, device)
    #print(preds1)
    #print(preds2)
    sim = util.cos_sim(preds1,[preds1,preds2])
    print(sim.shape)

