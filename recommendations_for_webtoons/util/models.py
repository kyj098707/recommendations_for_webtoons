import torch
import torch.nn as nn
import timm

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
