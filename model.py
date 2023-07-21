import torch
from torch import nn
from torch.nn import functional as F


class CNN(nn.Module):
    def __init__(
        self,
        feature_dim=75,
        embed_dim=8,
        out_channels=128,
        kernel_size=8,
        stride=2,
        dropout=0.5,
    ):
        super(CNN, self).__init__()
        self.batchnorm = nn.BatchNorm1d(feature_dim)
        self.dropout = nn.Dropout(dropout)
        self.conv = nn.Conv1d(
            in_channels=embed_dim,
            out_channels=out_channels*2,
            kernel_size=kernel_size,
            stride=stride,
        )
        self.fc = nn.Linear(out_channels, 1)
    
    def forward(self, x):
        x = x.unsqueeze(dim=2)
        bn_x = self.batchnorm(x)
        embed_x = torch.cat((bn_x,bn_x,bn_x,bn_x,bn_x,bn_x,bn_x,bn_x), dim=2)
        embedding = self.dropout(embed_x)
        conv_in = embedding.permute(0, 2, 1)
        conv_out = self.conv(conv_in)
        glu_out = F.glu(conv_out, dim=1)
        values, _ = glu_out.max(dim=-1)
        output = self.fc(values).squeeze(1)
        return output

    
class RCNN(nn.Module):
    def __init__(
        self,
        feature_dim=75,
        embed_dim=8,
        out_channels=128,
        kernel_size=8,
        stride=2,
        hidden_size=128,
        num_layers=2,
        bidirectional=True,
        dropout=0.5,
    ):
        super(RCNN, self).__init__()
        self.conv = nn.Conv1d(
            in_channels=embed_dim,
            out_channels=out_channels,
            kernel_size=kernel_size,
            stride=stride,
        )
        self.rnn = nn.GRU(
            input_size=out_channels,
            hidden_size=hidden_size,
            num_layers=num_layers,
            bidirectional=bidirectional,
        )
        self.batchnorm = nn.BatchNorm1d(feature_dim)
        self.dropout = nn.Dropout(dropout)
        rnn_size = (int(bidirectional) + 1) * hidden_size
        self.fc = nn.Linear(rnn_size, 1)

    def forward(self, x):
        x = x.unsqueeze(dim=2)
        bn_x = self.batchnorm(x)
        embed_x = torch.cat((bn_x,bn_x,bn_x,bn_x,bn_x,bn_x,bn_x,bn_x), dim=2)
        embedding = self.dropout(embed_x)
        conv_in = embedding.permute(0, 2, 1)
        conv_out = self.conv(conv_in)
        conv_out = conv_out.permute(2, 0, 1)
        rnn_out, _ = self.rnn(conv_out)
        fc_in = rnn_out[-1]
        output = self.fc(fc_in).squeeze(1)
        return output
    
class AttentionRCNN(nn.Module):
    def __init__(
        self,
        feature_dim=75,
        embed_dim=8,
        out_channels=128,
        kernel_size=8,
        stride=2,
        hidden_size=128,
        num_layers=2,
        bidirectional=True,
        attn_size=128,
        dropout=0.5,
    ):
        super(AttentionRCNN, self).__init__()
        self.conv = nn.Conv1d(
            in_channels=embed_dim,
            out_channels=out_channels,
            kernel_size=kernel_size,
            stride=stride,
        )
        self.rnn = nn.LSTM(
            input_size=out_channels,
            hidden_size=hidden_size,
            num_layers=num_layers,
            bidirectional=bidirectional,
        )
        self.batchnorm = nn.BatchNorm1d(feature_dim)
        rnn_size = (int(bidirectional) + 1) * hidden_size
        self.local2attn = nn.Linear(rnn_size, attn_size)
        self.global2attn = nn.Linear(rnn_size, attn_size, bias=False)
        self.attn_scale = nn.Parameter(
            nn.init.kaiming_uniform_(torch.empty(attn_size, 1))
        )
        self.dropout = nn.Dropout(dropout)
        self.fc = nn.Linear(rnn_size, 1)

    def forward(self, x):
        x = x.unsqueeze(dim=2)
        bn_x = self.batchnorm(x)
        embed_x = torch.cat((bn_x,bn_x,bn_x,bn_x,bn_x,bn_x,bn_x,bn_x), dim=2)
        embedding = self.dropout(embed_x)
        conv_in = embedding.permute(0, 2, 1)
        conv_out = self.conv(conv_in)
        conv_out = conv_out.permute(2, 0, 1)
        rnn_out, _ = self.rnn(conv_out)
        global_rnn_out = rnn_out.mean(dim=0)
        attention = torch.tanh(
            self.local2attn(rnn_out) + self.global2attn(global_rnn_out)
        ).permute(1, 0, 2)
        alpha = F.softmax(attention.matmul(self.attn_scale), dim=-1)
        rnn_out = rnn_out.permute(1, 0, 2)
        fc_in = (alpha * rnn_out).sum(dim=1)
        output = self.fc(fc_in).squeeze(1)
        return output