from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from django_elasticsearch_dsl.registries import registry


@receiver(post_save)
def update_document(sender, **kwargs):
    """Update document on added/changed records.
    Update Product document index if related `product.Category` (`category`),
    fields have been updated in the database.
    """
    app_label = sender._meta.app_label
    model_name = sender._meta.model_name
    instance = kwargs['instance']

    if app_label == 'product':
        # If it is `product.Category` that is being updated.
        if model_name == 'category':
            instances = instance.product.all()
            for _instance in instances:
                registry.update(_instance)


@receiver(post_delete)
def delete_document(sender, **kwargs):
    """Update document on deleted records.
    Updates Book document from index if related `product.Category`
    have been removed from database.
    """
    app_label = sender._meta.app_label
    model_name = sender._meta.model_name
    instance = kwargs['instance']

    if app_label == 'product':
        # If it is `product.Publisher` that is being updated.
        if model_name == 'category':
            instances = instance.product.all()
            for _instance in instances:
                registry.update(_instance)
                # registry.delete(_instance, raise_on_error=False)
