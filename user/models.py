from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.utils import timezone
import feed.models

USER_PROFILE_DATA = (
    'alias',
    'bio',
    'avatar'
)


class UserProfile(models.Model):
    """
    Extra data for user. (Adding new filed here make sure that you added its
    name to USER_PROFILE_DATA)
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    alias = models.CharField(max_length=250)
    bio = models.CharField(max_length=1000, null=True, blank=True)

    avatar = models.ImageField(default="default.png")
    mean_grade = models.IntegerField(default=0)
    
    def __str__(self):
        return self.user.username

    def recalculate_mean_grade(self):
        feedbacks = Feedback.objects.filter(userTo=self.user)
        mean = 0.0
        for feedback in feedbacks:
            mean += float(feedback.grade)
        if mean:
            mean = round(mean / len(feedbacks))
        self.mean_grade = mean
        self.save()

class Feedback(models.Model):
    userFrom = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='author')
    userTo = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='recipient')
    feedback_text = models.TextField(null=True, blank=True)
    grade = models.SmallIntegerField()
    published_date = models.DateTimeField(default=timezone.now)
    request = models.ForeignKey(feed.models.Request, null=True, on_delete=models.CASCADE, related_name='request')
    for_requester = models.BooleanField()

    def publish(self):
        self.save()