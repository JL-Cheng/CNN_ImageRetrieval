# coding=gbk

#����VGG16ģ��
from keras.applications.vgg16 import VGG16

#��������ģ��
from keras.layers import Input
from keras.layers import Flatten
from keras.layers import Dense
from keras.layers import Dropout
from keras.models import Model
from keras.optimizers import SGD
from keras.utils.np_utils import to_categorical

#ѵ��ͼƬ
import image_preprocessing as image_P

import matplotlib.pyplot as plt
from PIL import Image
import h5py as h5py
import numpy as np

#ͼƬ������
N_CLASSES=10
#ͼƬ�ߴ�
IMG_W=400
IMG_H=300

BATCH_SIZE=8
CAPACITY=4096

#����������
MAX_STEP=100

#ѧϰ����
learning_rate=0.0001

#Ŀ¼
train_dir="./image/image/"
log_dir="./VGG_log/VGG_model.h5"

#ģ�͹���
model_vgg=VGG16(include_top=False,weights='imagenet',input_shape=(IMG_H,IMG_W,3))
for layer in model_vgg.layers:
    layer.trainable=False
model=Flatten()(model_vgg.output)
model = Dense(4096, activation='relu', name='fc1')(model)
model = Dense(4096, activation='relu', name='fc2')(model)
model=Dropout(0.5)(model)
model=Dense(10,activation='softmax', name='prediction')(model)

model_vgg_train=Model(inputs=model_vgg.input,outputs=model, name='vgg16')
model_vgg_train.summary()

#�趨��ʧ����
sgd=SGD(lr=learning_rate,decay=1e-5)
model_vgg_train.compile(loss='categorical_crossentropy',
                        optimizer=sgd,metrics=['accuracy'])


#��������
def get_train_batch(X_train,Y_train,img_w,img_h):
    i=0
    while 1:
        x=[]
        y=[]
        image=Image.open(X_train[i])
        image=image.resize([img_w,img_h])
        x.append(np.array(image))
        y.append(to_categorical(Y_train[i],N_CLASSES))
        i=(i+1)%len(X_train)
        x=np.array(x)
        y=np.array(y)
        yield(x,y)

train,train_label=image_P.get_files(train_dir)

model_vgg_train.fit_generator(get_train_batch(train,
                    train_label,IMG_W,IMG_H),
                    steps_per_epoch=BATCH_SIZE,
                    epochs=MAX_STEP)

model_vgg_train.save(log_dir)
