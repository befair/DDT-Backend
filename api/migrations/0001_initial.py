# Generated by Django 3.1 on 2020-08-18 13:15

import api.utils
import django.contrib.auth.models
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='AppUser',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='auth.user')),
                ('otp', models.CharField(default=api.utils.short_uuid, editable=False, max_length=6, unique=True)),
                ('otp_used', models.BooleanField(default=False)),
                ('user_kind', models.CharField(choices=[('OP', 'Operatore'), ('RE', 'Responsabile')], default='OP', max_length=2, verbose_name='Mansione')),
            ],
            options={
                'verbose_name': 'Dipendente',
                'verbose_name_plural': 'Dipendenti',
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('corporate_name', models.CharField(max_length=100, verbose_name='Ragione Sociale')),
            ],
            options={
                'verbose_name': 'Cliente',
                'verbose_name_plural': 'Clienti',
            },
        ),
        migrations.CreateModel(
            name='DDT',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('serial', models.CharField(max_length=32, unique=True, verbose_name='Numero seriale')),
                ('date', models.DateField(verbose_name='Data')),
                ('photo', models.ImageField(upload_to='uploads/', verbose_name='Foto DDT')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='api.client', verbose_name='Cliente')),
                ('operator', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='api.appuser', verbose_name='Operatore')),
            ],
            options={
                'verbose_name': 'Documento di trasporto',
                'verbose_name_plural': 'Documenti di trasporto',
                'ordering': ['-date'],
            },
        ),
        migrations.CreateModel(
            name='Pallet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.IntegerField(choices=[(1, 'EPAL'), (2, 'Pallet grandi'), (3, 'Pallet sdoppiato'), (4, 'Carrelli grandi'), (5, 'Carrelli piccoli'), (6, 'Cestoni'), (7, 'Casse Verdi'), (8, 'Casse Grigie'), (9, 'Presse')], verbose_name='tipo')),
                ('received', models.PositiveSmallIntegerField(blank=True, validators=[django.core.validators.MaxValueValidator(99)], verbose_name='Ricevuti')),
                ('returned', models.PositiveSmallIntegerField(blank=True, validators=[django.core.validators.MaxValueValidator(99)], verbose_name='Resi')),
                ('moved', models.PositiveSmallIntegerField(blank=True, validators=[django.core.validators.MaxValueValidator(99)], verbose_name='Spostati')),
                ('ddt', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pallets', to='api.ddt')),
            ],
            options={
                'verbose_name': 'Bancale',
                'verbose_name_plural': 'Bancali',
                'unique_together': {('ddt', 'type')},
            },
        ),
    ]
