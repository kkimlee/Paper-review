import pandas as pd

# Features.txt 에는 feature label이 저장되어 있음
# 숫자 - feature label 형태로 저장되어 있음
features = pd.read_csv('dataset/Features.txt', names=['features'])


# feature label만 추출하기 위해 공백 문자를 탐색하여 삭제
# 추출된 label은 list 형태로 저장하여 data의 label로 사용
data_label = list()
for idx in range(len(features)):
    # feature 값 추출
    string = features['features'][idx]
    # 첫 번째 공백 위치 추출
    pos = string.find(' ')
    # 두 번째 공백 위치 추출
    pos2 = string.find(' ', pos+1)
    
    # 두 번째 공백 다음 위치 부터 data_label에 값 저장
    data_label.append(string[pos2+1:])
    
    

# data.txt 파일에 세번의 띄어쓰기로 데이터가 구분되어 있음
# 데이터를 분리하여 저장하기 위해 delimeter를 설정
delimeter = '   '

# 텍스트 파일을 csv 형태로 읽어옴
# 읽어온 텍스트 파일의 데이터는 delimeter로 분리됨
data = pd.read_csv('dataset/data.txt', delimiter=delimeter, names=data_label)

# csv 형태로 저장
data.to_csv('dataset/data.csv', index=None)

