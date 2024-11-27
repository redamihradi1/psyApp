# Generated by Django 5.1.2 on 2024-10-13 19:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Formulaire',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(default='', max_length=255, verbose_name='Titre du Formulaire')),
                ('description', models.TextField(default='', verbose_name='Description du Formulaire')),
            ],
        ),
        migrations.CreateModel(
            name='Parent',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('user_name', models.CharField(default='', max_length=255, verbose_name='Nom d’utilisateur')),
                ('name', models.CharField(default='', max_length=255, verbose_name='Nom du Parent')),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('num_question', models.AutoField(default='', primary_key=True, serialize=False, verbose_name='Numéro de la Question')),
                ('text', models.TextField(verbose_name='Texte de la Question')),
                ('can_ask', models.BooleanField(default=True, verbose_name='Est une Question ?')),
            ],
        ),
        migrations.CreateModel(
            name='Domain',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(default='', max_length=255, verbose_name='Nom du Domaine')),
                ('formulaire', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='domains', to='polls.formulaire', verbose_name='Formulaire')),
            ],
        ),
        migrations.CreateModel(
            name='Questionnaire',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Date de Création')),
                ('unique_key', models.CharField(default='', max_length=255, verbose_name='Clé Unique')),
                ('formulaire', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.formulaire', verbose_name='Formulaire')),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.parent', verbose_name='Parent')),
            ],
        ),
        migrations.CreateModel(
            name='DomaineResponse',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('score_total', models.IntegerField(default=0)),
                ('domaine', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.domain')),
                ('questionnaire', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='domaine_responses', to='polls.questionnaire')),
            ],
        ),
        migrations.CreateModel(
            name='Response',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('answer', models.IntegerField(choices=[(0, '0'), (1, '1'), (2, '2')], default=0)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.question')),
                ('questionnaire', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='responses', to='polls.questionnaire')),
            ],
        ),
        migrations.CreateModel(
            name='SousDomain',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(default='', max_length=255, verbose_name='Nom du Sous-Domaine')),
                ('domain', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='polls.domain', verbose_name='Domaine')),
            ],
        ),
        migrations.AddField(
            model_name='question',
            name='sous_domain',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='polls.sousdomain', verbose_name='Sous Domaine'),
        ),
        migrations.CreateModel(
            name='SousDomaineResponse',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('score_total', models.IntegerField(default=0)),
                ('questionnaire', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sous_domaine_responses', to='polls.questionnaire')),
                ('sous_domaine', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.sousdomain')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(default='', max_length=255, verbose_name='Nom de l’Élève')),
                ('age', models.IntegerField(default=1, verbose_name='Âge')),
                ('sexe', models.CharField(choices=[('M', 'Masculin'), ('F', 'Féminin')], default='M', max_length=1, verbose_name='Sexe')),
                ('date_of_birth', models.DateField(blank=True, null=True, verbose_name='Date de Naissance')),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='students', to='polls.parent')),
            ],
        ),
        migrations.AddField(
            model_name='questionnaire',
            name='student',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='polls.student', verbose_name='Élève'),
        ),
    ]
