from model import CNN, RCNN, AttentionRCNN
import torch
import time



def predict(feature,option):
    if option =="MalConv":
        model = CNN()
        model.load_state_dict(torch.load('model_ckpt/cnn.pt',map_location='cpu'))
    elif option =="RCNN":
        model = RCNN()
        model.load_state_dict(torch.load('model_ckpt/rcnn.pt',map_location='cpu'))
    elif option == "Att-LSTM":
        model = AttentionRCNN()
        model.load_state_dict(torch.load('model_ckpt/att-lstm.pt',map_location='cpu'))
    else:
        model = AttentionRCNN()
        model.load_state_dict(torch.load('model_ckpt/att-lstm.pt',map_location='cpu'))

    

    model.eval()
    t1 = time.time()
    out = model(feature)
    out = (out > 0).to(int)
    t2 = time.time()
    fps = round(float(1 / (t2 - t1)), 3)
    return out, fps


