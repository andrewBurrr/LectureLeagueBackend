from django.db import models

# Create your models here.


class Rating(models.Model):
    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE)
    section = models.ForeignKey('institutions.Section', on_delete=models.CASCADE)
    difficulty = models.FloatField()
    workload = models.FloatField()
    utility = models.FloatField()
    quality = models.FloatField()
    comment = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user} - {self.section} - {self.date_created}'


class Vote(models.Model):
    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE)
    rating = models.ForeignKey(Rating, on_delete=models.CASCADE)
    vote = models.BooleanField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user} - {self.rating} - {self.date_created}'
