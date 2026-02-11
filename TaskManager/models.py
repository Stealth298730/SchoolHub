from django.db import models
from Profile.models import Subject
from Resource.models import Resource

# Create your models here.

class Schedule(models.Model):
    resource = models.ForeignKey(Resource,on_delete=models.CASCADE,blank=True,verbose_name="Кабінет")
    meet_url = models.URLField(verbose_name="Посилання на урок",max_length=1000,default=None,blank=True,null=True)
    day = models.CharField(max_length=20,verbose_name="День тижня")
    number = models.PositiveIntegerField(verbose_name="Номер уроку")
    study = models.PositiveIntegerField("Клас")
    subject = models.ForeignKey(Subject,on_delete=models.CASCADE,verbose_name="Назва предмету")


    def __str__(self):
        return f"{self.subject} на {self.number} уроці ({self.study} клас)"