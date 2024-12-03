# Generated by Django 5.1.2 on 2024-12-02 23:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_rename_gender_customer_sex_rename_gender_teacher_sex'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_date', models.DateField()),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('paid', 'Paid'), ('failed', 'Failed'), ('refunded', 'Refunded')], max_length=10)),
                ('grade', models.PositiveIntegerField(blank=True, null=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.course')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.customer')),
            ],
            options={
                'unique_together': {('customer', 'course', 'payment_date')},
            },
        ),
        migrations.AddField(
            model_name='course',
            name='customers',
            field=models.ManyToManyField(through='api.Payment', to='api.customer'),
        ),
        migrations.DeleteModel(
            name='CustomerCourse',
        ),
    ]