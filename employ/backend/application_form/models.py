from mongoengine import Document, ReferenceField, DictField, DateTimeField, StringField
from datetime import datetime

# 회사 모델
class Company(Document):
    company_name = StringField(required=True, max_length=100, unique=True)  # 회사 이름

    def __str__(self):
        return self.company_name

# 부서별 지원서 양식 모델
class ApplicationForm(Document):
    company = ReferenceField('Company', required=True)  # 회사와 연결
    department = StringField(required=True, max_length=100)  # 부서 이름
    form_schema = DictField()  # 지원서 양식 (JSON 형태로 저장)

    def __str__(self):
        return f"{self.company.company_name} - {self.department}"

# 지원서 데이터 모델
class Application(Document):
    form = ReferenceField('ApplicationForm', required=True)  # 부서별 양식과 연결
    applicant_name = StringField(required=True, max_length=100)  # 지원자 이름
    application_data = DictField()  # 지원자가 작성한 데이터
    created_at = DateTimeField(default=datetime.utcnow)  # 지원서 제출 시각

    def __str__(self):
        return f"{self.applicant_name} - {self.form.company.company_name} ({self.form.department})"