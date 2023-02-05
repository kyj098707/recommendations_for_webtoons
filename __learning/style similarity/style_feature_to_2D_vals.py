import torch
import torch.nn as nn
import torchvision.models as models
import torchvision.transforms as transforms
import os
from sklearn.manifold import TSNE
import torchvision.datasets as datasets
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox, TextArea

class Resnet(nn.Module):
    def __init__(self):
        super(Resnet, self).__init__()
        resnet = models.resnet50(pretrained=True)
        self.layer0 = nn.Sequential(*list(resnet.children())[0:1])
        self.layer1 = nn.Sequential(*list(resnet.children())[1:4])
        self.layer2 = nn.Sequential(*list(resnet.children())[4:5])
        self.layer3 = nn.Sequential(*list(resnet.children())[5:6])
        self.layer4 = nn.Sequential(*list(resnet.children())[6:7])
        self.layer5 = nn.Sequential(*list(resnet.children())[7:8])

    def forward(self, x):
        out_0 = self.layer0(x)
        out_1 = self.layer1(out_0)
        out_2 = self.layer2(out_1)
        out_3 = self.layer3(out_2)
        out_4 = self.layer4(out_3)
        out_5 = self.layer5(out_4)
        return out_0, out_1, out_2, out_3, out_4, out_5


class GramMatrix(nn.Module):
    def forward(self, input):
        b,c,h,w = input.size()
        F = input.view(b, c, h*w)
        G = torch.bmm(F, F.transpose(1,2))
        return G


def imscatter(x, y, image, zoom=1, show_by_thumnail=False, title='webtoon'):
    ax = plt.gca()
    plt.rc('font', family='Malgun Gothic')
    
    try:
        image = plt.imread(image)
    except TypeError:
        pass
    
    im = OffsetImage(image, zoom=zoom)

    x, y = np.atleast_1d(x, y)

    artists = []
    for x0, y0 in zip(x, y):
        whole_offset_img = (80, 0)
        whole_offset_txt = (80, -35)
        ab = AnnotationBbox(im, (x0, y0), xybox=whole_offset_img, xycoords='data',
                                boxcoords="offset points", frameon=False)

        if show_by_thumnail:
            offsetbox = TextArea(title,
                                 textprops=dict(size=7, ha='center',va='baseline'))
            ac = AnnotationBbox(offsetbox, (x0, y0),
                                xybox=whole_offset_txt,
                                xycoords='data',
                                boxcoords="offset points",
                                pad=0.4,
                                arrowprops=dict(
                                    arrowstyle="->",
                                    connectionstyle="angle,angleA=0,angleB=90,rad=3"
                                    )
                                )
            
            artists.append(ax.add_artist(ac))
        artists.append(ax.add_artist(ab))

    ax.update_datalim(np.column_stack([x, y]))
    ax.autoscale()

    return artists

def main():
    image_size = 128
    # 본 학습에 사용한 파일은, 공유폴더 참조해주세요.
    data_dir = r'D:\TEST\prep\data'
    data = datasets.ImageFolder(data_dir, transform=transforms.Compose([
                                                    transforms.Resize(image_size),
                                                    transforms.CenterCrop(image_size),
                                                    transforms.ToTensor()]))


    img_list = sorted([os.path.join(data_dir, dir) for dir in os.listdir(data_dir)])

    resnet = Resnet().cuda()
    for param in resnet.parameters():
        param.requires_grad = False

    total_arr = []
    label_arr = []

    # Style 정보를 추출, total_arr에 배열로 저장.
    for idx, (image, label) in enumerate(data):
        i = image.cuda()
        i = i.view(-1, i.size()[0], i.size()[1], i.size()[2])

        style_target = list(GramMatrix().cuda()(i) for i in resnet(i))

        arr = torch.cat([style_target[0].view(-1), style_target[1].view(-1), style_target[2].view(-1),
                         style_target[3].view(-1)], 0)
        gram = arr.cpu().data.numpy().reshape(1, -1)

        total_arr.append(gram.reshape(-1))
        label_arr.append(label)
        
        # for문 내 메모리 캐싱 해제
        del style_target
        del arr
        del gram
        torch.cuda.empty_cache()

        if idx % 50 == 0 and idx != 0:
            print(f'{idx} images style feature extracted..[{round(idx / len(data), 2) * 100}%]')
    print("\nImage style feature extraction done.\n")

    # T-SNE 차원축소
    # 이 부분에서, total_arr을 TSNE로 올리면서 ram leak 발생합니다... (4번폴더 내 131작품 기점으로 오류 발생)
    model = TSNE(n_components=2, init='pca', random_state=0, verbose=3, perplexity=100)
    result = model.fit_transform(total_arr)
    
    
    # 축소한 산점도 데이터 평균치 산출
    scatter_x = result[:, 0]
    scatter_y = result[:, 1]
    group = np.array(label_arr)
    avg_list = [(np.mean(scatter_x[np.where(group == x)]), np.mean(scatter_y[np.where(group == x)])) for x in
                np.unique(group)]


    # PLT 통한 좌표평면 이미지파일 생성
    for i in range(len(avg_list)):
        img_path = os.path.join(data_dir, os.path.split(img_list[i])[1], os.listdir(img_list[i])[0])
        imscatter(avg_list[i][0], avg_list[i][1], image=img_path, zoom=0, show_by_thumnail=True,
                  title=os.path.split(img_list[i])[1]+"\n"+str(avg_list[i]))
    xmin, xmax = plt.xlim()
    ymin, ymax = plt.ylim()
    plt.axis([xmin * 1.5, xmax * 1.5, ymin * 1.5, ymax * 1.5])
    plt.savefig("./graph.jpg")
    
    
    # DB 인입 테스트용 TXT 생성
    writetxt = ''
    for i in range(len(avg_list)):
        writetxt += os.path.split(img_list[i])[1] + "\t" + str(avg_list[i]) + '\n'
    with open(f"./summary.txt", "w", encoding="UTF-8") as file:
        file.write(writetxt)
        

if __name__ == '__main__':
    main()