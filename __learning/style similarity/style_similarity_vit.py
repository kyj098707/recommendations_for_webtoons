# huggingface 사용할 때 필요한 package, install 후 사용 가능
import transformers
from transformers import ViTForImageClassification

import torch
from torch.utils.data import Dataset, DataLoader

import albumentations as A
from albumentations.pytorch.transforms import ToTensorV2

import cv2
from glob import glob
from tqdm.auto import tqdm

from sentence_transformers import util

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
        for imgs in tqdm(iter(test_loader)):
            imgs = imgs.float().to(device)
            
            probs = model(imgs).logits
            probs  = probs.cpu().detach().numpy()
            preds = probs.astype(float)
            predictions += preds.tolist() 
    return predictions


if __name__ == "__main__":
    device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
    img = sorted(glob("../../dataset/style/d/*.jpg"))
    # 사전 학습 모델 받아오기
    checkpoints = "jayanta/google-vit-base-patch16-224-cartoon-emotion-detection"
    model = ViTForImageClassification.from_pretrained(checkpoints)
    test_transform = A.Compose([A.Resize(224, 224),
                                A.Normalize(mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225), max_pixel_value=255.0, always_apply=False, p=1.0),
                                ToTensorV2()])
    test_dataset = CustomDataset(img, None, test_transform)
    test_loader = DataLoader(test_dataset, batch_size = 16, shuffle=False)

    device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
    preds = infer(model, test_loader, device)
    similarity = util.cos_sim(preds,preds)
    print(similarity)
    print(similarity.numpy().mean())