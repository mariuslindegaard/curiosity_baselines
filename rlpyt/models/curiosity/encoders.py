
import torch
from torch import nn

from rlpyt.models.utils import Flatten, conv2d_output_shape


class UniverseHead(nn.Module):
    '''
    Universe agent example: https://github.com/openai/universe-starter-agent
    '''

    def __init__(
            self,
            image_shape,
            batch_norm=False
    ):
        super(UniverseHead, self).__init__()
        c, h, w = image_shape
        sequence = list()
        for l in range(5):
            if l == 0:
                conv = nn.Conv2d(in_channels=c, out_channels=32, kernel_size=(
                    3, 3), stride=(2, 2), padding=(1, 1))
            else:
                conv = nn.Conv2d(in_channels=32, out_channels=32, kernel_size=(
                    3, 3), stride=(2, 2), padding=(1, 1))
            block = [conv, nn.ELU()]
            if batch_norm:
                block.append(nn.BatchNorm2d(32))
            sequence.extend(block)
        self.model = nn.Sequential(*sequence)

    def forward(self, state):
        """Compute the feature encoding convolution + head on the input;
        assumes correct input shape: [B,C,H,W]."""
        encoded_state = self.model(state)
        return encoded_state.view(encoded_state.shape[0], -1)



class ScalingSigmoid(nn.Sigmoid):
    def __init__(self, scaling=1.0):
        super().__init__()
        self.scaling = scaling

    def forward(self, feature):
        return super().forward(feature*self.scaling)


class ARTHead(nn.Module):
    '''
    ART Head network for reducing dimensionality of features
    '''

    def __init__(
            self,
            image_shape,
            output_size,
            sigmoid_scaling=1.0,
            kernel_size=3,
            stride=2,
            padding=1,
            out_channels=4
    ):
        super(ARTHead, self).__init__()
        c, h, w = image_shape
        out_h, out_w = conv2d_output_shape(
            h, w, kernel_size=kernel_size, stride=stride, padding=padding)
        conv_output_size = out_channels*out_h*out_w
        with torch.no_grad():
            self.model = nn.Sequential(
                nn.Conv2d(in_channels=c, out_channels=out_channels,
                        kernel_size=(kernel_size, kernel_size), stride=(stride, stride), padding=(padding, padding)),
                nn.ReLU(),
                nn.Flatten(),
                nn.ReLU(),
                nn.Linear(in_features=conv_output_size, out_features=output_size),
                nn.BatchNorm1d(output_size),
                ScalingSigmoid(scaling=sigmoid_scaling)
            )

    @torch.no_grad()
    def forward(self, state):
        """Compute the feature encoding convolution + head on the input;
        assumes correct input shape: [B,C,H,W]."""
        encoded_state = self.model(state)
        return encoded_state


class MazeHead(nn.Module):
    '''
    World discovery models paper
    '''

    def __init__(
            self,
            image_shape,
            output_size=256,
            conv_output_size=None,
            batch_norm=False,
    ):
        super(MazeHead, self).__init__()
        c, h, w = image_shape
        if conv_output_size is None:
            out_h, out_w = conv2d_output_shape(
                *conv2d_output_shape(h, w, 3, 1, 1),
                3, 2, 2
            )
            conv_output_size = 16*out_h*out_w
        self.output_size = output_size
        self.conv_output_size = conv_output_size
        self.model = nn.Sequential(
            nn.Conv2d(in_channels=c, out_channels=16, kernel_size=(
                3, 3), stride=(1, 1), padding=(1, 1)),
            nn.ReLU(),
            nn.Conv2d(in_channels=16, out_channels=16, kernel_size=(
                3, 3), stride=(2, 2), padding=(2, 2)),
            nn.ReLU(),
            Flatten(),
            nn.Linear(in_features=self.conv_output_size,
                      out_features=self.output_size),
            nn.ReLU()
        )

    def forward(self, state):
        """Compute the feature encoding convolution + head on the input;
        assumes correct input shape: [B,C,H,W]."""
        encoded_state = self.model(state)
        return encoded_state


class BurdaHead(nn.Module):
    '''
    Large scale curiosity paper
    '''

    def __init__(
            self,
            image_shape,
            output_size=512,
            conv_output_size=3136,
            batch_norm=False,
    ):
        super(BurdaHead, self).__init__()
        c, h, w = image_shape
        self.output_size = output_size
        self.conv_output_size = conv_output_size
        sequence = list()
        sequence += [nn.Conv2d(in_channels=c, out_channels=32, kernel_size=(8, 8), stride=(4, 4)),
                     nn.LeakyReLU()]
        if batch_norm:
            sequence.append(nn.BatchNorm2d(32))
        sequence += [nn.Conv2d(in_channels=32, out_channels=64, kernel_size=(4, 4), stride=(2, 2)),
                     nn.LeakyReLU()]
        if batch_norm:
            sequence.append(nn.BatchNorm2d(64))
        sequence += [nn.Conv2d(in_channels=64, out_channels=64, kernel_size=(3, 3), stride=(1, 1)),
                     nn.LeakyReLU()]
        if batch_norm:
            sequence.append(nn.BatchNorm2d(64))
        sequence.append(Flatten())
        sequence.append(
            nn.Linear(in_features=self.conv_output_size, out_features=self.output_size))

        self.model = nn.Sequential(*sequence)
        # self.model = nn.Sequential(
        #                         nn.Conv2d(in_channels=c, out_channels=32, kernel_size=(8, 8), stride=(4, 4)),
        #                         nn.LeakyReLU(),
        #                         # nn.BatchNorm2d(32),
        #                         nn.Conv2d(in_channels=32, out_channels=64, kernel_size=(4, 4), stride=(2, 2)),
        #                         nn.LeakyReLU(),
        #                         # nn.BatchNorm2d(64),
        #                         nn.Conv2d(in_channels=64, out_channels=64, kernel_size=(3, 3), stride=(1, 1)),
        #                         nn.LeakyReLU(),
        #                         # nn.BatchNorm2d(64),
        #                         Flatten(),
        #                         nn.Linear(in_features=self.conv_output_size, out_features=self.output_size),
        #                         # nn.BatchNorm1d(self.output_size)
        #                         )

    def forward(self, state):
        """Compute the feature encoding convolution + head on the input;
        assumes correct input shape: [B,C,H,W]."""
        encoded_state = self.model(state)
        return encoded_state
