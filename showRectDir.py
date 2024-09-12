import matplotlib.pyplot as plt
import pdb
from PIL import Image
import random
import glob
import os

srcName = "valid"
dstName = "valid1"
imgDir =  srcName + "/images/"
saveImgDir =  dstName + "/images/"
saveLabelDir = dstName + "/labels/"

os.makedirs(saveImgDir)
os.makedirs(saveLabelDir)


fgs = {}

def plot_pics(img, boxes):
    # 显示图像和候选框，img是Image.Open()类型, boxes是Tensor类型
    plt.imshow(img)
    label_colors = [(213, 110, 89)]
    for i in range(len(boxes)):
        box = boxes[i]
        x, y, box_w, box_h = box[0], box[1], box[2]-box[0], box[3]-box[1]
        plt.gca().add_patch(plt.Rectangle(xy=(x, y), width=box_w, height=box_h,
                                          edgecolor=[c / 255 for c in label_colors[0]],
                                          fill=False, linewidth=2))
        #pdb.set_trace()
        #cropped_image = img.crop(box)
        #cropped_image.save("%s.jpg" % (i))
        #fgs.append(cropped_image)

    plt.show()

imgName = "test1/images/image_2d71388853d74775_jpeg.rf.5ca5cbab9e1e1ce4ed9a02b71809cb33.jpg"
labelName = "test1/labels/image_2d71388853d74775_jpeg.rf.5ca5cbab9e1e1ce4ed9a02b71809cb33.txt"

def getLabel(img, labelName):
    data2 = []
    w, h = img.size
    with open(labelName, 'r', encoding='utf-8') as infile:
        # 读取并转换标签
        for line in infile:
            data_line = line.strip("\n").split()
            #pdb.set_trace()
            boxes = [float(i) for i in data_line][1:]
            xc, yc, wc, hc = boxes[0], boxes[1], boxes[2], boxes[3]
            x = w * xc - 0.5 * w * wc
            y = h * yc - 0.5 * h * hc
            box_w, box_h = w * wc, h * hc
            data2.append([int(x), int(y), int(x+box_w), int(y+box_h), data_line[0]])
    return data2

for f in glob.glob(imgDir + "*.jpg"):
    img = Image.open(f)
    label_f = f.replace("images\\", "labels\\").replace(".jpg", ".txt")
    data2 = getLabel(img, label_f)
    for i in data2:
        label = i[-1]
        cropped_image = img.crop(i[:4])
        #cropped_image.save("%s.jpg" % (i))
        fgs.setdefault(label, [])
        fgs[label].append(cropped_image)
#pdb.set_trace()

img = Image.open(imgName)
data2 = getLabel(img, labelName)
plot_pics(img, data2)
#pdb.set_trace()

def isOverLap(fg, bt):
    x1, y1, x2, y2 = fg
    x3, y3, x4, y4 = bt[:4]
    if x2 < x3:
        return False
    if x1 > x4:
        return False
    if y2 < y3:
        return False
    if y1 > y4:
        return False
    return True

def judgeInter(fg, bts):
    flag = False
    for bt in bts:
        overlapFlag = isOverLap(fg, bt)
        if overlapFlag:
            flag = True
            return True
    return flag

def convert(img_size, box):
    dw = 1./(img_size[0])
    dh = 1./(img_size[1])
    x = (box[0] + box[2])/2.0 - 1
    y = (box[1] + box[3])/2.0 - 1
    w = box[2] - box[0]
    h = box[3] - box[1]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h)

#bg_name = "train/images/image_0a11179ca17a4a47_jpeg.rf.28dcbd9d925443094eaf468b475b99e0.jpg"
#bg_label_name = "train/labels/image_0a11179ca17a4a47_jpeg.rf.28dcbd9d925443094eaf468b475b99e0.txt"


for f in glob.glob(imgDir + "*.jpg"):
    bg = Image.open(f)
    label_f = f.replace("images\\", "labels\\").replace(".jpg", ".txt")

    saveLabelf = label_f.replace(srcName, dstName)
    fpsavelabel = open(saveLabelf, "w")
    bg_w, bg_h = bg.size
    bg_boxs = getLabel(bg, label_f)
    interFlag = True

    randLabel = random.sample(fgs.keys(), 1)[0]
    fgImg = random.sample(fgs[randLabel], 1)[0]
    fg_w, fg_h = fgImg.size
    while True:
        offset_x = random.randint(10, bg_w - 100)
        if fg_w > 500:
            offset_x = 2
        offset_y = random.randint(10, bg_h - 100)
        interFlag = judgeInter([offset_x, offset_y, offset_x + fg_w, offset_y + fg_h], bg_boxs)
        if not interFlag:
            bg.paste(fgImg, (offset_x, offset_y))
            bg.save(f.replace(srcName, dstName))

            x, y, w, h = convert(bg.size, [offset_x, offset_y, offset_x + fg_w, offset_y + fg_h])
            linesave = "%s %s %s %s %s\n" % (randLabel, x, y, w, h)
            fpsavelabel.write(open(label_f, "r").read().strip() + "\n" + linesave)
            break
    fpsavelabel.close()
    #if randLabel == '10':
    #    pdb.set_trace()