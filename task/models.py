from django.db import models


# Create your models here.
class Product(models.Model):
    title = models.CharField(max_length=200)
    weight = models.FloatField()
    price = models.FloatField()
    category = models.ForeignKey('Category', on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Category(models.Model):
    # db_index used because categories are unique and it will make the lookup more efficient
    title = models.CharField(max_length=150, db_index=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Categories'


