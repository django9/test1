import matplotlib.pyplot as plt
import pdb
from PIL import Image
import torch

def plot_pics(img, boxes):
    # 显示图像和候选框，img是Image.Open()类型, boxes是Tensor类型
    plt.imshow(img)
    label_colors = [(213, 110, 89)]
    w, h = img.size
    boxes = torch.tensor(boxes)
    for i in range(boxes.shape[0]):
        box = boxes[i, 1:]
        xc, yc, wc, hc = box
        x = w * xc - 0.5 * w * wc
        y = h * yc - 0.5 * h * hc
        box_w, box_h = w * wc, h * hc
        plt.gca().add_patch(plt.Rectangle(xy=(x, y), width=box_w, height=box_h,
                                          edgecolor=[c / 255 for c in label_colors[0]],
                                          fill=False, linewidth=2))
    plt.show()

imgName = "train/images/image_0a679a4a8b5e4001_jpeg.rf.289e1d450e46656d48ea4790d6c08315.jpg"
label = "train/labels/image_0a679a4a8b5e4001_jpeg.rf.289e1d450e46656d48ea4790d6c08315.txt"


data2 = []
with open(label, 'r', encoding='utf-8') as infile:
    # 读取并转换标签
    for line in infile:
        data_line = line.strip("\n").split()
        data2.append([float(i) for i in data_line])

img = Image.open(imgName)

plot_pics(img, data2)
pdb.set_trace()
