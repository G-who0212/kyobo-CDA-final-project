from django.db import models

class Application(models.Model):
    name = models.CharField(max_length=50)
    date_of_birth = models.CharField(max_length=6)  # '990212' format
    phone_num = models.CharField(max_length=15)
    email = models.EmailField(max_length=100)
    residence = models.CharField(max_length=100)
    educational_background = models.CharField(max_length=50)  # e.g., '학사'
    school = models.CharField(max_length=100)
    major = models.CharField(max_length=100)
    certificate = models.CharField(max_length=200)  # e.g., 'sqld, CKA'
    it_experience = models.CharField(max_length=200)  # e.g., '관광데이터 공모전 / 장려상'
    education_experience = models.CharField(max_length=50)  # e.g., '3개월 이상'
    it_career_experience = models.CharField(max_length=50)  # e.g., '6개월 ~ 1년'
    card_possession = models.CharField(max_length=100)  # e.g., '내일배움카드가 있습니다.'
    motivation_career_plan = models.TextField()  # Detailed career motivation
    source_of_info = models.CharField(max_length=100)  # e.g., '자소설닷컴'

    def __str__(self):
        return f"{self.name} - {self.email}"