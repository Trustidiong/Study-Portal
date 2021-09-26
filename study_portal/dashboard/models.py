from django.db import models
from django.contrib.auth.models import User

# For the UNote app
class Notes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    
    # DISPLAY TILE OF THE NOTES
    def __str__(self):
        return self.title
    
    # ADD META CLASS TO FORCE THE NAME FROM NOTESS TO NOTES
    class Meta:
        verbose_name = "notes"
        verbose_name_plural = "notes"
    

# For the Homework app
class Homework(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=50)
    title = models.CharField(max_length=100)
    description = models.TextField()
    due = models.DateTimeField()
    is_finished = models.BooleanField()
    
    def __str__(self):
        return self.title


class Todo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    is_finished = models.BooleanField()

    def __str__(self):
        return self.title
