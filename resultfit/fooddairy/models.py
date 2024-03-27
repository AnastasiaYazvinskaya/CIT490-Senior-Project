from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User, Group
from django.utils import timezone
from recipe.models import Recipe, Product, MealType

class FoodDairyGeneral(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    kkal = models.IntegerField(verbose_name ='Ккалории', blank=True, null=True, default=0)
    proteins = models.IntegerField(verbose_name ='Белки', blank=True, null=True, default=0)
    fats = models.IntegerField(verbose_name ='Жиры', blank=True, null=True, default=0)
    carbohydrates = models.IntegerField(verbose_name ='Углеводы', blank=True, null=True, default=0)
    
    def __str__(self):
        return f'{self.kkal}/{self.proteins}/{self.fats}/{self.carbohydrates}'

# triggred when User object is created
@receiver(post_save, sender=FoodDairyGeneral)
def user_created(sender, instance, created, **kwargs):
    if created:
        pass

class MealDetail(models.Model):
    mealType = models.ForeignKey(MealType, on_delete=models.PROTECT, null=True, blank=True)
    kkal = models.IntegerField(verbose_name ='Ккалории', blank=True, null=True, default=0)
    proteins = models.IntegerField(verbose_name ='Белки', blank=True, null=True, default=0)
    fats = models.IntegerField(verbose_name ='Жиры', blank=True, null=True, default=0)
    carbohydrates = models.IntegerField(verbose_name ='Углеводы', blank=True, null=True, default=0)
    recipes = models.ForeignKey(Recipe, on_delete=models.PROTECT, verbose_name ='recipes', blank=True, null=True)
    products = models.ManyToManyField(Product, verbose_name ='Продукты', blank=True)
    is_recommend = models.BooleanField(blank=True, null=True, default=True)
    is_noted = models.BooleanField(blank=True, null=True, default=False)

class DayMenu(models.Model):
    day = models.DateField(verbose_name ='День', blank=True, null=True, default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True, related_name='Пользователь')
    #recipes = models.ManyToManyField(Recipe, verbose_name ='Рецепты', blank=True)
    braekfast = models.ForeignKey(MealDetail, related_name='breakfast', on_delete=models.PROTECT, null=True, blank=True)
    lanch = models.ForeignKey(MealDetail, related_name='lanch', on_delete=models.PROTECT, null=True, blank=True)
    dinner = models.ForeignKey(MealDetail, related_name='dinner', on_delete=models.PROTECT, null=True, blank=True)
    snack = models.ForeignKey(MealDetail, related_name='snack', on_delete=models.PROTECT, null=True, blank=True)
    kkal = models.IntegerField(verbose_name ='Ккалории', blank=True, null=True, default=0)
    proteins = models.IntegerField(verbose_name ='Белки', blank=True, null=True, default=0)
    fats = models.IntegerField(verbose_name ='Жиры', blank=True, null=True, default=0)
    carbohydrates = models.IntegerField(verbose_name ='Углеводы', blank=True, null=True, default=0)

# triggred when User object is created/updated
@receiver(post_save, sender=DayMenu)
def day_menu_created(sender, instance, created, **kwargs):
    if created:
        instance.kkal = 0
        instance.proteins = 0
        instance.fats = 0
        instance.carbohydrates = 0
        meal = MealDetail.objects.create(mealType = MealType.objects.get(pk=1), is_recommend = True, is_noted = False)
        meal.recipes = Recipe.objects.filter(privacy__name = 'Публичный', mealType__name = 'Завтрак').order_by("?").first()
        meal.kkal = meal.recipes.kkal
        meal.proteins = meal.recipes.proteins
        meal.fats = meal.recipes.fats
        meal.carbohydrates = meal.recipes.carbohydrates
        meal.save()
        instance.braekfast = meal
        meal = MealDetail.objects.create(mealType = MealType.objects.get(pk=2), is_recommend = True, is_noted = False)
        meal.recipes = Recipe.objects.filter(privacy__name = 'Публичный', mealType__name = 'Обед').order_by("?").first()
        meal.kkal = meal.recipes.kkal
        meal.proteins = meal.recipes.proteins
        meal.fats = meal.recipes.fats
        meal.carbohydrates = meal.recipes.carbohydrates
        meal.save()
        instance.lanch = meal
        meal = MealDetail.objects.create(is_recommend = True, is_noted = False)
        meal.recipes = Recipe.objects.filter(mealType = MealType.objects.get(pk=3), privacy__name = 'Публичный', mealType__name = 'Ужин').order_by("?").first()
        meal.kkal = meal.recipes.kkal
        meal.proteins = meal.recipes.proteins
        meal.fats = meal.recipes.fats
        meal.carbohydrates = meal.recipes.carbohydrates
        meal.save()
        instance.dinner = meal
        #instance.kkal = instance.braekfast.recipes.all()[0].kkal
        instance.save()


class DayNote(models.Model):
    day = models.DateField(verbose_name ='День', blank=True, null=True, default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True)

class FoodDairyNote(models.Model):
    image = models.FileField(upload_to='fooddairy/assets/media', verbose_name='image', null=True, blank=True)
    mealType = models.ForeignKey(MealType, on_delete=models.PROTECT, null=True, blank=True)
    kkal = models.IntegerField(verbose_name ='Ккалории', blank=True, null=True, default=0)
    proteins = models.IntegerField(verbose_name ='Белки', blank=True, null=True, default=0)
    fats = models.IntegerField(verbose_name ='Жиры', blank=True, null=True, default=0)
    carbohydrates = models.IntegerField(verbose_name ='Углеводы', blank=True, null=True, default=0)
    recipes = models.ForeignKey(Recipe, on_delete=models.PROTECT, verbose_name ='Рецепты', blank=True, null=True)
    products = models.ManyToManyField(Product, verbose_name ='Продукты', blank=True)
    #comments = models.ManyToManyField(Comment, verbose_name ='Комментарии', blank=True)
    day = models.ForeignKey(DayNote, on_delete=models.PROTECT, null=True, blank=True, related_name='foodday')

# relocate later
class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True, related_name='Автор_комментария')
    created_by = models.DateTimeField(verbose_name ='Дата создания', blank=True, null=True, default=timezone.now)
    text = models.TextField(max_length=2000, verbose_name ='Сообщение', null=True, blank=True, default=None)
    foodNote = models.ForeignKey(FoodDairyNote, on_delete=models.PROTECT, null=True, blank=True, related_name='foodnote')

