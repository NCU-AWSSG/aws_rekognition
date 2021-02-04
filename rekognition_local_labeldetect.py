#!/usr/bin/env python
# coding: utf-8

# In[2]:


import boto3

# 分析標籤
def detect_labels_local_file(photo):
    client=boto3.client('rekognition')
    
    with open(photo, 'rb') as image:
        response = client.detect_labels(Image={'Bytes': image.read()})
        print('Detected labels in ' + photo)
    
    for label in response['Labels']:
        print (label['Name'] + ' : ' + str(label['Confidence']))
    
    return len(response['Labels'])

def main():
    # 可自訂在本機中的圖片檔案位置
    photo="C:/Users/fdj61/Desktop/cat.jpg"
    label_count=detect_labels_local_file(photo)
    print("Labels detected: " + str(label_count))
    
if __name__ == "__main__":
    main()


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

# from IPython.display import Image # display picture用

# 設定檔案位置與名稱 
path = "C:/Users/fdj61/Desktop/"
file = ["cat.jpg", "dog.jpg"]
for f in file:
    upload_file(path + f,"amazon-rekognition-fdj612", f)

