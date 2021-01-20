import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.decomposition import PCA

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.optimizers import Adam



# csv형태로 저장된 데이터 파일 읽어오기
data = pd.read_csv('dataset/data.csv')
# 데이터의 길이
data_len = len(data)

# 입력과 출력 값 분리
value_data = data.drop(['GT Compressor decay state coefficient.', 'GT Turbine decay state coefficient.'], axis=1)
label_data = data[['GT Compressor decay state coefficient.', 'GT Turbine decay state coefficient.']]

# pca
pca = PCA(n_components=2)
pca_data = pca.fit_transform(value_data)
pca_data = pd.DataFrame(data = pca_data, columns = ['pca 1', 'pca 2'])

# train, test 데이터 분리
train_data = value_data.iloc[:int(data_len * 0.8)]
train_label = label_data.iloc[:int(data_len * 0.8)]

test_data = value_data.iloc[int(data_len*0.8):]
test_label = label_data.iloc[int(data_len * 0.8):]

train_pca_data = value_data.iloc[:int(data_len * 0.8)]
train_pca_label = label_data.iloc[:int(data_len * 0.8)]

test_pca_data = value_data.iloc[int(data_len*0.8):]
test_pca_label = label_data.iloc[int(data_len * 0.8):]

# model 생성
# 16개의 변수 입력
# 은닉층 8-6-4-2
# 2개의 값 출력
model = keras.Sequential([
    keras.layers.Dense(8, input_shape=(16, )),
    keras.layers.Dense(6),
    keras.layers.Dense(4),
    keras.layers.Dense(2),
    keras.layers.Dense(2)])

# # 은닉층 8-6-4
# # 2개의 값 출력
# model = keras.Sequential([
#     keras.layers.Dense(8, input_shape=(16, )),
#     keras.layers.Dense(6),
#     keras.layers.Dense(4),
#     keras.layers.Dense(2)])

# # 은닉층 8-6
# # 2개의 값 출력
# model = keras.Sequential([
#     keras.layers.Dense(8, input_shape=(16, )),
#     keras.layers.Dense(6),
#     keras.layers.Dense(2)])

# 모델 구조 출력
model.summary()

# 모델 최적화
model.compile(optimizer=Adam(), loss='mean_squared_error', metrics=['mse'])

# 학습(raw)
model.fit(train_data, train_label, epochs=1000, validation_data=(test_data, test_label))

# # 학습(pca)
# model.fit(train_pca_data, train_pca_label, epochs=1000, validation_data=(test_pca_data, test_pca_label))


