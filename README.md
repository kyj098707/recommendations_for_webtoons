<p align="center">
    <img src="https://user-images.githubusercontent.com/62131378/220874392-0d3f6cb8-d069-434d-90b5-7c113276e71d.png" width="80%">
    <p align="center">
      <img src="https://user-images.githubusercontent.com/54027397/222316541-17da0380-1018-43a6-90eb-3c085bc83811.png">
    </p>
    <p align="center">
        당신에게 맞는 웹툰을 에이블러들이 추천해줄게요 .<br><br> Aivler will recommend a webtoon for you
    </p>
    <h3>
        <p align="center">
            <strong>
                <a href="http://kt-aivle.iptime.org:59000/service/">Go to Project Page!(~2023.06)</a>
            </strong>
        </p>
    </h3>
    <br><br>
</p>

<br>
<hr>
<br>

<img src="https://user-images.githubusercontent.com/62131378/220957545-6e99bdcc-9608-44dc-9a99-ab90ea14e449.png">

<div align="center">

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore -->
**잠시 블라인드처리 하였습니다**
<!-- ALL-CONTRIBUTORS-LIST:END -->
"Thanks goes to these wonderful people"
<Br>
<b>KT Aivler 3rd, AI track</b>
</div>

    
<br>
<hr>
<br>
<img src="https://user-images.githubusercontent.com/62131378/220957565-8195c772-4c76-4b30-a25c-1028f06f89c8.png">
<img src="https://user-images.githubusercontent.com/54027397/220891020-f4eb4227-482a-4550-9db2-8054ab231d5e.png">


## Detail [More Information](https://americanoisice.tistory.com/219)

### 1. 그림체 유사도 산정
timm에서 제공해주는 ImageNet1000으로 사전학습시킨 EfficientV2-S를 베이스 모델로 사용하였습니다. 해당 모델을 100화가 넘어가는 작품(165개)을 골라 이를 맞추는 방식(multi-label classification)으로 3epoch 미세조정하였으며 평가방식은 동일한 작품의 회차들끼리의 cosine 유사도를 계산한 값을 평가지표로 삼았습니다. 최종적으로 학습된 모델의 classifier layer에 들어오기 이전의 feature값을 추출하여 cosine 유사도를 통해 유사도를 체크하였습니다.

아래는 해당 모델을 통해 알아 본 웹툰 '광마회귀'라는 작품과 비슷한 그림체를 가진 작품들입니다. (1열 광마회귀)

<p align="center">
<img src="https://user-images.githubusercontent.com/54027397/220611728-2346e52d-de04-4516-8645-b953cdef0d4e.png" width="500px;"/>
</p>

### 2. 줄거리 유사도 산정
BERT에서 Sentecnce에서 좀 더 의미론적인 임베딩을 뽑아낼 수 있도록 수정된 BERT인 SBERT를 사용하였습니다. 사전학습 모델로는 snunlp에서 사전학습시킨 KR-SBERT를 사용하였으며 이를 통해 줄거리의 임베딩 값을 구해 cosine 유사도를 구해 유사도를 비교하였습니다.

아래는 해당 모델을 통해 알아 본 웹툰 '광마회귀'라는 작품과 비슷한 줄거리를 가진 작품들입니다.

```
<광마회귀>
무공에 미친 광마 이자하. 그는 마교 교주의 천옥을 훔쳐 쫓기던 중 벼랑에서 떨어지게 된다. 모든 게 끝났다고 생각한 순간 눈을 떠보니,
사람들에게 무시당하던 점소이 시절로 돌아와 있는데...
게다가 억울한 누명으로 두들겨 맞고 객잔은 박살이 나 있는 상황. 점소이 시절로 회귀한 광마!
사내는 다시 미치게 될 것인가? 아니면 사내의 적들이 미치게 될 것인가.

<이모털 헐크>
낮의 브루스 배너는 죽음 앞에 무력하다. 하지만 이 연약한 인간이 쓰러지고 밤이 오면, 그땐 헐크의 시간이 시작된다!
미지의 '녹색 문'을 넘어 지옥 밑바닥에 도착하는 배너 일행. 그러나 지옥보다 위험한 것은 헐크 자신이다!
감마 실험체들을 노리는 잔인무도한 적들의 등장으로 헐크의 친구, 연인, 모든 주변인물이 혼돈에 빠지는데….

<은탄>
흡혈귀와 요괴, 무당이 창궐한 혼란의 조선, 자신을 암흑어사라 칭하는 박문수가 타락한 관아를 파괴하고
다닌다. 다급해진 조정에서는 흡혈귀 왕의 부활을 노리는 암흑어사 박문수를 토벌하라 명하기 위해
갓 무과에 급제한 무관 안손에게 도술과 무술에 능한 도적 홍킬동을 찾아오라 태백산으로 파견한다. 

<천마육성>
마교의 태왕각주 ‘사마귀’의 명령으로 화산파 출목지역으로 파견나간 비객조. ‘설휘’는 화산파의 절대고수 ‘구종명’에게 죽임을 당할 위기에 처한다.
그 때 눈앞에 상태창이 나타나고 정찰임무를 받기 직전으로 회귀하게 된다.
설휘는 자신이 전생에서 죽임을 당했던 똑같은 임무를 받게 되자 주변의 환경을 조금이라도 바꾸어 살아남고자 발버둥친다.
고비마다 눈앞에 나타나는 선택창, 미래를 알 수 없는 지문들. 삶과 죽음이 공존하는 세상 안에서 최선의 방법을 찾아 나선다.

<7FATES: CHAKHO>
타락한 도시 신시, 길에서 마주친 수수께끼의 사내가 제하에게 의문의 말을 던진다.
하지만 병원에서 깨어난 제하는 그날의 일을 기억하지 못하고...
현세에 존재해선 안될 범이라는 존재들이 도시를 재앙으로 물들일 때,
일곱개의 운명이 엮어져, 그들에 맞서기 위해 무기를 든다. 이제 범을 사냥할 시간이다
```

    



