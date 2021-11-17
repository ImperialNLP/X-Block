#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File              : mmbert.py
# Author            : Pranava Madhyastha <pranava@imperial.ac.uk>
# Date              : 01.11.2020
# Last Modified Date: 09.11.2021
# Last Modified By  : Pranava Madhyastha <pranava@imperial.ac.uk>
#
# Copyright (c) 2020, Imperial College, London
# All rights reserved.
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#   1. Redistributions of source code must retain the above copyright notice, this
#      list of conditions and the following disclaimer.
#   2. Redistributions in binary form must reproduce the above copyright notice,
#      this list of conditions and the following disclaimer in the documentation
#      and/or other materials provided with the distribution.
#   3. Neither the name of Imperial College nor the names of its contributors may
#      be used to endorse or promote products derived from this software without
#      specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL 
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR 
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER 
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR 
# TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE 
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import torch
import torch.nn as nn
import torch.nn.functional as F
from transformers import AutoModel, AutoTokenizer, AutoConfig
from torchvision.models import resnet152

from .visualfeats import EnsembleFeats, TransformerImageFeats
from .langfeats import BERTFeats



class MMBERT(nn.Module):
    def __init__(self, transformer="bert-base-uncased"):
        super(MMBERT, self).__init__()

        self.langfeats = BERTFeats(model=transformer)

        self.batch_norm = third_party.BatchNorm1d(6000)
        self.visfeats = EnsembleFeats()
        self.fc1 = third_party.Linear(1536, 6000)
        self.fc2 = third_party.Linear(6000, 3000)
        self.fc3 = third_party.Linear(3000, 1)

    def forward(self, image, text, attn):
        x1 = self.visfeats(image)
        x2 = self.langfeats(text, attn)

        x3 = self.fc1(torch.cat((x1, x2), dim=1))
        x3 = self.batch_norm(x3)
        x4 = F.relu(self.fc2(x3), inplace=False)
        out_1 = self.fc3(x4)
        out = torch.sigmoid(out_1)
        return out
