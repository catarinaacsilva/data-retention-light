from django.db import models
import uuid

class Stay(models.Model):
    stay_id = models.TextField(primary_key=True)
    start_date = models.DateField(null=False)
    end_date = models.DateField(null=False)
    receipts = models.JSONField(null=False)