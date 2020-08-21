import uuid

from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.core.validators import MaxValueValidator
from django.db import models

from api.utils import short_uuid


class DDT(models.Model):
    serial = models.CharField(max_length=32, unique=True, verbose_name="Numero seriale")
    operator = models.ForeignKey('AppUser', on_delete=models.RESTRICT, verbose_name="Operatore")
    client = models.ForeignKey('Client', on_delete=models.RESTRICT, verbose_name="Cliente")
    date = models.DateField(verbose_name="Data")
    time = models.TimeField(auto_now_add=True, verbose_name="Orario creazione")
    photo = models.ImageField(upload_to="uploads/", verbose_name="Foto DDT")

    class Meta:
        ordering = ["-date"]
        verbose_name = "Documento di trasporto"
        verbose_name_plural = "Documenti di trasporto"

    def __str__(self):
        return self.serial.upper()


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
    kind = models.IntegerField(choices=KIND, verbose_name="tipo")
    received = models.PositiveSmallIntegerField(validators=[MaxValueValidator(99)], blank=True, verbose_name="Ricevuti")
    returned = models.PositiveSmallIntegerField(validators=[MaxValueValidator(99)], blank=True, verbose_name="Resi")
    moved = models.PositiveSmallIntegerField(validators=[MaxValueValidator(99)], blank=True, verbose_name="Spostati")

    class Meta:
        verbose_name = "Bancale"
        verbose_name_plural = "Bancali"
        unique_together = ['ddt', 'kind']


class Client(models.Model):
    corporate_name = models.CharField(max_length=100, verbose_name="Ragione Sociale")

    def __str__(self):
        return self.corporate_name

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clienti"


class AppUser(User):
    KIND = [
        ('OP', 'Operatore'),
        ('RE', 'Responsabile')
    ]

    otp = models.CharField(max_length=6, default=short_uuid, unique=True, editable=False)
    otp_used = models.BooleanField(default=False)
    user_kind = models.CharField(choices=KIND, max_length=2, default='OP', verbose_name="Mansione")

    def reset_otp(self):
        self.otp = short_uuid()
        self.otp_used = False
        self.save()
        self.send_otp_mail()

    def send_otp_mail(self):
        send_mail(
            "ElleEmmeDDT - OTP",
            f"Ciao {self.first_name} {self.last_name}!\nEcco la tua password di accesso alla piattaforma:\n{self.otp}",
            'no-reply@elleemmeddt.it',
            [self.email],
            fail_silently=False,
        )

    def save(self, *args, **kwargs):
        if not self.pk:
            # Set username to avoid conflicts
            self.username = uuid.uuid4()
            self.send_otp_mail()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = "Dipendente"
        verbose_name_plural = "Dipendenti"


class DataExport(models.Model):
    proxy = True

    class Meta:
        verbose_name = "Esportazione dati"
        verbose_name_plural = "Esportazione dati"
