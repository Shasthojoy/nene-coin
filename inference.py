import string
import os.path
from model import Alex
from image import clip_coin, show_bgrimg
import chainer.links as L
from chainer import serializers
from chainer import Variable
import numpy as np
import matplotlib.pyplot as plt
import seaborn
import cv2


def inference(img, model):
    IMAGE_SIZE = 128
    IN_CHANNELS = 1

    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.resize(img, (IMAGE_SIZE, IMAGE_SIZE))
    img = img / 255
    im = img.astype(np.float32).reshape(1, IN_CHANNELS, IMAGE_SIZE, IMAGE_SIZE)
    x = Variable(im)
    y = model.predictor(x)
    [pred] = y.data
    print(pred)
    recog = np.argmax(pred)
    return recog, im.reshape(IMAGE_SIZE, IMAGE_SIZE)


def main():
    model = L.Classifier(Alex())
    serializers.load_npz('./model/model.npz', model)

    for r, ds, fs in os.walk('./sample/00/'):
        for f in fs:
            filename = os.path.join(r, f)
            image, imgs = clip_coin(filename)
            show_bgrimg(image)

            count = 1
            for img in imgs:
                plt.subplot(3, 4, count)
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                recog, img = inference(img, model)
                img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
                plt.imshow(img)
                plt.title([
                    '  1_omote', '  1_ura',
                    '  5_omote', '  5_ura',
                    ' 10_omote', ' 10_ura',
                    ' 50_omote', ' 50_ura',
                    '100_omote', '100_ura',
                    '500_omote', '500_ura'][recog])
                count += 1
            plt.show()


if __name__ == '__main__':
    main()
