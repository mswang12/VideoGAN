"""
"""
import torch
import torch.nn as nn
import torch.nn.functional as F

# Default settings of discriminator networks.
IMG_H = 32
IMG_W = 32

HIST_LEN = 4

# feature maps for each convolution of each scale network in the discriminator model
SCALE_FMS_G = [
    [3 * (HIST_LEN), 128, 256, 128, 3],
    [3 * (HIST_LEN), 128, 256, 128, 3],
    [3 * (HIST_LEN), 128, 256, 512, 256, 128, 3],
    [3 * (HIST_LEN), 128, 256, 512, 256, 128, 3]
]

# kernel sizes for each convolution of each scale network in the discriminator model
SCALE_KERNEL_SIZES_G = [
    [3, 3, 3, 3],
    [5, 3, 3, 5],
    [5, 3, 3, 3, 3, 5],
    [7, 5, 5, 5, 5, 7],
]


class Generator(nn.Module):
    def __init__(self, layers):
        super(Generator, self).__init__()
        self.layers = layers

    def forward(self, x):
        for i, layer in enumerate(self.layers):
            x = F.relu(layer(x))
            print('i: {}, size: {}'.format(i, x.shape))

        return x

class GeneratorDefinitions(nn.Module):
    def __init__(self):
        super(GeneratorDefinitions, self).__init__()

        # Generator Net 1
        self.layers1 = nn.ModuleList()
        self.layers1.append(nn.Conv2d(3 * HIST_LEN, 128, 3, stride=1, padding=1))
        self.layers1.append(nn.Conv2d(128, 256, 3, stride=1, padding=1))
        self.layers1.append(nn.ConvTranspose2d(256, 128, 3, stride=1, padding=1, output_padding=0))
        self.layers1.append(nn.ConvTranspose2d(128, 3, 3, stride=1, padding=1, output_padding=0))

        # Generator Net 2
        self.layers2 = nn.ModuleList()
        self.layers2.append(nn.Conv2d(3 * HIST_LEN, 128, 5, stride=1, padding=2))
        self.layers2.append(nn.Conv2d(128, 256, 3, stride=1, padding=1))
        self.layers2.append(nn.ConvTranspose2d(256, 128, 3, stride=1, padding=1, output_padding=0))
        self.layers2.append(nn.ConvTranspose2d(128, 3, 5, stride=1, padding=2, output_padding=0))

        # Generator Net 3
        self.layers3 = nn.ModuleList()
        self.layers3.append(nn.Conv2d(3 * HIST_LEN, 128, 5, stride=1, padding=2))
        self.layers3.append(nn.Conv2d(128, 256, 3, stride=1, padding=1))
        self.layers3.append(nn.Conv2d(256, 512, 3, stride=1, padding=1))
        self.layers3.append(nn.ConvTranspose2d(512, 256, 3, stride=1, padding=1, output_padding=0))
        self.layers3.append(nn.ConvTranspose2d(256, 128, 3, stride=1, padding=1, output_padding=0))
        self.layers3.append(nn.ConvTranspose2d(128, 3, 5, stride=1, padding=2, output_padding=0))

        # Generator Net 4
        self.layers4 = nn.ModuleList()
        self.layers4.append(nn.Conv2d(3 * HIST_LEN, 128, 7, stride=1, padding=3))
        self.layers4.append(nn.Conv2d(128, 256, 5, stride=1, padding=2))
        self.layers4.append(nn.Conv2d(256, 512, 5, stride=1, padding=2))
        self.layers4.append(nn.ConvTranspose2d(512, 256, 5, stride=1, padding=2, output_padding=0))
        self.layers4.append(nn.ConvTranspose2d(256, 128, 5, stride=1, padding=2, output_padding=0))
        self.layers4.append(nn.ConvTranspose2d(128, 3, 7, stride=1, padding=3, output_padding=0))

    def forward(self, x):
        model1 = Generator(self.layers1)
        model2 = Generator(self.layers2)
        model3 = Generator(self.layers3)
        model4 = Generator(self.layers4)

        input_image1 = F.interpolate(x, size=(4, 4))
        image1 = model1(input_image1)

        input_image2 = F.interpolate(x, size=(8, 8))
        image2 = model2(input_image2)

        input_image3 = F.interpolate(x, size=(16, 16))
        image3 = model3(input_image3)

        input_image4 = F.interpolate(x, size=(32, 32))
        image4 = model4(input_image4)

        return image4
