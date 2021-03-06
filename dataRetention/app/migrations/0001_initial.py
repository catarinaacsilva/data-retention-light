# Generated by Django 3.1.7 on 2021-05-11 10:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('email', models.EmailField(max_length=254, primary_key=True, serialize=False, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Stay_Data',
            fields=[
                ('datein', models.DateTimeField()),
                ('dateout', models.DateTimeField()),
                ('data', models.BooleanField()),
                ('receiptJson', models.JSONField()),
                ('receiptid', models.UUIDField(primary_key=True, serialize=False)),
                ('email', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.user')),
            ],
        ),
        migrations.CreateModel(
            name='Receipt',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField()),
                ('email', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.user')),
                ('stayId', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='app.stay_data')),
            ],
        ),
        migrations.AddConstraint(
            model_name='stay_data',
            constraint=models.UniqueConstraint(fields=('email', 'datein', 'dateout'), name='unique_stay'),
        ),
    ]
