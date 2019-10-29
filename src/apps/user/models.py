from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, BaseUserManager
from django.db import models
from visited_domains import settings
from django.utils.translation import ugettext_lazy as _


class UserManager(BaseUserManager):

    def create_user(self, email, username, password="password"):
        if self._exists_user(email):
            user = User.objects.get(email=email)
            return user
            # raise UserExists("Пользователь с такими данными уже есть в базе")
        user = self.model(email=email, username=username)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, username, password):
        user = self.model(email=email)
        user.username = username
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user

    def exists_user(self, email):
        return self._exists_user(email)

    @staticmethod
    def _exists_user(email):
        try:
            User.objects.get(email=email)
            return True
        except User.DoesNotExist as _:
            return False

    @staticmethod
    def get_all_users():
        users = []
        for user in User.objects.all():
            users.append({
                "username": user.username,
                "email": user.email,
                "date_joined": user.date_joined,
            })

        return users

    @staticmethod
    def update_user(validate_data):
        user = User.objects.get(email=validate_data['email'])
        user.username = validate_data['username']
        user.set_password(validate_data['username'])
        user.save()
        return user

    def update_user_user(self, email, username, password):
        user = self.model(email=email, username=username)
        user.set_password(password)
        try:
            user.save(force_insert=True)
        except:
            pass
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.CharField(_('E-mail'), max_length=255, unique=True, blank=False)
    username = models.CharField(_('Имя пользователя'), max_length=255, unique=False, blank=False)
    phone = models.CharField(_('Телефон'), max_length=16, blank=True)
    is_staff = models.BooleanField(_('Права на доступ в админ. панель'), default=False)
    is_superuser = models.BooleanField(_('Права суперпользователя'), default=False)
    date_joined = models.DateTimeField(_('Дата регистрации'), auto_now_add=True)
    active = models.BooleanField(_('Активный пользователь?'), default=False)
    activation_hash = models.CharField(_('Хеш пользователя'), max_length=40, blank=True)

    USERNAME_FIELD = 'email'

    objects = UserManager()

    REQUIRED_FIELDS = ["username"]

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    def __str__(self):
        return self.username

settings.AUTH_USER_MODEL = User


class UserExists(BaseException):
    pass


class UserLinks(models.Model):
    hash = models.CharField(_('Хеш'), max_length=32, unique=True, blank=False)
    date = models.DateTimeField(_('Дата обновления'), auto_now=True)
    user = models.ForeignKey(User, verbose_name="Пользователь", blank=False, null=False, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Хеш пользователя'
        verbose_name_plural = 'Хеши пользователей'
