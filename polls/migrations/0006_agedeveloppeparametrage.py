# Generated by Django 5.1.2 on 2024-11-28 20:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0005_alter_student_age_alter_student_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='AgeDeveloppeParametrage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sous_domain', models.CharField(max_length=50)),
                ('score_brut', models.IntegerField()),
                ('age_developpe', models.CharField(max_length=10)),
            ],
            options={
                'unique_together': {('sous_domain', 'score_brut')},
            },
        ),
    ]
