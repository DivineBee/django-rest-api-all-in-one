from django.db import models


class Product(models.Model):
    title = models.CharField(max_length=200)
    weight = models.FloatField()
    price = models.FloatField()
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='products')

    def __str__(self):
        return self.title

    @property
    def category_indexing(self):
        """Category for indexing.  Used in Elasticsearch indexing."""
        if self.category is not None:
            return self.category.title

    class Meta:
        ordering = ['id']


class Category(models.Model):
    # db_index used because categories are unique and it will make the lookup more efficient
    title = models.CharField(max_length=150, db_index=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['id']
        verbose_name_plural = 'Categories'


