# Generated by Django 3.1 on 2020-08-07 18:37

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('corporate_name', models.CharField(max_length=100, verbose_name='Ragione Sociale')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('auth_id', models.UUIDField(default=uuid.uuid4, editable=False, verbose_name='Login ID')),
                ('name', models.CharField(max_length=30, verbose_name='Nome')),
                ('surname', models.CharField(max_length=30, verbose_name='Cognome')),
                ('email', models.EmailField(max_length=254, verbose_name='Email')),
                ('user_kind', models.CharField(choices=[('OP', 'Operatore'), ('RE', 'Responsabile')], default='OP', max_length=2, verbose_name='Tipo di utente')),
            ],
        ),
        migrations.CreateModel(
            name='DDT',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='Data')),
                ('photo', models.ImageField(upload_to='uploads/', verbose_name='Foto DDT')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='api.client', verbose_name='Cliente')),
            ],
        ),
        migrations.CreateModel(
            name='Container',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.IntegerField(choices=[(1, 'EPAL'), (2, 'Pallet grandi'), (3, 'Pallet sdoppiato'), (4, 'Carrelli grandi'), (5, 'Carrelli piccoli'), (6, 'Cestoni'), (7, 'Casse Verdi'), (8, 'Casse Grigie'), (9, 'Presse')], verbose_name='tipo')),
                ('count', models.PositiveSmallIntegerField(validators=[django.core.validators.MaxValueValidator(99)], verbose_name='Quantità')),
                ('ddt', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.ddt')),
            ],
        ),
    ]