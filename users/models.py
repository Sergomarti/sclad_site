import string
import random
import hashlib
import base64
import datetime

from django.db import models
from django.core.signing import TimestampSigner
from django.core.mail import send_mail
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from PIL import Image

HOST = 'http://127.0.0.1:8000'


class TypeOfGoods(models.Model):
    type_of_goods = models.CharField(max_length=25)

    def __str__(self):
        return self.type_of_goods


class User(AbstractUser):
    TOKEN_ALPHABET = (string.ascii_letters + string.digits) * 10
    TOKEN_LENGTH = 256

    signer = TimestampSigner()

    type_of_goods = models.ForeignKey(TypeOfGoods, on_delete=models.CASCADE, null=True)
    is_client = models.BooleanField(default=False)
    is_employee = models.BooleanField(default=False)

    telephone = models.CharField(
        max_length=13,
        null=True,
        default="00000000000"
    )
    is_email_verified = models.BooleanField(default=False)
    secret_email_token = models.CharField(max_length=TOKEN_LENGTH)
    verification_email_sent_at = models.DateTimeField(null=True)

    def get_secret_token(self):
        return "".join(
            random.sample(self.TOKEN_ALPHABET, self.TOKEN_LENGTH)
        )

    def digest_token(self, token):
        return hashlib.md5(
            token.encode('utf-8')
        ).hexdigest()

    def sign_token(self, token):
        return self.signer.sign(token)

    def unsign_token(self, token):
        return self.signer.unsign(token, max_age=datetime.timedelta(hours=2))

    def convert_token(self, token):
        return base64.b64encode(token.encode('utf-8')).decode('utf-8')

    def make_verify_link(self, token):
        return f"{HOST}/verify/?token={token}"

    def deconvert_token(self, token):
        return base64.b64decode(token.encode('utf-8')).decode('utf-8')

    def is_token_correct(self, token):
        deconverted = self.deconvert_token(token)
        unsigned = self.unsign_token(deconverted)
        return unsigned == self.digest_token(self.secret_email_token)

    def verify_email(self):
        self.is_email_verified = True
        self.save()

    def send_verification_email(self):
        token = self.get_secret_token()
        self.secret_email_token = token
        self.verification_email_sent_at = timezone.now()
        self.save()

        digested_token = self.digest_token(token)
        signed = self.sign_token(digested_token)
        converted = self.convert_token(signed)
        link = self.make_verify_link(converted)

        return send_mail(
            "Verify your email",
            f"Please follow this link: {link}",
            "sergeyhcwest16@gmail.com",
            [self.email]
        )


class Product(models.Model):
    brend = models.CharField(max_length=50)
    product = models.CharField(max_length=100)
    count = models.PositiveIntegerField(default=0)
    type_of_goods = models.ForeignKey(TypeOfGoods, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="images")

    def __str__(self):
        return f"{self.brend}, {self.product}"

    def save(self):
        super().save()
        img = Image.open(self.image.path)

        if img.height > 700 or img.width > 700:
            output_size = (700, 700)
            img.thumbnail(output_size)
            img.save(self.image.path)


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    count = models.PositiveIntegerField(default=0)
    date = models.DateField()
    comment = models.TextField()
    was_response = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.product} заказал {self.user} в количестве {self.count}"


class AdditionProduct(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    count = models.PositiveIntegerField(default=0)
    date = models.DateField()
    comment = models.TextField()
    was_response = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.product} принёс {self.user} в количестве {self.count}"


class OrderResponse(models.Model):
    response = models.CharField(max_length=20)

    def __str__(self):
        return self.response


class HistoryOrders(models.Model):
    addition = models.ForeignKey(AdditionProduct, blank=True, null=True, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, blank=True, null=True, on_delete=models.CASCADE)
    response = models.ForeignKey(OrderResponse, on_delete=models.CASCADE)
    comment = models.TextField()

    def __str__(self):
        return f"Заявка {self.order}{self.addition} {self.response}"
