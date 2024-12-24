# EasyCruit - 기업 맞춤형 채용 지원 서비스

![프로젝트 로고](https://github.com/user-attachments/assets/16eadf83-a8d4-464b-8fe0-fa03f0f96c6f)

## 01. 프로젝트 정보

### 프로젝트 개요  
- **단체**: 교보 DTS Cloud Architecture DX Academy  
- **개발 기간**: 10/28 ~ 12/2 (추가 개발 진행 중)  

### 팀 소개  
| 이름       | 역할                                |
|------------|-------------------------------------|
| **김지후** | 팀장, 백엔드 및 프론트엔드 개발, 아키텍처 설계 및 구축, 부하 테스트 |
| **김재현** | UI 개발, 기획서 및 PPT 작성, 아키텍처 설계         |
| **정종호** | 프론트 개발, 아키텍처 설계, 부하 테스트          |
| **황원준** | 아키텍처 조사, UI 개발, 문서 정리              |

### 프로젝트 동기  
1. **지원 과정 개선**: 구글폼 기반 지원서 접수는 신뢰도를 떨어뜨릴 수 있음
2. **비효율성 해결**: Linkareer와 잡플래닛을 통해 접속해도 최종적으로 회사 개별 웹사이트로 이동해야 하는 번거로움이 존재함

### 프로젝트 설명  
- 회사가 지원서 생성, 수집, 열람을 쉽게 할 수 있도록 **SaaS 서비스** 제공
- SaaS 서비스와 연계된 회사 개별 채용 웹사이트도 함께 제공

### 기대 효과  
- **회사 측**: Linkareer, 잡플래닛과 연계된 채용 플랫폼과 개별 채용 웹사이트를 통해 지원자를 모집할 수 있음
- **지원자 측**: 여러 번 로그인할 필요 없이 다양한 회사에 손쉽게 지원 가능

---

## 02. 기술 스택  

![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)  
![JavaScript](https://img.shields.io/badge/JavaScript-323330?style=for-the-badge&logo=javascript&logoColor=F7DF1E)  
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)  
![Kubernetes](https://img.shields.io/badge/Kubernetes-326CE5?style=for-the-badge&logo=kubernetes&logoColor=white)  
![AWS](https://img.shields.io/badge/AWS-FF9900?style=for-the-badge&logo=amazon-aws&logoColor=white)  
![Prometheus](https://img.shields.io/badge/Prometheus-E6522C?style=for-the-badge&logo=prometheus&logoColor=white)  
![Grafana](https://img.shields.io/badge/Grafana-F46800?style=for-the-badge&logo=grafana&logoColor=white)  

---

## 03. 화면 구성  

### 지원자 입장  
![지원자 화면](https://github.com/user-attachments/assets/afaf67b8-d77e-459b-9683-099602aec955)

### 채용 담당자 입장  
![채용 담당자 화면](https://github.com/user-attachments/assets/185ddd15-b59f-4f75-921f-609c0e3ca5bb)

---

## 04. 아키텍처  

![아키텍처 이미지 1](https://github.com/user-attachments/assets/3ead5f9c-c9ff-43d3-8fd2-f9bbdff36873)  
![아키텍처 이미지 2](https://github.com/user-attachments/assets/c2506275-b89e-4e8f-a45c-0b87d20c1fb6)

- **SaaS 서비스**: 변화하는 트래픽에 대응하기 위해 **EKS** 환경에 배포 (상시 운영).  
- **회사 개별 지원 웹사이트**: 예측 가능한 트래픽에 따라 **ECS** 환경에 배포 (채용 기간에만 운영).  

---

## 05. 모니터링 및 오토스케일링 (Kubernetes HPA)  

![HPA 이미지](https://github.com/user-attachments/assets/15661d78-ac8a-4f3e-ae7f-03f8ca0b6714)

### Apply Service 목표  
- **총 지원자**: 10,000명  
- **동시 접속자 비율**: 10%  
- **목표 RPS**: 1,000  

**부하 테스트 결과**:  
- **Apply pod**: 1개당 **326 RPS** 수용 가능  
  ![부하 테스트 1](https://github.com/user-attachments/assets/ce7ab3f9-8999-43a0-8dda-cca52efe5d9c)  
- **Max Replica**: 4  
- **최대 RPS**: 1,002  
  ![부하 테스트 2](https://github.com/user-attachments/assets/014964d5-3031-43ed-a28a-b19c488230e5)  

### Employ Service 목표  
- **총 담당자**: 4,000명  
- **동시 접속자 비율**: 10%  
- **목표 RPS**: 400  

**부하 테스트 결과**:  
- **Employ pod**: 1개당 **113 RPS** 수용 가능  
  ![부하 테스트 3](https://github.com/user-attachments/assets/180dc248-1373-4240-9c61-d30c4b537a6e)  
- **Max Replica**: 4  
- **최대 RPS**: 440  
  ![부하 테스트 4](https://github.com/user-attachments/assets/ceeabae1-576b-412e-ac08-da9f972d9d21)  

---