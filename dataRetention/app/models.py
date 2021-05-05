from django.db import models
import uuid


class User(models.Model):
    email = models.EmailField(unique = True, null=False, primary_key=True)

class Stay_Data(models.Model):
    email = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    datein = models.DateField(null=False)
    dateout = models.DateField(null=False)
    data = models.BooleanField(null=False)
    receipt = models.JSONField(null=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['email', 'datein', 'dateout'], name='unique_stay')
        ]


'''
class Stay(models.Model):
    stay_id = models.TextField(primary_key=True)
    start_date = models.DateField(null=False)
    end_date = models.DateField(null=False)
    receipts = models.JSONField(null=False)
'''