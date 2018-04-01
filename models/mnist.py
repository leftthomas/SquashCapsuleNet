from capsule_layer import CapsuleLinear
from torch import nn


class MNISTNet(nn.Module):
    def __init__(self, num_iterations=3):
        super(MNISTNet, self).__init__()

        self.conv1 = nn.Sequential(nn.Conv2d(1, 64, kernel_size=3, padding=1), nn.ReLU())
        self.features = nn.Sequential(nn.Conv2d(64, 64, kernel_size=3, stride=2, padding=1), nn.ReLU(),
                                      nn.Conv2d(64, 128, kernel_size=3, padding=1), nn.ReLU(),
                                      nn.Conv2d(128, 128, kernel_size=3, padding=1), nn.ReLU())
        self.classifier = CapsuleLinear(out_capsules=10, in_length=128, out_length=16, in_capsules=None,
                                        share_weight=True, routing_type='k_means', num_iterations=num_iterations)

    def forward(self, x):
        out = self.conv1(x)
        out = self.features(out)

        out = out.permute(0, 2, 3, 1)
        out = out.contiguous().view(out.size(0), -1, 128)
        out = self.classifier(out)
        classes = out.norm(dim=-1)
        return classes
