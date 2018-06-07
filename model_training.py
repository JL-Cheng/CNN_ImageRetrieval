# coding=gbk

import os
import numpy as np
import tensorflow as tf

import CNN_model as model
import image_preprocessing as image_P

#ͼƬ������
N_CLASSES=10
#ͼƬ�ߴ�
IMG_W=400
IMG_H=300

BATCH_SIZE=8
CAPACITY=64

#����������
MAX_STEP=1000

#ѧϰ����
learning_rate=0.0001

def run_training():
    #Ŀ¼
    train_dir="./image/image/"
    logs_train_dir ="./log"

    train,train_label=image_P.get_files(train_dir)
    train_batch,train_label_batch=image_P.get_batch(train,
                                            train_label,
                                            IMG_W,
                                            IMG_H,
                                            BATCH_SIZE,
                                            CAPACITY)
    train_logits=model.inference(train_batch,BATCH_SIZE,N_CLASSES)
    train_loss=model.losses(train_logits,train_label_batch)
    train_op=model.trainning(train_loss,learning_rate)
    train_acc=model.evaluation(train_logits,train_label_batch)

    summary_op=tf.summary.merge_all()

    sess=tf.Session()
    train_writer=tf.summary.FileWriter(logs_train_dir,sess.graph)
    #����ģ��
    saver=tf.train.Saver()

    #��ʼ��
    sess.run(tf.global_variables_initializer())

    #ʹ�ö��߳�
    coord=tf.train.Coordinator()
    threads=tf.train.start_queue_runners(sess=sess,coord=coord)

    try:
        for step in np.arange(MAX_STEP):
            if coord.should_stop():
                break#�߳�ֹͣ
            _,temp_loss,temp_acc=sess.run([train_op,train_loss,train_acc])
            
            #ÿ����50�δ�ӡһ�ν��
            if step%50 == 0:
                print('Step %d,train loss = %.2f,train occuracy = %.2f'%(step,temp_loss,temp_acc))
                summary_str=sess.run(summary_op)
                train_writer.add_summary(summary_str,step)
            
            #ÿ����200�λ򵽴����һ�α���һ��ģ��
            if step%200 == 0 or (step+1) == MAX_STEP:
                checkpoint_path=os.path.join(logs_train_dir,'model.ckpt')
                saver.save(sess,checkpoint_path,global_step=step)
    except tf.errors.OutOfRangeError:
        print('Failed!')
    finally:
        coord.request_stop()

    #�����߳�
    coord.join(threads)

    sess.close()

run_training()