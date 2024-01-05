from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Note(models.Model):
    owner= models.ForeignKey(User, on_delete=models.CASCADE)
    description= models.TextField()
    shared_with= models.ManyToManyField(User, related_name='shared_notes')

    def __str__(self) -> str:
        return self.owner.username + ': ' + self.description
