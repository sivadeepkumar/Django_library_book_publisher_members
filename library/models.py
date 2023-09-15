from django.db import models

# Create your models here.


class Publisher(models.Model):
    publisher = models.CharField(max_length=100)
    address = models.TextField()

    def __str__(self) -> str:
        return self.publisher
    


class Book(models.Model):
    published_by = models.ForeignKey(Publisher,on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    price = models.IntegerField()
    availability = models.BooleanField(default=True)
    count = models.IntegerField(default=1)

    def __str__(self) -> str:
        return f'Title: {self.title}, Author : {self.author}'

class Member(models.Model):
    book_title = models.ForeignKey(Book,on_delete=models.CASCADE)
    member_name = models.CharField(max_length=100)
    age  = models.IntegerField(default=18)
    address = models.TextField()

    def __str__(self) -> str:
        return self.member_name