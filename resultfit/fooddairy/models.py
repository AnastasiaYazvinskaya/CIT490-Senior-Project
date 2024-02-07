from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User, Group
from django.utils import timezone
from recipe.models import Recipe, Product, MealType

class FoodDairyGeneral(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    kkal = models.IntegerField(verbose_name ='Ккалории', blank=True, null=True, default=None)
    proteins = models.IntegerField(verbose_name ='Белки', blank=True, null=True, default=None)
    fats = models.IntegerField(verbose_name ='Жиры', blank=True, null=True, default=None)
    carbohydrates = models.IntegerField(verbose_name ='Углеводы', blank=True, null=True, default=None)
    
    def __str__(self):
        return f'{self.kkal}/{self.proteins}/{self.fats}/{self.carbohydrates}'

# triggred when User object is created
@receiver(post_save, sender=FoodDairyGeneral)
def user_created(sender, instance, created, **kwargs):
    if created:
        pass

class DayMenu(models.Model):
    day = models.DateField(verbose_name ='День', blank=True, null=True, default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True, related_name='Пользователь')
    recipes = models.ManyToManyField(Recipe, verbose_name ='Рецепты', blank=True)

class DayNote(models.Model):
    day = models.DateField(verbose_name ='День', blank=True, null=True, default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True)

class FoodDairyNote(models.Model):
    image = models.FileField(upload_to='fooddairy/assets/media', verbose_name='image')
    mealType = models.ForeignKey(MealType, on_delete=models.PROTECT, null=True, blank=True)
    kkal = models.IntegerField(verbose_name ='Ккалории', blank=True, null=True, default=None)
    proteins = models.IntegerField(verbose_name ='Белки', blank=True, null=True, default=None)
    fats = models.IntegerField(verbose_name ='Жиры', blank=True, null=True, default=None)
    carbohydrates = models.IntegerField(verbose_name ='Углеводы', blank=True, null=True, default=None)
    recipes = models.ManyToManyField(Recipe, verbose_name ='Рецепты', blank=True)
    products = models.ManyToManyField(Product, verbose_name ='Продукты', blank=True)
    #comments = models.ManyToManyField(Comment, verbose_name ='Комментарии', blank=True)
    day = models.ForeignKey(DayNote, on_delete=models.PROTECT, null=True, blank=True, related_name='foodday')

# relocate later
class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True, related_name='Автор_комментария')
    created_by = models.DateTimeField(verbose_name ='Дата создания', blank=True, null=True, default=timezone.now)
    text = models.TextField(max_length=2000, verbose_name ='Сообщение', null=True, blank=True, default=None)
    foodNote = models.ForeignKey(FoodDairyNote, on_delete=models.PROTECT, null=True, blank=True, related_name='foodnote')

