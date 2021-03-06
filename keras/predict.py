import os
import sys
from model import get_model
from keras.callbacks import ModelCheckpoint, EarlyStopping
import numpy as np
import matplotlib.pyplot as plt
import seaborn
import cv2

sys.path.append(os.path.join(os.path.dirname(__file__), '../utility/'))
from image import clip_coin, adjust_gamma, normalize_image, show_bgrimg, IMAGE_SIZE


def softmax(a):
    c = np.max(a)
    exp_a = np.exp(a - c)
    sum_exp_a = np.sum(exp_a)
    y = exp_a / sum_exp_a
    return y


def predict(img, model, in_channels):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    if in_channels == 1:
        img = normalize_image(img)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    else:
        img = adjust_gamma(img)
    img = cv2.resize(img, IMAGE_SIZE)
    img = img / 255
    im = img.astype(np.float32).reshape(
        1, IMAGE_SIZE[0], IMAGE_SIZE[1], in_channels)
    y = model.predict([im])
    [pred] = y
    pred = softmax(pred)
    print(('[{:.5f} {:.5f}]  ' * (len(pred) // 2)).format(*pred))
    return pred, img


def main():
    IN_CHANNELS = 3
    model = get_model(IN_CHANNELS)
    model.load_weights('./model/model_color.hdf5')

    for r, ds, fs in os.walk('../sample/0001/'):
        for f in fs:
            filename = os.path.join(r, f)
            image, imgs = clip_coin(filename)
            show_bgrimg(image)

            count = 1
            for img in imgs:
                if 12 < count:
                    break
                plt.subplot(3, 4, count)
                pred, img_ = predict(img, model, IN_CHANNELS)
                recog = np.argmax(pred)
                plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
                plt.title([
                    '  1_omote', '  1_ura',
                    '  5_omote', '  5_ura',
                    ' 10_omote', ' 10_ura',
                    ' 50_omote', ' 50_ura',
                    '100_omote', '100_ura',
                    '500_omote', '500_ura'][recog])
                plt.axis('off')
                count += 1
            plt.show()


if __name__ == '__main__':
    main()
