import numpy as np
import werkzeug
from PIL import Image
from flask import Flask, request
import torch
from model import Model, ResidualBlock, LinearBlock

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def classify():
    data = request.files['image']
    filename = werkzeug.utils.secure_filename(data.filename)
    data.save(filename)

    img = torch.tensor(np.asarray(Image.open(filename).resize((256, 256))),
                       dtype=torch.float32).permute(2, 0, 1)
    img /= 255

    model = torch.load("LungCancerNet.pt", weights_only=False)
    model.eval()

    img = torch.stack((img, img, img, img, img, img, img, img,
                       img, img, img, img, img, img, img, img,
                       img, img, img, img, img, img, img, img,
                       img, img, img, img, img, img, img, img))
    pred_list = list(model(img).max(1).indices.cpu().detach())
    frequency = [0, 0, 0]
    for el in pred_list:
        frequency[el] += 1
    pred = frequency.index(max(frequency))

    if pred == 0:
        return "bengin"
    if pred == 1:
        return "malignant"
    return "normal"


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")