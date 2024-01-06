from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import UserManager, PermissionsMixin
from django.utils import timezone
import uuid

class UserManager(UserManager):

    def _create_user(self, email, password, **extra_fields):

        email = self.normalize_email(email)
#        GlobalUserModel = apps.get_model(
#            self.model._meta.app_label, self.model._meta.object_name
#        )
        user = self.model(email=email, **extra_fields)
#        user.password = make_password(password)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)
    
    def __str__(self):
        return self.name


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField("メールアドレス", unique=True)
    first_name = models.CharField("姓", max_length=30)
    last_name = models.CharField("名", max_length=30)
    department = models.CharField("所属", max_length=50)
    created = models.DateTimeField("登録日", default=timezone.now)
    is_staff = models.BooleanField(
        ("staff status"),
        default=False,
        help_text=("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        ("active"),
        default=True,
        help_text=(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )

    objects = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = ("user")
        verbose_name_plural = ("users")

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def __str__(self):
        return self.name
    

class SupportUser(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField('姓', max_length=30)
    last_name = models.CharField('名' ,max_length=30)
    first_kana = models.CharField('姓カナ', max_length=30)
    last_kana = models.CharField('名カナ', max_length=30)
    post_code = models.IntegerField('郵便番号', blank=True, null=True)
    state = models.CharField('都道府県',max_length=6, blank=True, null=True)
    city = models.CharField('市区町村', max_length=10, blank=True, null=True)
    city_block = models.CharField('丁目、番号', max_length=30, blank=True, null=True)
    apartments = models.CharField('マンション名、部屋番号', max_length=30, blank=True, null=True)
    email = models.EmailField('メールアドレス', max_length=30, blank=True, null=True)
    phone = models.IntegerField('電話番号', blank=True, null=True)
    donation = models.IntegerField('賛助額', blank=True, null=True)
    payment = models.CharField('支払方法', max_length=30, blank=True, null=True)    
    is_confirmed = models.BooleanField('支払確認', default=False)
    created = models.DateTimeField("登録日", default=timezone.now, blank=True, null=True)
    shipping = models.DateTimeField('発送確認', blank=True, null=True)

    def __str__(self):
        return self.name
        

from django.utils.crypto import get_random_string

def create_id():
    return get_random_string(22)

class Item(models.Model):
    id = models.CharField(default=create_id, primary_key=True,
                        max_length=22, editable=False)
    name = models.CharField(default='', max_length=50)
    price = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name
