from django.db import models
from django.contrib.auth.models import User
from systemdata.models import PrivacyType, Product, UnitType, MealType

class Recipe(models.Model):
    author = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True, related_name='Автор')
    name = models.CharField(max_length=100, verbose_name ='Название', null=True, default=None)
    privacy = models.ForeignKey(PrivacyType, on_delete=models.PROTECT, null=True, blank=True, related_name='Доступ', default=2)
    active = models.BooleanField(default=True, verbose_name ='Активность', blank=True)
    kkal = models.IntegerField(verbose_name ='Ккалории', blank=True, null=True, default=None)
    proteins = models.IntegerField(verbose_name ='Белки', blank=True, null=True, default=None)
    fats = models.IntegerField(verbose_name ='Жиры', blank=True, null=True, default=None)
    carbohydrates = models.IntegerField(verbose_name ='Углеводы', blank=True, null=True, default=None)
    mealType = models.ForeignKey(MealType, on_delete=models.PROTECT, null=True, blank=True, related_name='Прием_пищи')
    description = models.CharField(max_length=100, verbose_name ='Описание', null=True, default=None)
    
    def __str__(self):
        return self.name
   
class Ingredient(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT, null=True, blank=True, related_name='Продукт')
    amount = models.FloatField(verbose_name ='Количество', null=True, default=None)
    unitType = models.ForeignKey(UnitType, on_delete=models.PROTECT, null=True, blank=True, related_name='Ед_измерения')
    recipe = models.ForeignKey(Recipe, on_delete=models.PROTECT, null=True, blank=True, related_name='Рецепт')
    
    def __str__(self):
        return self.product.name

