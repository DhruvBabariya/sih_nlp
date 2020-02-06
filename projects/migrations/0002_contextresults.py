# Generated by Django 2.2.1 on 2020-02-06 10:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContextResults',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('original_average_rating', models.FloatField()),
                ('predicted_average_rating', models.FloatField()),
                ('num_of_reviews', models.IntegerField(max_length=10)),
                ('aspects_rating', models.TextField(max_length=5000)),
                ('project', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='projects.Project')),
            ],
        ),
    ]
