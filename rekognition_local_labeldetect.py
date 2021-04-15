#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import boto3
import os


# In[ ]:


path = 'C:/Users/fdj61/Desktop/image_rekognition'
arr = os.listdir(path)
files = []
for a in arr:
    if(".jpg" in a) or (".png" in a):
        files.append(path+"/"+a)
files


# In[ ]:


# 分析標籤
def detect_labels_local_file(photo):
    client=boto3.client('rekognition')
    
    with open(photo, 'rb') as image:
        response = client.detect_labels(Image={'Bytes': image.read()})
        print('*Detected labels in ' + photo)
    
    for label in response['Labels']:
        print (label['Name'] + ' : ' + str(label['Confidence']))
    
    return len(response['Labels'])


# In[ ]:


# 可自訂在本機中的圖片檔案位置
for photo in files:
    label_count=detect_labels_local_file(photo)
    print("Labels detected: " + str(label_count))


# In[ ]:


#　查看 S3的資源狀況
s3 = boto3.resource('s3')
print(s3)
buckets = s3.buckets.all()
print(buckets)
for buc in buckets:
    print(buc.name)


# In[ ]:


# 上傳檔案到 S3 bucket
# 給 file path、要存的 bucket名稱、object name
def upload_file(file_name, bucket, object_name=None):
    # 如果物件名稱沒有指定，就跟檔案名稱設一樣
    if object_name is None:
        object_name = file_name

    # 連接 s3
    s3_client = boto3.client('s3')
    # 除錯
    try:
        # 根據收到的參數設定上傳的參數
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True


# 設定 bucket名稱
BUCKET = "bucketforrekognition"
for f in files:
    upload_file(path + f, BUCKET, f)

