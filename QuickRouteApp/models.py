from django.db import models

class Route(models.Model):
    start = models.CharField(max_length=2)
    pickup = models.CharField(max_length=2)
    delivery = models.CharField(max_length=2)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.start} to {self.delivery} on {self.date.strftime('%Y-%m-%d %H:%M')}"
