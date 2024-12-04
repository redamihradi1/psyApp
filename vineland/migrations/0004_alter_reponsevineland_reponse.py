# Generated by Django 5.1.2 on 2024-12-03 07:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vineland', '0003_alter_reponsevineland_reponse'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reponsevineland',
            name='reponse',
            field=models.CharField(blank=True, choices=[('0', '0'), ('1', '1'), ('2', '2'), ('NSP', 'Ne sais pas'), ('NA', 'Non applicable'), ('?', '?'), ('', 'Non répondu')], max_length=3, null=True, verbose_name='Réponse'),
        ),
    ]
