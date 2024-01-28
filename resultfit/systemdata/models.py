from django.db import models

class ActivityType(models.Model):
    name = models.CharField(max_length=20, verbose_name ='Тип', null=True, default=None)
    description = models.CharField(max_length=200, verbose_name ='Описание', blank=True, null=True, default=None)
    rate = models.FloatField(verbose_name ='Коэффициент', null=True, default=None)
    active = models.BooleanField(default=True, verbose_name ='Активный', blank=True)

    def __str__(self):
        return self.name

class PurposeType(models.Model):
    name = models.CharField(max_length=20, verbose_name ='Название', null=True, default=None)
    proteins_rate_min = models.IntegerField(verbose_name ='Минимальный % белков', blank=True, null=True, default=None)
    proteins_rate_max = models.IntegerField(verbose_name ='Максимальный % белков', blank=True, null=True, default=None)
    fats_rate_min = models.IntegerField(verbose_name ='Минимальный % жиров', blank=True, null=True, default=None)
    fats_rate_max = models.IntegerField(verbose_name ='Максимальный % жиров', blank=True, null=True, default=None)
    carbohydrates_rate_min = models.IntegerField(verbose_name ='Минимальный % углеводов', blank=True, null=True, default=None)
    carbohydrates_rate_max = models.IntegerField(verbose_name ='Максимальный % углеводов', blank=True, null=True, default=None)
    active = models.BooleanField(default=True, verbose_name ='Активный', blank=True)

    def __str__(self):
        return self.name
    
class PrivacyType(models.Model):
    name = models.CharField(max_length=20, verbose_name ='Название', null=True, default=None)
    description = models.CharField(max_length=200, verbose_name ='Описание', blank=True, null=True, default=None)
    active = models.BooleanField(default=True, verbose_name ='Активный', blank=True)

    def __str__(self):
        return self.name
    
class UnitType(models.Model):
    name = models.CharField(max_length=20, verbose_name ='Название', null=True, default=None)
    full_name = models.CharField(max_length=50, verbose_name ='Полное_название', null=True, default=None)
    description = models.CharField(max_length=200, verbose_name ='Описание', blank=True, null=True, default=None)
    active = models.BooleanField(default=True, verbose_name ='Активный', blank=True)

    def __str__(self):
        return self.name
    
class Product(models.Model):
    name = models.CharField(max_length=20, verbose_name ='Название', null=True, default=None)
    kkal = models.IntegerField(verbose_name ='Ккалории', blank=True, null=True, default=None)
    proteins = models.IntegerField(verbose_name ='Белки', blank=True, null=True, default=None)
    fats = models.IntegerField(verbose_name ='Жиры', blank=True, null=True, default=None)
    carbohydrates = models.IntegerField(verbose_name ='Углеводы', blank=True, null=True, default=None)
    baseUnit = models.ForeignKey(UnitType, on_delete=models.PROTECT, null=True, blank=True, related_name='Стандартная_ед_измерения')
    active = models.BooleanField(default=True, verbose_name ='Активный', blank=True)

    def __str__(self):
        return self.name
    
