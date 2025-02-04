# Generated by Django 5.1.2 on 2024-11-28 16:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0003_alter_student_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='AgeTranche',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=3)),
                ('label', models.CharField(max_length=100)),
                ('min_months', models.IntegerField()),
                ('max_months', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='ScoreParametrage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('domain', models.CharField(max_length=50)),
                ('sous_domain', models.CharField(max_length=50)),
                ('score_brut', models.IntegerField()),
                ('ns', models.IntegerField()),
                ('percentile', models.CharField(max_length=10)),
                ('age_developpe', models.CharField(max_length=10)),
                ('tranche', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.agetranche')),
            ],
        ),
        migrations.CreateModel(
            name='StudentScore',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('domain', models.CharField(max_length=50)),
                ('sous_domain', models.CharField(max_length=50)),
                ('score_brut', models.IntegerField()),
                ('ns', models.IntegerField(null=True)),
                ('percentile', models.CharField(max_length=10, null=True)),
                ('niveau', models.CharField(max_length=20, null=True)),
                ('age_developpe', models.CharField(max_length=10, null=True)),
                ('questionnaire', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.questionnaire')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.student')),
            ],
        ),
    ]
