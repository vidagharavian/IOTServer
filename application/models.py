from django.db import models
from django.db.models import JSONField


# Create your models here.

class Branch(models.Model):
    Restaurant = "RS"
    CoffeeShop = "CS"
    Mall = "ML"
    Hospital = "HL"
    BranchCategory = [
        (Restaurant, "Restaurant"),
        (CoffeeShop, "CoffeeShop"),
        (Hospital, "Hospital"),
        (Mall, "Mall"),
    ]
    category = models.CharField(
        max_length=2,
        choices=BranchCategory,
        default=Restaurant,
    )
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name

class ServiceProvider(models.Model):
    branch = models.ForeignKey(Branch,on_delete=models.CASCADE)
    lat = models.FloatField(blank=True,null=True)
    lan = models.FloatField(blank=True,null=True)

    def __str__(self):
        return self.branch.name
class Service(models.Model):
    service_name = models.CharField(max_length=200,null=True,blank=True)
    def __str__(self):
        return self.service_name

class ServiceServiceProvider(models.Model):
    service_provider = models.ForeignKey(ServiceProvider, on_delete=models.CASCADE, null=True, blank=True)
    service = models.ForeignKey(Service,on_delete=models.CASCADE,null=True,blank=True)
    def __str__(self):
        return self.service.service_name+self.service_provider.branch.name






def contact_default():
    return {"info": "frame"}


class SPFrame(models.Model):
    image = models.ImageField(upload_to="templates/image/",null=True,blank=True)
    head_coordinate = models.TextField()
    creation_date = models.DateTimeField(null=True,blank=True)
    service_provider = models.ForeignKey(ServiceProvider,on_delete=models.CASCADE,null=True,blank=True)
    def __str__(self):
        return self.service_provider.branch.name


class CustomerWaitingTime(models.Model):
    start_date = models.IntegerField(null=True)
    last_updated = models.IntegerField(null=True,blank=True)
    x = models.IntegerField()
    y = models.IntegerField()
    height= models.IntegerField()
    weight = models.IntegerField()
    service_provider = models.ForeignKey(ServiceProvider,on_delete=models.CASCADE)
    updatable = models.BooleanField(default=True)


