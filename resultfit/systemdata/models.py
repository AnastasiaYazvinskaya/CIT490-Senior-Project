from django.db import models

class ActivityType(models.Model):
    name = models.CharField(max_length=20, verbose_name ='Тип', null=True, default=None)
    description = models.CharField(max_length=200, verbose_name ='Описание', blank=True, null=True, default=None)
    rate = models.FloatField(verbose_name ='Коэффициент', null=True, default=None)

    def __str__(self):
        return self.name

class PurposeType(models.Model):
    name = models.CharField(max_length=20, verbose_name ='Тип', null=True, default=None)
    proteins_rate_min = models.IntegerField(verbose_name ='Минимальный % белков', blank=True, null=True, default=None)
    proteins_rate_max = models.IntegerField(verbose_name ='Максимальный % белков', blank=True, null=True, default=None)
    fats_rate_min = models.IntegerField(verbose_name ='Минимальный % жиров', blank=True, null=True, default=None)
    fats_rate_max = models.IntegerField(verbose_name ='Максимальный % жиров', blank=True, null=True, default=None)
    carbohydrates_rate_min = models.IntegerField(verbose_name ='Минимальный % углеводов', blank=True, null=True, default=None)
    carbohydrates_rate_max = models.IntegerField(verbose_name ='Максимальный % углеводов', blank=True, null=True, default=None)

    def __str__(self):
        return self.name
    