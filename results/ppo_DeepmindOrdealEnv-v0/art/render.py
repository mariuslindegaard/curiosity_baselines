import pickle
import base64
import gzip
import torch




a = torch.load("results/ppo_DeepmindOrdealEnv-v0/art/params.pkl", map_location=torch.device('cpu'))
print(a.render())
