import uuid
from django.db import models
from django.core.validators import MaxValueValidator


class DDT(models.Model):
    client = models.ForeignKey('Client', on_delete=models.RESTRICT, verbose_name="Cliente")
    date = models.DateField(verbose_name="Data")
    photo = models.ImageField(upload_to="uploads/", verbose_name="Foto DDT")


class Container(models.Model):
    KIND = [
        (1, "EPAL"),
        (2, "Pallet grandi"),
        (3, "Pallet sdoppiato"),
        (4, "Carrelli grandi"),
        (5, "Carrelli piccoli"),
        (6, "Cestoni"),
        (7, "Casse Verdi"),
        (8, "Casse Grigie"),
        (9, "Presse")
    ]

    ddt = models.ForeignKey('DDT', on_delete=models.CASCADE)
    type = models.IntegerField(choices=KIND, verbose_name="tipo")
    count = models.PositiveSmallIntegerField(validators=[MaxValueValidator(99)], verbose_name="Quantità")


class Client(models.Model):
    corporate_name = models.CharField(max_length=100, verbose_name="Ragione Sociale")


class User(models.Model):
    KIND = [
        ('OP', 'Operatore'),
        ('RE', 'Responsabile')
    ]

    auth_id = models.UUIDField(default=uuid.uuid4, editable=False, verbose_name="Login ID")
    name = models.CharField(max_length=30, verbose_name="Nome")
    surname = models.CharField(max_length=30, verbose_name="Cognome")
    email = models.EmailField(verbose_name="Email")
    user_kind = models.CharField(choices=KIND, max_length=2, default='OP', verbose_name="Tipo di utente")