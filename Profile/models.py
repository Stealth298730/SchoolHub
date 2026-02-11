from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
# Create your models here.

class Action(models.Model):
    class ActionChoice(models.TextChoices):
        CREATEBOOKING = "CB", _("CreateBooking")
        READBOOKING = "RB", _("ReadBooking")
        UPDATEBOOKING = "UB", _("UpdateBooking")
        CREATESCHEDULE = "CS",_("CreateSchedule")
        READSCHEDULE = "RS",_("ReadSchedule")

    name = models.CharField(
        max_length=100,
        verbose_name="Дозволена дія",
        help_text="Введіть назву дії",
        choices=ActionChoice.choices,
        default=ActionChoice.READBOOKING
        )

    def __str__(self):
        return f"Назва дії:{self.name}"


class Position(models.Model):
    name = models.CharField(max_length=100,verbose_name="Посада",help_text="Введіть посаду")
    actions = models.ManyToManyField(Action,verbose_name="Список дозволів",help_text="Виберіть дії, які можна виконати")

    def __str__(self):
        return f"Посада:{self.name}|Дії:{','.join([action.name for action in self.actions.all()])}"
    


class Subject(models.Model):
    name = models.CharField(max_length=150,verbose_name="Назва предмета",help_text="Введіть назву предмету")

    def __str__(self):
        return f"Назва предмету:{self.name}"
    

class ClassRoom(models.Model):
    name = models.TextField(max_length=30,verbose_name="Назва класу")
    description = models.CharField(max_length=255,verbose_name="Опис класу",default=None,null=True,blank=True)
    subjects = models.ManyToManyField(Subject,blank=True,default=None,verbose_name="Список предметів")

    def __str__(self):
        return f"{self.name} клас"


class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    positions = models.ManyToManyField(Position,blank=True,default=None)
    class_room = models.ForeignKey(ClassRoom,on_delete=models.CASCADE,null=True,default=None,blank=True)
    avatar = models.ImageField(upload_to=".",verbose_name="Аватарка",null=True,blank=True,default=None)
    bio = models.TextField(verbose_name="Про себе",null=True,blank=True,default=None,help_text="біографія")
    phone_number = models.CharField(max_length=20,null=True,blank=True,default=None,verbose_name="Номер телефону",help_text="Введіть номер телефону")

    def __str__(self):
        return f"Користувач:{self.user.get_full_name()}|Предмети: {self.class_room}"
