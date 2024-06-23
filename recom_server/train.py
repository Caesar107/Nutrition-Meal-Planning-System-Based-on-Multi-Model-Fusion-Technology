import sqlalchemy
from sqlalchemy import create_engine
import pandas as pd
from loguru import logger
import json
import sys
import os
import numpy as np
import pandas as pd
import torch
import pickle as pkl
from sklearn.preprocessing import MinMaxScaler, LabelEncoder
from torch_rechub.models.matching import DSSM
from torch_rechub.trainers import MatchTrainer
from torch_rechub.basic.features import DenseFeature, SparseFeature, SequenceFeature
from torch_rechub.utils.match import generate_seq_feature_match, gen_model_input
from torch_rechub.utils.data import df_to_dict, MatchDataGenerator

if __name__ == '__main__':

    logger.add('train.log')

    dbpath = '../mysite/db.sqlite3'
    engine = create_engine(f'sqlite:///{dbpath}')

    logger.success(f'connect to {dbpath}')
    sql = '''
       -- 平均指标
        select a.data_id,
               a.user_id,
               a.visit_time,
               -- a.rating,
               -- item特征
               b.rating,
               b.calories,
               b.protein,
               b.fat,
               b.sodium,
               -- 用户特征
               c.gender,
               c.age,
               c.weight,
               c.blood_sugar,
               c.blood_pressure,
               c.heart_rate

       from app_uservisit a 
       inner join app_data b
            on a.data_id = b.id
       inner join (
            select a.user_id,
                    a.age,
                    a.gender,
                    b.weight,
                    b.blood_sugar,
                    b.blood_pressure,
                    b.heart_rate
                from user_profile a
                inner join (
                    select user_id,
                        avg(weight) as weight,
                        avg(blood_sugar) as blood_sugar,
                        avg(blood_pressure) as blood_pressure,
                        avg(heart_rate) as heart_rate
                    from user_healthindex
                    group by user_id
                ) b
            on a.user_id = b.user_id
        ) c
        on a.user_id = c.user_id
         
    '''
    df = pd.read_sql_query(sql, engine)
    # 向前填充
    df = df.fillna(method='ffill').dropna()
    # del df['visit_time']
    df.to_csv('train.csv', index=False)

    logger.success('train.csv is generated')


# from movielens_utils import match_evaluation



    df = df.rename(columns={'data_id': 'movie_id', 'visit_time': 'timestamp'})

    data = df.copy()

    sparse_features = ['user_id', 'movie_id', 'gender']
    user_col, item_col = "user_id", "movie_id"

    feature_max_idx = {}
    for feature in sparse_features:
        lbe = LabelEncoder()
        data[feature] = lbe.fit_transform(data[feature]) + 1
        feature_max_idx[feature] = data[feature].max() + 1
        if feature == user_col:
            user_map = {encode_id + 1: raw_id for encode_id, raw_id in enumerate(lbe.classes_)}  #encode user id: raw user id
        if feature == item_col:
            item_map = {encode_id + 1: raw_id for encode_id, raw_id in enumerate(lbe.classes_)}  #encode item id: raw item id

    logger.info(user_map)
    logger.info(item_map)

    with open('save_models/user_map.pkl', 'wb') as f:
        pkl.dump(user_map, f)
    with open('save_models/item_map.pkl', 'wb') as f:
        pkl.dump(item_map, f)


    user_profile = data[["user_id", "gender", 
                         "age", 
                         "weight",
                         "blood_sugar", 
                         "blood_pressure", 
                         "heart_rate"]].drop_duplicates('user_id')
    item_profile = data[["movie_id", # "cate_id",
                        "rating",
                        "calories",
                        "protein",
                        "fat",
                        "sodium",
                         ]].drop_duplicates('movie_id')

    logger.success('data preprocessing is done')

    df_train, df_test = generate_seq_feature_match(data,
                                                user_col,
                                                item_col,
                                                time_col="timestamp",
                                                item_attribute_cols=[],
                                                sample_method=1,
                                                mode=0,
                                                neg_ratio=3,
                                                min_item=0)
    x_train = gen_model_input(df_train, user_profile, user_col, item_profile, item_col, seq_max_len=50)
    y_train = x_train["label"]
    x_test = gen_model_input(df_test, user_profile, user_col, item_profile, item_col, seq_max_len=50)
    y_test = x_test["label"]

    logger.success('data preprocessing step 2 is done')

    user_cols = ['user_id', 'gender', ]
    item_cols = ['movie_id', 
                 # "cate_id"
                 ]

    # TODO 暂时无法融合物品特征与用户特征

    user_features = [
        SparseFeature(feature_name, vocab_size=feature_max_idx[feature_name], embed_dim=16) for feature_name in user_cols
    ]
    user_features += [
        SequenceFeature("hist_movie_id",
                        vocab_size=feature_max_idx["movie_id"],
                        embed_dim=16,
                        pooling="mean",
                        shared_with="movie_id")
    ]
    user_features += [
        DenseFeature(feature_name) for feature_name in ["weight", "age",
                         "blood_sugar", 
                         "blood_pressure", 
                         "heart_rate"]
    ]
    item_features = [
        SparseFeature(feature_name, vocab_size=feature_max_idx[feature_name], embed_dim=16) for feature_name in item_cols
    ]
    item_features += [
        DenseFeature(feature_name) for feature_name in [
            "rating",
            "calories",
            "protein",
            "fat",
            "sodium",
            
        ]
    ]

    all_item = df_to_dict(item_profile)
    test_user = x_test

    logger.success('data preprocessing step 3 is done')

    dg = MatchDataGenerator(x=x_train, y=y_train)

    epoch = 1
    device = 'cpu'
    learning_rate = 0.001
    weight_decay = 1e-6
    batch_size = 64
    save_dir = 'save_models/'

    model = DSSM(user_features,
                item_features,
                temperature=0.02,
                user_params={
                    "dims": [256, 128, 64],
                    "activation": 'prelu',  # important!!
                },
                item_params={
                    "dims": [256, 128, 64],
                    "activation": 'prelu',  # important!!
                })

    trainer = MatchTrainer(model,
                        mode=0,
                        optimizer_params={
                            "lr": learning_rate,
                            "weight_decay": weight_decay
                        },
                        n_epoch=epoch,
                        device=device,
                        model_path=save_dir)

    logger.success('model is ready')

    train_dl, test_dl, item_dl = dg.generate_dataloader(test_user, all_item, batch_size=batch_size)


    logger.success('start to train')


    trainer.fit(train_dl)

    user_embedding = trainer.inference_embedding(model=model, mode="user", data_loader=test_dl, model_path=save_dir)

    item_embedding = trainer.inference_embedding(model=model, mode="item", data_loader=item_dl, model_path=save_dir)

    user_embedding = user_embedding.detach().cpu().numpy()
    item_embedding = item_embedding.detach().cpu().numpy()

    pkl.dump(user_embedding, open("save_models/user_embedding.pkl", "wb"))
    pkl.dump(item_embedding, open("save_models/item_embedding.pkl", "wb"))


