# EasyCruit - 기업 맞춤형 채용 지원 서비스

<!-- ![프로젝트 로고](https://github.com/user-attachments/assets/16eadf83-a8d4-464b-8fe0-fa03f0f96c6f) -->
<img src="https://github.com/user-attachments/assets/16eadf83-a8d4-464b-8fe0-fa03f0f96c6f" alt="프로젝트 로고" width="300"/>

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
<div align=center> 
    <img src="https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white"> 
    <img src="https://img.shields.io/badge/JavaScript-323330?style=for-the-badge&logo=javascript&logoColor=F7DF1E">
    <img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white"> 
    <br>
    <img src="https://img.shields.io/badge/Kubernetes-326CE5?style=for-the-badge&logo=kubernetes&logoColor=white">
    <img src="https://img.shields.io/badge/AWS-FF9900?style=for-the-badge&logo=amazon-aws&logoColor=white">
    <img src="https://img.shields.io/badge/Prometheus-E6522C?style=for-the-badge&logo=prometheus&logoColor=white">
    <img src="https://img.shields.io/badge/Grafana-F46800?style=for-the-badge&logo=grafana&logoColor=white">
    <br>
</div>


<!-- ## 02. 기술 스택  

![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)  
![JavaScript](https://img.shields.io/badge/JavaScript-323330?style=for-the-badge&logo=javascript&logoColor=F7DF1E)  
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)  
![Kubernetes](https://img.shields.io/badge/Kubernetes-326CE5?style=for-the-badge&logo=kubernetes&logoColor=white)  
![AWS](https://img.shields.io/badge/AWS-FF9900?style=for-the-badge&logo=amazon-aws&logoColor=white)  
![Prometheus](https://img.shields.io/badge/Prometheus-E6522C?style=for-the-badge&logo=prometheus&logoColor=white)  
![Grafana](https://img.shields.io/badge/Grafana-F46800?style=for-the-badge&logo=grafana&logoColor=white)   -->

---

## 03. 화면 구성  

### 지원자 입장  
![지원자 화면](https://github.com/user-attachments/assets/afaf67b8-d77e-459b-9683-099602aec955)

### 채용 담당자 입장  
![채용 담당자 화면](https://github.com/user-attachments/assets/185ddd15-b59f-4f75-921f-609c0e3ca5bb)

---

## 04. 아키텍처  
### 전체 아키텍처
<img src="https://github.com/user-attachments/assets/74cae740-f70c-4e40-bcb8-76eece6d440b" alt="프로젝트 로고" width="800"/>

- **SaaS 서비스**: 변화하는 트래픽에 대응하기 위해 **EKS** 환경에 배포 (상시 운영).  
- **회사 개별 지원 웹사이트**: 예측 가능한 트래픽에 따라 **ECS** 환경에 배포 (채용 기간에만 운영).  

### K8S(EKS) 구성
<img src="https://github.com/user-attachments/assets/c2506275-b89e-4e8f-a45c-0b87d20c1fb6" alt="프로젝트 로고" width="700"/>

- **Namespace 분리**: **EasyCruit namespace** / **Monitoring namespace**
- **Ingress**: 여러 서비스 트래픽을 단일 Load Balancer로 처리
- **HPA (Horizontal Pod Autoscaling)**: 변화하는 트래픽에 유연하게 대응하기 위해 Apply Service와 Employ Service에 대하여 Autoscaling 적용



---

## 05. 모니터링 및 오토스케일링 (Kubernetes HPA)  

![HPA 이미지](https://github.com/user-attachments/assets/340bcf88-bf6b-4128-b0a9-e62040f42d60)

### Apply Service 목표  
- **총 지원자**: 10,000명  
- **동시 접속자 비율**: 10%  
- **목표 RPS**: 1,000  

**부하 테스트 결과**:  
- **Apply pod**: 1개당 **345 RPS** 수용 가능  
  ![부하 테스트 1](https://github.com/user-attachments/assets/ce7ab3f9-8999-43a0-8dda-cca52efe5d9c)  
- **Max Replica**: 4  
- **Apply Service의 최대 RPS**: 1,002  
  ![부하 테스트 2](https://github.com/user-attachments/assets/014964d5-3031-43ed-a28a-b19c488230e5)  

### Employ Service 목표  
- **총 채용담당자**: 3,000명  
- **동시 접속자 비율**: 10%  
- **목표 RPS**: 300  

**부하 테스트 결과**:  
- **Employ pod**: 1개당 **96 RPS** 수용 가능  
  ![부하 테스트 3](https://github.com/user-attachments/assets/180dc248-1373-4240-9c61-d30c4b537a6e)  
- **Max Replica**: 4  
- **Employ Service의 최대 RPS**: 440  
  ![부하 테스트 4](https://github.com/user-attachments/assets/ceeabae1-576b-412e-ac08-da9f972d9d21)  

---