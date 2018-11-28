from django.db import models

# Create your models here.
class Image(models.Model):
    name = models.CharField(max_length=30,unique=True)
    width = models.FloatField(null=True)
    height = models.FloatField(null=True)
    location = models.CharField(max_length=30,null=True)

    def __str__(self):
        return self.name

class BoundingBox(models.Model):
    image = models.ForeignKey(Image,on_delete=models.CASCADE)
    pointer_x = models.FloatField(null=True)
    pointer_y = models.FloatField(null=True)
    box_width = models.FloatField(null=True)
    box_height = models.FloatField(null=True)
    label = models.CharField(max_length=30, null=True)

    def __str__(self):
        return self.label

