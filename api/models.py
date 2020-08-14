import uuid
from django.db import models
from django.core.validators import MaxValueValidator

from api.utils import short_uuid


class DDT(models.Model):
    operator = models.ForeignKey('User', on_delete=models.RESTRICT, verbose_name="Operatore")
    client = models.ForeignKey('Client', on_delete=models.RESTRICT, verbose_name="Cliente")
    date = models.DateField(verbose_name="Data")
    photo = models.ImageField(upload_to="uploads/", verbose_name="Foto DDT")

    class Meta:
        ordering = ["date"]
        verbose_name = "Documento di trasporto"
        verbose_name_plural = "Documenti di trasporto"

    def __str__(self):
        return f"{self.pk}-{self.client}-{self.date}"


class Pallet(models.Model):
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

    ddt = models.ForeignKey('DDT', on_delete=models.CASCADE, related_name='pallets')
    type = models.IntegerField(choices=KIND, verbose_name="tipo")
    received = models.PositiveSmallIntegerField(validators=[MaxValueValidator(99)], blank=True, verbose_name="Ricevuti")
    returned = models.PositiveSmallIntegerField(validators=[MaxValueValidator(99)], blank=True, verbose_name="Resi")
    moved = models.PositiveSmallIntegerField(validators=[MaxValueValidator(99)], blank=True, verbose_name="Spostati")

    class Meta:
        verbose_name = "Bancale"
        verbose_name_plural = "Bancali"
        unique_together = ['ddt', 'type']


class Client(models.Model):
    corporate_name = models.CharField(
        max_length=100, verbose_name="Ragione Sociale")

    def __str__(self):
        return self.corporate_name

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clienti"


class User(models.Model):
    KIND = [
        ('OP', 'Operatore'),
        ('RE', 'Responsabile')
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    otp = models.CharField(max_length=6, default=short_uuid, unique=True, editable=False)
    name = models.CharField(max_length=30, verbose_name="Nome")
    surname = models.CharField(max_length=30, verbose_name="Cognome")
    email = models.EmailField(verbose_name="Email")
    user_kind = models.CharField(choices=KIND, max_length=2, default='OP', verbose_name="Tipo di utente")

    def __str__(self):
        return f"{self.name} {self.surname}"

    class Meta:
        verbose_name = "Utente"
        verbose_name_plural = "Utenti"
