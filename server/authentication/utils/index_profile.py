from django.db.models.signals import post_save
from django.dispatch import receiver
from elasticsearch import Elasticsearch
from myapp.models import Profile

es = Elasticsearch()

@receiver(post_save, sender=Profile)
def index_profile(sender, instance, **kwargs):
    es.index(
        index='profiles',
        id=instance.id,
        body={
            'username': instance.username,
            'full_name': instance.full_name,
            'email': instance.email,
            'other_fields': instance.other_fields, 
        }
    )