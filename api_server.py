import pickle as pkl
from loguru import logger
import numpy as np

logger.add("http.log")

from flask import *

with open('save_models/user_embedding.pkl', 'rb') as f:
    user_embedding = pkl.load(f)

with open('save_models/item_embedding.pkl', 'rb') as f:
    item_embedding = pkl.load(f)

with open('save_models/user_map.pkl', 'rb') as f:
    # encode user id: raw user id
    user_map = pkl.load(f)

useridx2encoded = {v: k for k, v in user_map.items()}

with open('save_models/item_map.pkl', 'rb') as f:
    item_map = pkl.load(f)

logger.info(f'item shape: {item_embedding.shape}')
logger.info(f'user shape: {user_embedding.shape}')

from torch_rechub.utils.match import Annoy
annoy = Annoy(n_trees=10)
annoy.fit(item_embedding)

logger.success("load model successfully")


app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    # 获取post请求参数
    user_id = request.form.get('user_id')
    user_id = int(user_id)
    # 转化成user_idx
    user_idx = useridx2encoded.get(user_id)
    logger.warning(f'user_id: {user_id}, user_idx: {user_idx}')
    #普通召回
    user_emb = user_embedding[user_idx]
    topk = 30
    items_idx, items_scores = annoy.query(v=user_emb, n=topk)  #the index of topk match items
    items_idx = [int(item_map.get(i)) for i in items_idx]
    return jsonify({'items_idx': items_idx})

# load model
# predict

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)