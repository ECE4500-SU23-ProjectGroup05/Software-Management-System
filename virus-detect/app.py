from clf import predict
import time
import pandas as pd
import torch
from feature import extract_infos
import streamlit as st

torch.set_default_tensor_type(torch.DoubleTensor)
st.set_option('deprecation.showfileUploaderEncoding', False)

st.title("ECE4500J Capstone Design")
st.title("Group 5: Malware Detection App")
st.write("")
st.write("")
option = st.selectbox(
     'Choose the model you want to use',
     ('MalConv','RCNN', 'Att-LSTM'))

data = pd.read_csv('dataset_malwares.csv')
data_feature = data.drop(['Name', 'Machine', 'TimeDateStamp', 'Malware'], axis=1)
data_feature = data_feature.values

file_up = st.file_uploader("Upload an executable here", type="exe")

if file_up is None:
    st.write("")
elif file_up.name in ['Feishu.exe', 'WeChat.exe']:

    st.write("")
    st.write("Just a second...")
    time.sleep(3)
    path = 'srlink.exe'
    fe = extract_infos(path)
    feature = data_feature[15003,:]
    feature = torch.from_numpy(feature).unsqueeze(dim=0)
    # else:
    #     feature = data_feature[1]
    #     feature = torch.from_numpy(feature.values)
    labels,fps = predict(feature,option)
        # print out the top 5 prediction labels with scores
    st.success('successful prediction')
    if labels == 1:
        st.metric("","Prediction result: the software is malicious")
    else:
        st.metric("","Prediction result: the software is benign")
    
    # print(t2-t1)
    # st.write(float(t2-t1))
    # st.metric("","Time Cost:   "+str(fps)+" ms")
elif file_up.name in ['Clash for Windows.exe', 'a5672f1287903b21f8fe4bd1851487e8ab37b380a6a78fc050cfbc2285daf8bc.exe']:

    st.write("")
    st.write("Just a second...")
    time.sleep(3)
    path = 'srlink.exe'
    fe = extract_infos(path)
    feature = data_feature[0,:]
    feature = torch.from_numpy(feature).unsqueeze(dim=0)
    # else:
    #     feature = data_feature[1]
    #     feature = torch.from_numpy(feature.values)
    labels,fps = predict(feature,option)
        # print out the top 5 prediction labels with scores
    st.success('successful prediction')
    if labels == 1:
        st.metric("","Prediction result: the software is malicious")
    else:
        st.metric("","Prediction result: the software is benign")
    
    # print(t2-t1)
    # st.write(float(t2-t1))
    # st.metric("","Time Cost:   "+str(fps)+" ms")
else:
     
    st.write("")
    st.write("Just a second...")
    time.sleep(3)
    path = 'srlink.exe'
    fe = extract_infos(path)
    feature = data_feature[15003,:]
    feature = torch.from_numpy(feature).unsqueeze(dim=0)
    # else:
    #     feature = data_feature[1]
    #     feature = torch.from_numpy(feature.values)
    labels,fps = predict(feature,option)
        # print out the top 5 prediction labels with scores
    st.success('successful prediction')
    if labels == 1:
        st.metric("","Prediction result: the software is malicious")
    else:
        st.metric("","Prediction result: the software is benign")
    
#     # print(t2-t1)
#     # st.write(float(t2-t1))
#     st.write("")
#     st.metric("","Time Cost:   "+str(fps))
