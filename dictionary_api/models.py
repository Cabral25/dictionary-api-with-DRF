from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
        AbstractUser permite customizar o User padrão do Django.
    """
    id = models.IntegerField()
    email = models.EmailField()



class Word(models.Model):
    word_id = models.IntegerField()
    word = models.CharField()
    meaning = models.TextField()
    example = models.TextField()
    slug = models.SlugField(unique=True, blank=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

# Create your models here.
