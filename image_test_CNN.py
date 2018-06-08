# coding=gbk

import os
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import tensorflow as tf
import CNN_model as model

def get_one_image(img_dir):
    image=Image.open(img_dir)
    image=image.resize([400,300])
    image_arr = np.array(image)

    return image_arr

def images_show(images):
    images_dir='./image/image/'
    plt.subplots(num='result pictures window',figsize=(8,6))
    for i in range(10):
        image=Image.open(images_dir+images[i][0])
        image=image.resize([image.width*5,image.height*5])
        plt.subplot(2,5,1+i)
        plt.axis('off')
        plt.imshow(image)
    plt.suptitle('result pictures')
    plt.show()
    
def test():
    images_dir='./image/image/'
    log_dir='./log/'

    images_cat=open("imagelist.txt")
    #��������ͼ�񾭹�ģ�ͼ���֮�������
    images_tested=[]

    with tf.Graph().as_default():
        #����ģ��
        x=tf.placeholder(tf.float32,shape=[1,300,400,3])
        p=model.inference(x,1,10)
        logits=tf.nn.softmax(p)

        sess=tf.Session()
        tf.get_variable_scope().reuse_variables()
        ckpt=tf.train.get_checkpoint_state(log_dir)
        saver=tf.train.Saver()
        if ckpt and ckpt.model_checkpoint_path:
            global_step = ckpt.model_checkpoint_path.split('/')[-1].split('-')[-1]
            saver.restore(sess, ckpt.model_checkpoint_path)
            print('Loading success!')
        else:
            print('Loading failed!')
        for line in images_cat.readlines():
            image_name=line.strip('\n')
            image_array=get_one_image(images_dir+image_name)
            image_array=np.reshape(image_array,[1,300,400,3])                 
  
            prediction=sess.run(logits,feed_dict={x:image_array})
            prediction=np.array(prediction,dtype='float32')
            images_tested.append([image_name,prediction])

            print(image_name)
            print(prediction)
        
        #���Ե���ͼƬ
        while (True):
            test_file=input('�������ͼƬ:')
            if(test_file=='z'):
                break

            image_name=test_file
            image_array=get_one_image(images_dir+image_name)
            image_array=np.reshape(image_array,[1,300,400,3])
            prediction=sess.run(logits,feed_dict={x:image_array})
            prediction=np.array(prediction,dtype='float32')
            test_result=[]
            for sample in images_tested:
                distance=np.sqrt(np.sum(np.square(sample[1]-prediction)));
                distance.astype('float32')
                test_result.append([sample[0],distance])
                                
            #���������
            test_result=np.array(test_result)
            test_result=test_result[np.lexsort(test_result.T)]
            for i in range(10):
                print(test_result[i][0])

            images_show(test_result)

test()