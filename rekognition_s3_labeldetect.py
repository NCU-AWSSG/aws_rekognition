#!/usr/bin/env python
# coding: utf-8

# In[9]:


# error log
import logging
# connect aws
import boto3
# error report
from botocore.exceptions import ClientError

#　查看 S3的資源狀況
s3 = boto3.resource('s3')
print(s3)
buckets = s3.buckets.all()
print(buckets)
for buc in buckets:
    print(buc.name)

# 
BUCKET = "amazon-rekognition-fdj612" # can be other bucket listed
my_bucket = s3.Bucket(BUCKET)
file = []
# 撈出bucket中所有圖片
for my_bucket_object in my_bucket.objects.all():
    # 每張圖片中的 key值為當初丟上去時給的 object name(即file name)
    key = my_bucket_object.key
    if(".jpg" in key) or (".png" in key):
        file.append(key)
print(file)

# 將S3 bucket中的圖片丟到 AWS Rekognition，然後回傳結果的分析 Label的 json格式
def detect_labels(bucket, key, max_labels=20, min_confidence=50, region="eu-west-1"):
    rekognition = boto3.client("rekognition", region)
    # Image=Image("C:/Users/fdj61/Desktop/cat.jpg")-->不行
    response = rekognition.detect_labels(
        Image={
            "S3Object": {
                "Bucket": bucket,
                "Name": key,
            }
        },
        # 最多回傳 label數
        MaxLabels=max_labels,
        # 最少要多少信心指數
        MinConfidence=min_confidence,
    )
    return response['Labels']

# 每張圖片中的 key值為當初丟上去時給的 object name(即file name)
for pic in file:
    print("\n" + pic)
    # 根據回傳的 json檔，挑出需要的資訊印出
    for label in detect_labels(BUCKET, pic):
        print('%15s - %.1f' % (label['Name'], label['Confidence']) + "%")


# In[ ]:




