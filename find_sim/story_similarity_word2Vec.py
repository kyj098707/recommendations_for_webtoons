# 패키지 임포트
from collections.abc import Mapping
import urllib.request
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests
import re
from konlpy.tag import Okt
from gensim.models import Word2Vec
from gensim.models import KeyedVectors
from sklearn.metrics.pairwise import cosine_similarity
import io
from gensim.models import Word2Vec

#텍스트 전처리
def preprocessing(df):
    df['story'] = df['story'].str.replace("[^ㄱ-ㅎㅏ-ㅣ가-힣 ]","")

    with open('../output/stopwords.txt', 'r') as f:
        list_file = f.readlines()
    stopwords = list_file[0].split(",")
    df['story'] = [x for x in df['story'] if x not in stopwords]

    tokenized_data = []

#단어 벡터 평균 구하기
def vectors(document_list):
    document_embedding_list = []

    # 각 문서에 대해서
    for line in document_list:
        doc2vec = None
        count = 0
        for word in line.split():
            if word in word2vec_model.wv.vocab:
                count += 1
                # 해당 문서에 있는 모든 단어들의 벡터값을 더한다.
                if doc2vec is None:
                    doc2vec = word2vec_model[word]
                else:
                    doc2vec = doc2vec + word2vec_model[word]

        if doc2vec is not None:
            # 단어 벡터를 모두 더한 벡터의 값을 문서 길이로 나눠준다.
            doc2vec = doc2vec / count
            document_embedding_list.append(doc2vec)

    # 각 문서에 대한 문서 벡터 리스트를 리턴
    return document_embedding_list

def recommendations(title):
    books = df[['title', 'story','genre']]

    # 책의 제목을 입력하면 해당 제목의 인덱스를 리턴받아 idx에 저장.
    indices = pd.Series(df.index, index = df['title']).drop_duplicates()    
    idx = indices[title]

    # 입력된 책과 줄거리(document embedding)가 유사한 책 5개 선정.
    sim_scores = list(enumerate(cosine_similarities[idx]))
    sim_scores = sorted(sim_scores, key = lambda x: x[1], reverse = True)
    sim_scores = sim_scores[1:6]

    # 가장 유사한 책 5권의 인덱스
    book_indices = [i[0] for i in sim_scores]

    # 전체 데이터프레임에서 해당 인덱스의 행만 추출. 5개의 행을 가진다.
    recommend = books.iloc[book_indices].reset_index(drop=True)

    # 데이터프레임으로부터 순차적으로 이미지를 출력
    for i, row in recommend.iterrows():
        print('title : ',row['title'])
        print(sim_scores[i])
        print('genre : ',row['genre'])
        print('-------------')

if __name__ == "__main__":
    df = pd.read_csv('../output/info.csv')
    print('전체 문서의 수 : ', len(df))
    #토큰화하여 리스트에 저장
    corpus = []
    for words in df['story']:
        corpus.append(words.split())
    
    word2vec_model = Word2Vec(sentences=corpus, size=100, window=5, min_count=5, workers=4, sg=0)

    document_embedding_list = vectors(df['story'])
    print('문서 벡터의 수 :',len(document_embedding_list))
    cosine_similarities = cosine_similarity(document_embedding_list, document_embedding_list)
    print('코사인 유사도 매트릭스의 크기 :',cosine_similarities.shape)

    recommendations("싸움독학")