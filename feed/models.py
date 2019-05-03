from django.db import models
from django.conf import settings
from django.utils import timezone


class Offer(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    service_type = models.CharField(max_length=200)
    price = models.CharField(max_length=100)
    start_date = models.DateField(blank=True, null=True)
    deadline = models.DateField(blank=True, null=True)
    offer_description = models.TextField(null=True)
    image = models.ImageField(blank=True, null=True)
    published_date = models.DateTimeField(default=timezone.now)
    closed = models.BooleanField(default=False)

    def publish(self):
        self.save()

    def __str__(self):
        return self.title


class Request(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    performer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True,
                                  related_name='performer')
    visible = models.BooleanField()
    closed = models.BooleanField(default=False)
    title = models.CharField(max_length=200)
    service_type = models.CharField(max_length=200)
    price = models.CharField(max_length=100)
    start_date = models.DateField()
    deadline = models.DateField()
    request_description = models.TextField()
    image = models.ImageField(blank=True, null=True)
    published_date = models.DateTimeField(default=timezone.now)

    def publish(self):
        self.save()

    def __str__(self):
        return self.title


class RespondRequest(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    request_id = models.ForeignKey(Request, on_delete=models.CASCADE)
    message = models.TextField()
    respond_date = models.DateTimeField(default=timezone.now)

    def publish(self):
        self.save()

    def __str__(self):
        return self.message

class RespondOffer(models.Model): 
    offer = models.ForeignKey(Offer, on_delete=models.PROTECT)
    request_as_response = models.ForeignKey(Request, on_delete=models.PROTECT)
