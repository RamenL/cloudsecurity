from django.db import models
from django.contrib.postgres.fields import ArrayField

class FileDetails(models.Model):
    owner = models.CharField(max_length=200)
    file_name = models.CharField(max_length=2000)
    file_type = models.CharField(max_length=7)
    head_id = models.IntegerField()
    head_table = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    def __str__(self):
        return self.file_name

class FilePartitionOne(models.Model):
    byte_array = models.BinaryField()
    next_id = models.IntegerField()
    next_table = models.IntegerField()
    def __str__(self):
        return self.id

class FilePartitionTwo(models.Model):
    byte_array = models.BinaryField()
    next_id = models.IntegerField()
    next_table = models.IntegerField()
    def __str__(self):
        return self.id

class FilePartitionThree(models.Model):
    byte_array = models.BinaryField()
    next_id = models.IntegerField()
    next_table = models.IntegerField()
    def __str__(self):
        return self.id

class FilePartitionFour(models.Model):
    byte_array = models.BinaryField()
    next_id = models.IntegerField()
    next_table = models.IntegerField()
    def __str__(self):
        return self.id