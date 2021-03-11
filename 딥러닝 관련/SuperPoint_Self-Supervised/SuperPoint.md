# SuperPoint
## Abstract
이 논문은 컴퓨터 비전의 다수의 다중 뷰 지오메트리 문제에 적합한 관심 지점 감지기 및 설명자를 학습하기위한 자체 감독 프레임 워크를 제공합니다.
패치 기반 신경망과는 달리, 우리의 완전 컨볼 루션 모델은 전체 크기 이미지에서 작동하며 한 번의 순방향 패스에서 픽셀 수준 관심 지점 위치 및 관련 설명자를 공동으로 계산합니다. 
관심 지점 감지 반복성을 높이고 도메인 간 적응 (예 : 합성-실제)을 수행하기위한 다중 스케일, 다중 호모 그래피 접근 방식 인 Homographic Adaptation을 소개합니다. 
Homographic Adaptation을 사용하여 MS-COCO 일반 이미지 데이터 세트에 대해 학습 된 모델은 초기 사전 조정 된 심층 모델 및 기타 기존의 모서리 감지기보다 훨씬 더 풍부한 관심 지점 집합을 반복적으로 감지 할 수 있습니다. 
최종 시스템은 LIFT, SIFT 및 ORB와 비교할 때 HPatch에 대한 최신 동형 추정 결과를 제공합니다.  
  
## 1. Introduction
SLAM (Simultaneous Localization and Mapping), SfM (Structure-from-Motion), 카메라 보정 및 이미지 일치와 같은 기하학적 컴퓨터 비전 작업의 첫 번째 단계는 이미지에서 관심 지점을 추출하는 것입니다. 
관심 지점은 안정적이고 다양한 조명 조건 및 관점에서 반복 가능한 이미지의 2D 위치입니다.
Multiple View Geometry [9]로 알려진 수학 및 컴퓨터 비전의 하위 분야는 관심 지점을 이미지에서 안정적으로 추출하고 일치시킬 수 있다는 가정을 바탕으로 구축 된 정리 및 알고리즘으로 구성됩니다. 
그러나 대부분의 실제 컴퓨터 비전 시스템에 대한 입력은 이상적인 지점 위치가 아닌 원시 이미지입니다.  
  
컨볼 루션 신경망은 이미지를 입력으로 요구하는 거의 모든 작업에서 수작업으로 설계된 표현보다 우수한 것으로 나타났습니다. 
특히, 2D "키포인트"또는 "랜드 마크"를 예측하는 완전 컨볼 루션 신경망은 사람 포즈 추정 [31], 물체 감지 [14], 방 레이아웃 추정 [12]과 같은 다양한 작업에 대해 잘 연구되어 있습니다. 
이러한 기술의 핵심은 사람 어노 테이터가 레이블을 지정한 2D Ground Truth 위치의 대규모 데이터 세트입니다.  
   
관심 지점 감지를 대규모지도 머신 러닝 문제로 유사하게 공식화하고이를 감지하도록 최신 컨볼 루션 신경망 아키텍처를 훈련시키는 것은 자연스러운 것처럼 보입니다.
안타깝게도 네트워크가 입가 또는 왼쪽 발목과 같은 신체 부위를 감지하도록 훈련 된 인체 키포인트 추정과 같은 의미 론적 작업과 비교할 때 관심 지점 감지 개념은 의미 상 잘못 정의되어 있습니다. 
따라서 관심 지점에 대한 강력한 감독으로 컨볼 루션 신경망을 훈련하는 것은 중요하지 않습니다.  
  
실제 이미지에서 관심 지점을 정의하기 위해 사람의 감독을 사용하는 대신자가 훈련을 사용하는자가 감독 솔루션을 제시합니다. 
우리의 접근 방식에서는 대규모 인간 주석 작업이 아닌 관심 지점 감지기 자체가 감독하는 실제 이미지에서 의사 지상 진실 관심 지점 위치의 대규모 데이터 세트를 만듭니다.  
  
![fig 2](./img/fig2.PNG)
###### [fig 2] Self-Supervised Training Overview. In our self-supervised approach, we (a) pre-train an initial interest point detector on synthetic data and (b) apply a novel Homographic Adaptation procedure to automatically label images from a target, unlabeled domain. The generated labels are used to (c) train a fully-convolutional network that jointly extracts interest points and descriptors from an image.
  
가상 현실의 관심 지점을 생성하기 위해 먼저 Synthetic Shapes (그림 2a 참조)라는 합성 데이터 세트에서 만든 수백만 개의 예제에 대해 완전 컨볼 루션 신경망을 훈련합니다. 
합성 데이터 세트는 관심 지점 위치가 모호하지 않은 단순한 기하학적 모양으로 구성됩니다. 
결과적으로 훈련 된 탐지기를 MagicPoint라고 부릅니다. 
이는 합성 데이터 세트에서 기존의 관심 지점 탐지기보다 훨씬 뛰어난 성능을 발휘합니다 (섹션 4 참조). 
MagicPoint는 도메인 적응의 어려움에도 불구하고 실제 이미지에서 놀라운 성능을 발휘합니다 [7]. 
그러나 다양한 이미지 텍스처 및 패턴에 대한 기존의 관심 지점 감지기와 비교할 때 MagicPoint는 많은 잠재적 관심 지점 위치를 놓칩니다. 
실제 이미지의 성능 격차를 해소하기 위해 우리는 다중 스케일, 다중 변환 기술인 Homographic Adaptation을 개발했습니다.  
  
Homographic Adaptation은 관심 지점 감지기의자가지도 학습을 가능하게하도록 설계되었습니다. 
입력 이미지를 여러 번 왜곡하여 관심 지점 감지기가 다양한 관점과 배율에서 장면을 볼 수 있도록합니다 (섹션 5 참조). 
우리는 MagicPoint 감지기와 함께 Homographic Adaptation을 사용하여 감지기의 성능을 높이고 의사 지상 진실 관심 지점을 생성합니다 (그림 2b 참조). 
그 결과 탐지는 더 반복 가능하며 더 큰 자극 세트에서 발생합니다. 
따라서 결과 검출기를 SuperPoint라고 명명했습니다.  
  
견고하고 반복 가능한 관심 지점을 감지 한 후 가장 일반적인 단계는 이미지 일치와 같은 더 높은 수준의 의미 작업을 위해 각 지점에 고정 차원 설명자 벡터를 연결하는 것입니다. 
따라서 마지막으로 SuperPoint를 디스크립터 서브 네트워크와 결합합니다 (그림 2c 참조). 
수퍼 포인트 아키텍처는 다중 스케일 기능을 추출하는 컨볼 루션 레이어의 깊은 스택으로 구성되므로 관심 포인트 설명자를 계산하는 추가 서브 네트워크와 관심 포인트 네트워크를 결합하는 것이 간단합니다 (섹션 3 참조). 
결과 시스템은 그림 1에 나와 있습니다.  
  
![fig 1](./img/fig1.PNG)
###### [fig 1] Figure 1. SuperPoint for Geometric Correspondences. We present a fully-convolutional neural network that computes SIFTlike 2D interest point locations and descriptors in a single forward pass and runs at 70 FPS on 480×640 images with a Titan X GPU.  
  
## 2. Related Work
기존의 관심 지점 감지기는 철저히 평가되었습니다 [24, 16]. 
FAST 코너 검출기 [21]는 고속 코너 검출을 머신 러닝 문제로 캐스팅 한 최초의 시스템이었으며 스케일 불변 특성 변환 (SIFT [15])은 컴퓨터 비전에서 여전히 ​​가장 잘 알려진 전통적인 로컬 특성 설명 자일 것입니다.  
  
SuperPoint 아키텍처는 관심 지점 감지 및 설명자 학습에 딥 러닝을 적용하는 최근 발전에서 영감을 받았습니다. 
이미지 하위 구조를 일치시킬 수있는 능력에서 우리는 UCN [3]과 비슷하지만 DeepDesc ​​[6] 정도는 비슷합니다. 
그러나 둘 다 관심 지점 감지를 수행하지 않습니다. 
반면에 LIFT [32], 최근 도입 된 SIFT의 컨볼 루션 대체는 기존의 패치 기반 탐지에 가깝고 레시피를 설명합니다.
LIFT 파이프 라인에는 관심 지점 감지, 방향 추정 및 설명자 계산이 포함되어 있지만 추가로 기존 SfM 시스템의 감독이 필요합니다. 
이러한 차이점은 표 1에 요약되어 있습니다.  
  
![table 1](./img/table1.PNG)
  
감독 스펙트럼의 다른 극단에서 Quad- Networks [23]는 감독되지 않은 접근 방식에서 관심 지점 감지 문제를 다룹니다. 
그러나 그들의 시스템은 패치 기반 (입력은 작은 이미지 패치 임)이고 비교적 얕은 2 계층 네트워크입니다. 
TILDE [29] 관심 지점 감지 시스템은 Homographic Adaptation과 유사한 원리를 사용했습니다. 
그러나 이들의 접근 방식은 대규모 완전 컨볼 루션 신경망의 힘의 이점을 얻지 못합니다.  
  
우리의 접근 방식은 다른 자체 감독 방법 인 합성에서 실제 도메인으로의 적응 방법과도 비교할 수 있습니다. 
Homographic Adaptation에 대한 유사한 접근 방식은 Honari et al. "등변 랜드 마크 변환"이라는 이름으로 [10] 또한 Geometric Matching Networks [20] 및 Deep Image Homography Estimation [4]은 유사한 자체 감독 전략을 사용하여 글로벌 변환을 추정하기위한 훈련 데이터를 생성합니다. 
그러나 이러한 방법에는 SLAM 및 SfM과 같은 더 높은 수준의 컴퓨터 비전 작업을 수행하는 데 일반적으로 필요한 관심 지점 및 지점 대응이 없습니다. 
관절 자세 및 깊이 추정 모델도 존재하지만 [33, 30, 28] 관심 지점을 사용하지 않습니다.  
  
## 3. SuperPoint Architecture
우리는 전체 크기 이미지에서 작동하고 단일 순방향 패스에서 고정 길이 설명자와 함께 관심 지점 감지를 생성하는 SuperPoint라는 완전 합성 곱 신경망 아키텍처를 설계했습니다 (그림 3 참조). 
이 모델에는 입력 이미지 차원을 처리하고 줄이기위한 단일 공유 인코더가 있습니다. 
인코더 이후 아키텍처는 두 개의 디코더 "헤드"로 분할되어 작업 별 가중치를 학습합니다. 
하나는 관심 지점 감지 용이고 다른 하나는 관심 지점 설명 용입니다. 
네트워크 매개 변수의 대부분은 두 작업간에 공유되며, 이는 먼저 관심 지점을 감지 한 다음 설명자를 계산하고 두 작업에서 계산 및 표현을 공유하는 기능이 부족한 기존 시스템과는 다릅니다.  
  
### 3.1. Shared Encoder
우리의 SuperPoint 아키텍처는 이미지의 차원을 줄이기 위해 VGG 스타일의 인코더를 사용합니다. 
인코더는 컨벌루션 레이어, 풀링을 통한 공간 다운 샘플링 및 비선형 활성화 함수로 구성됩니다. 
인코더는 3 개의 최대 풀링 레이어를 사용하므로 H × W 크기의 이미지에 대해 H<sub>c</sub> = H / 8 및 W<sub>c</sub> = W / 8을 정의 할 수 있습니다.
저 차원 출력의 픽셀을 "셀"이라고합니다. 
여기서 3 개의 2 × 인코더에서 2 개의 비 중첩 최대 풀링 작업으로 인해 8 x 8 픽셀 셀이 생성됩니다. 
인코더는 입력 이미지 I ∈ R<sup>H×W</sup>를 더 작은 공간 차원과 더 큰 채널 깊이 (즉, H<sub>c</sub> <H, W<sub>c</sub> <W 및 F> 1)로 중간 텐서 B ∈ R<sup>H<sub>c</sub>xW<sub>c</sub>xF</sup>에 매핑합니다.

### 3.2. Interest Point Decoder
관심 지점 감지의 경우 출력의 각 픽셀은 입력의 해당 픽셀에 대한 "점성"확률에 해당합니다. 
조밀 한 예측을위한 표준 네트워크 설계에는 인코더-디코더 쌍이 포함됩니다. 
여기서 공간 해상도는 풀링 또는 스트라이드 컨볼 루션을 통해 감소한 다음 SegNet [1]에서와 같이 업 컨볼 루션 작업을 통해 전체 해상도로 다시 업 샘플링됩니다.
불행히도 업 샘플링 레이어는 많은 양의 계산을 추가하는 경향이 있고 원하지 않는 바둑판 아티팩트 [18]를 도입 할 수 있으므로 모델 계산을 줄이기 위해 명시 적 디코더 1로 관심 지점 감지 헤드를 설계했습니다.  
  
관심 지점 검출기 헤드는 X ∈ R<sup>H<sub>c</sub> × W<sub>c<sub> × 65</sup>를 계산하고 텐서 크기의 R<sup>H × W</sup>를 출력합니다. 
65 개 채널은 겹치지 않는 로컬 8 × 8 그리드 픽셀 영역과 추가 "관심 지점 없음"쓰레기통에 해당합니다. 
채널 별 소프트 맥스 후 쓰레기통 치수가 제거되고 R<sup>H<sub>c</sub> × W<sub>c</sub> × 64</sup> ⇒ RH × W 모양 변경이 수행됩니다.  
  
### 3.3. Descriptor Decoder
디스크립터 헤드는 D ∈ R<sup>H<sub>c</sub> × W<sub>c</sub> × D</sup>를 계산하고 R<sup>H × W × D</sup> 크기의 텐서를 출력합니다. 
L2 정규화 된 고정 길이 설명 자의 조밀 한 맵을 출력하기 위해 UCN [3]과 유사한 모델을 사용하여 먼저 반 조밀 한 설명자 그리드 (예 : 8 픽셀마다 하나씩)를 출력합니다. 
설명자를 조밀하지 않고 반 조밀하게 학습하면 훈련 메모리가 줄어들고 런타임이 다루기 쉽습니다.
그런 다음 디코더는 디스크립터의 쌍 입방 보간을 수행 한 다음 L2는 활성화를 단위 길이로 정규화합니다. 
이 고정 된 비 학습 설명자 디코더는 그림 3에 나와 있습니다.  
  
![fig 3](./img/fig3.PNG)
###### [fig 3] SuperPoint Decoders. Both decoders operate on a shared and spatially reduced representation of the input. To keep the model fast and easy to train, both decoders use non-learned upsampling to bring the representation back to R<sup>H×W</sup>.  
  
### 3.4. Loss Functions
최종 손실은 두 개의 중간 손실의 합입니다. 
하나는 관심 지점 검출기 L<sub>p</sub> 용이고 다른 하나는 설명자 L<sub>d</sub> 용입니다. 
우리는 (a) 의사 지상 진실 관심 지점 위치와 (b) 두 이미지를 연관시키는 무작위로 생성 된 호모 그래피 H의 지상 진실 대응을 모두 갖는 합성 적으로 뒤틀린 이미지 쌍을 사용합니다. 
이를 통해 그림 2c에 표시된 것처럼 한 쌍의 이미지가 주어지면 두 손실을 동시에 최적화 할 수 있습니다. 
최종 손실의 균형을 맞추기 위해 λ를 사용합니다.  
  
![equation 1](./img/equation1.PNG)  
  
  
관심 지점 검출기 손실 함수 Lp는 셀 x<sub>hw</sub> ∈ X에 대한 완전 컨볼 루션 교차 엔트로피 손실입니다. 해당 지상 진실 관심 지점 레이블 세트 Y와 개별 항목을 y<sub>hw</sub>라고합니다. 
손실은 다음과 같습니다.  
  
![equation 2](./img/equation2.PNG)  
  
![equation 3](./img/equation3.PNG)  
  
설명자 손실은 모든 쌍의 설명자 셀에 적용되며, 첫 번째 이미지의 d<sub>hw</sub> ∈ D 및 두 번째 이미지의 d'<sub>h'w'</sub> ∈ D'입니다. 
(h, w) 셀과 (h', w') 셀 사이의 호모 그래피 유도 대응은 다음과 같이 쓸 수 있습니다.  
  
![equation 4](./img/equation4.PNG)  
  
여기서 p<sub>hw<sub>는 (h, w) 셀의 중심 픽셀 위치를 나타내고 ![](./img/img1.png)는 셀 위치 p<sub>hw</sub>에 호모 그래피 H를 곱하고 마지막 좌표로 나누는 것을 나타냅니다. 
일반적으로 유클리드 좌표와 균질 좌표 사이에서 변환 할 때 수행됩니다. 
우리는 S가있는 한 쌍의 이미지에 대한 전체 대응 집합을 나타냅니다.  
  
또한 양수보다 음의 대응이 더 많다는 사실의 균형을 맞추기 위해 가중치 용어 λ<sub>d</sub>를 추가합니다.
마진 m<sub>p</sub>와 마이너스 m<sub>n</sub>의 힌지 손실을 사용합니다. 
설명자 손실은 다음과 같이 정의됩니다.  
  
![equation 5](./img/equation5.PNG)  
  
![equation 6](./img/equation6.PNG)  
  
## 4. Synthetic PreTraining
이 섹션에서는 자체 감독 방식으로 레이블이 지정되지 않은 이미지에 대한 의사 지상 진실 관심 지점 레이블을 생성하기 위해 Homographic Adaptation과 함께 사용되는 MagicPoint라는 기본 감지기 (그림 2a에 표시)를 훈련하는 방법을 설명합니다.  
  
### 4.1. Synthetic Shapes
오늘날 존재하는 관심 지점 레이블 이미지의 큰 데이터베이스는 없습니다. 
따라서 깊은 관심 지점 감지기를 부트 스트랩하기 위해 먼저 사변형, 삼각형, 선 및 타원의 합성 데이터 렌더링을 통해 단순화 된 2D 지오메트리로 구성된 Synthetic Shapes라는 대규모 합성 데이터 세트를 만듭니다.
이러한 형태의 예는 그림 4에 나와 있습니다.
이 데이터 세트에서는 간단한 Y- 접합, L- 접합, T- 접합은 물론 작은 타원의 중심과 선 세그먼트의 끝점으로 관심 지점을 모델링하여 레이블 모호성을 제거 할 수 있습니다.  
  
![fig 4](./img/fig4.PNG)
###### Synthetic Pre-Training. We use our Synthetic Shapes dataset consisting of rendered triangles, quadrilaterals, lines, cubes, checkerboards, and stars each with ground truth corner locations. The dataset is used to train the MagicPoint convolutional neural network, which is more robust to noise when compared to classical detectors.  
  
## 4.2. MagicPoint
우리는 SuperPoint 아키텍처의 검출기 경로 (설명자 헤드 무시)를 사용하고 합성 모양에 대해 훈련합니다. 
결과 모델을 MagicPoint라고합니다.  
  
흥미롭게도 MagicPoint를 Synthetic Shapes 데이터 세트에 대한 FAST [21], Harris corners [8] 및 Shi-Tomasi의“Good Features To Track”[25]과 같은 다른 기존 모서리 감지 접근 방식과 비교하여 평가했을 때 우리의 경우에서 매우 큰 효과를 발견했습니다. 
Synthetic Shapes 데이터 세트의 1000 개의 홀드 아웃 이미지에서 평균 평균 정밀도 (mAP)를 측정하고 그 결과를 표 2에보고합니다. 
기존 검출기는 이미징 노이즈가있는 상황에서 어려움을 겪습니다. 
이에 대한 정 성적 예는 그림 4에 나와 있습니다. 더 자세한 실험은 부록 B에서 찾을 수 있습니다.  
  
![tabel 2](./img/tabel2.PNG)  
  
