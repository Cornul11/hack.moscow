from django.db import models


class Users(models.Model):
    email = models.CharField(max_length=50, primary_key=True)
    password = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    age = models.PositiveSmallIntegerField()
    gender = models.CharField(max_length=10)


class Interests(models.Model):
    name = models.CharField(max_length=50, primary_key=True)


class UsersInterests(models.Model):
    email = models.ForeignKey(Users, on_delete=models.CASCADE)
    interest = models.ForeignKey(Interests, on_delete=models.CASCADE)


class Shops(models.Model):
    name = models.CharField(max_length=100)
    email = models.ForeignKey(Users, on_delete=models.CASCADE)
    start_time = models.TimeField(auto_now_add=True)
    duration = models.PositiveIntegerField()
    start = models.PositiveSmallIntegerField(null=True)



