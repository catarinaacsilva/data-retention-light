from django.db import models
import uuid


class Contact(models.Model):
    email = models.EmailField(unique = True, null=False, primary_key=True)

class Stay_Data(models.Model):
    email = models.ForeignKey(Contact, on_delete=models.CASCADE, null=False)
    datein = models.DateTimeField(null=False)
    dateout = models.DateTimeField(null=False)
    data = models.BooleanField(null=False)
    receiptJson = models.JSONField(null=False)
    receiptid = models.UUIDField(null=False, primary_key=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['email', 'datein', 'dateout'], name='unique_stay')
        ]

class Receipt(models.Model):
    email = models.ForeignKey(Contact, on_delete=models.CASCADE, null=False)
    stayId = models.OneToOneField(Stay_Data, on_delete=models.CASCADE, null=False)
    timestamp = models.DateTimeField(null=False)


'''
class Stay(models.Model):
    stay_id = models.TextField(primary_key=True)
    start_date = models.DateField(null=False)
    end_date = models.DateField(null=False)
    receipts = models.JSONField(null=False)
'''