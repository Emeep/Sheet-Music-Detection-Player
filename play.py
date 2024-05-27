import gdown as gd
import os
import glob

weights = glob.glob("weights/*")
for f in weights:
    os.remove(f)

if os.path.exists("weights"):
  os.rmdir("weights")

url_weights = "https://drive.google.com/drive/folders/1vwlLz2dVbfybKPyeU3UcS9pHeyRBd1JU?usp=sharing"
gd.download_folder(url_weights)