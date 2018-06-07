# coding=gbk

import os
import numpy as np
import tensorflow as tf
from PIL import Image

#ѵ��ͼƬ��·��
train_dir="./image/image/"

#��ȡÿ��ͼƬ����Ϣ�ͱ�ǩ
def get_files(file_dir):
    #���ڴ�Ÿ������ݺͱ�ǩ
    All_Image=[[] for i in range(10)]
    All_Label=[[] for i in range(10)]

    #����ͼƬ���ƺͱ�ǩ���л���
    for file in os.listdir(file_dir):
        name=file.split(sep='_')
        if name[0]=='n03877845':
            All_Image[0].append(file_dir+file)
            All_Label[0].append(0)
        elif name[0]=='n02278980':
            All_Image[1].append(file_dir+file)
            All_Label[1].append(1)
        elif name[0]=='n11669921':
            All_Image[2].append(file_dir+file)
            All_Label[2].append(2)
        elif name[0]=='n01613177':
            All_Image[3].append(file_dir+file)
            All_Label[3].append(3)
        elif name[0]=='n01923025':
            All_Image[4].append(file_dir+file)
            All_Label[4].append(4)
        elif name[0]=='n04515003':
            All_Image[5].append(file_dir+file)
            All_Label[5].append(5)
        elif name[0]=='n04583620':
            All_Image[6].append(file_dir+file)
            All_Label[6].append(6)
        elif name[0]=='n03767203':
            All_Image[7].append(file_dir+file)
            All_Label[7].append(7)
        elif name[0]=='n07897438':
            All_Image[8].append(file_dir+file)
            All_Label[8].append(8)
        elif name[0]=='n10247358':
            All_Image[9].append(file_dir+file)
            All_Label[9].append(9)

    #ˮƽ�ϲ�����
    Image_List=np.hstack(All_Image[i] for i in range(10))
    Label_List=np.hstack(All_Label[i] for i in range(10))

    #ת�ú��������
    temp=np.array([Image_List,Label_List])
    temp=temp.transpose()
    np.random.shuffle(temp)

    Image_List=list(temp[:,0])
    Label_List=list(temp[:,1])
    Label_List=[int(i) for i in Label_List]

    #��������list
    return Image_List,Label_List

#��������ѵ������
def get_batch(image,label,image_W,image_H,batch_size,capacity):
    #��������ת��
    image=tf.cast(image,tf.string)
    label=tf.cast(label,tf.int32)

    #�������
    input_queue=tf.train.slice_input_producer([image,label])

    label=input_queue[1]
    image_content=tf.read_file(input_queue[0])
    image=tf.image.decode_jpeg(image_content,channels=3)

    #ͼ���Сresizeһ�²����б�׼������
    image=tf.image.resize_image_with_crop_or_pad(image,image_W,image_H)
    image=tf.image.per_image_standardization(image)

    image_batch,label_batch=tf.train.batch([image,label],batch_size=batch_size,num_threads=16,capacity=capacity)

    label_batch=tf.reshape(label_batch,[batch_size])

    return image_batch,label_batch

