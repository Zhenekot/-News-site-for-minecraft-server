from django.db import models
from django.db.models import Count
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.core.validators import (FileExtensionValidator, MinValueValidator,
                                    MaxValueValidator, MaxLengthValidator, MinLengthValidator, RegexValidator)
from decimal import Decimal
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from datetime import date
from django.contrib.auth.hashers import make_password, is_password_usable
from django.utils.translation import gettext_lazy as _
from django.utils.formats import date_format

class Role(models.Model):
    """
        Модель Role представляет роль пользователя в системе.

        Атрибуты:
        - title: Название роли. Должно быть уникальным и иметь длину не менее 3 символов.
        - is_archived: Булево значение, указывающее, архивирована ли роль.
                       По умолчанию установлено в 'False'.

        Методы:
        - delete: Переопределяет метод удаления для пометки объекта как архивированного, вместо его удаления из базы данных.
        - __str__: Возвращает строковое представление объекта, включая название роли и статус архивирования.

        Мета-класс:
        - verbose_name: Читаемое название модели в единственном числе.
        - verbose_name_plural: Читаемое название модели во множественном числе.
    """
    title = models.CharField(
        max_length=20,
        verbose_name=_("Название"),
        unique=True,
        validators=[
            MinLengthValidator(3, _("Название должно быть длиной не менее 3 символов"))
        ]
    )

    is_archived = models.BooleanField(default=False, verbose_name="Архивирован")

    def delete(self, *args, **kwargs):
        """ Переопределяет метод удаления, помечая объект как архивированный вместо удаления. """
        self.is_archived = True
        self.save()

    def __str__(self):
        """ Возвращает строковое представление объекта Role. """
        archived_status = " (Архивировано)" if self.is_archived else ""
        return f"{self.title}{archived_status}"

    class Meta:
        verbose_name = "Роль"
        verbose_name_plural = "Роли"


class UserManager(BaseUserManager):
    """
       Менеджер пользовательских моделей, предоставляющий методы для создания пользователей и суперпользователей.

       Методы:
       - create_user: Создает и возвращает пользователя с обычными правами доступа.
       - create_superuser: Создает и возвращает пользователя с правами суперпользователя.
    """
    def create_user(self, email, password=None, role=None, name=None,
                    date_of_birth=None, login=None):
        """
            Создает и возвращает пользователя с заданными email и паролем.
            Валидирует обязательные поля и устанавливает роль 'Клиент', если она не предоставлена.
        """
        if not email:
            raise ValueError('Введите Email')
        if password is None:
            raise ValueError('Введите пароль')
        if name is None:
            raise ValueError('Введите имя')
        if date_of_birth is None:
            raise ValueError('Введите паспортные данные')
        if login is None:
            raise ValueError('Введите логин')
        if role is None:
            user_role, created = Role.objects.get_or_create(title='Клиент')
            role = user_role
        user = self.model(
            email=self.normalize_email(email),
            password=password,
            role=role,
            name=name,
            date_of_birth=date_of_birth,
            login=login,

        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, role=None,  name=None,
                          date_of_birth=None, login=None):
        """
            Создает и возвращает суперпользователя с заданными email и паролем.
            Валидирует обязательные поля и устанавливает роль 'Администратор', если она не предоставлена.
        """
        if not email:
            raise ValueError('Введите Email')
        if password is None:
            raise ValueError('Введите пароль')

        if name is None:
            raise ValueError('Введите имя')

        if date_of_birth is None:
            raise ValueError('Введите паспортные данные')
        if login is None:
            raise ValueError('Введите логин')
        if role is None:
            user_role, created = Role.objects.get_or_create(title='Администратор')
            role = user_role
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            role=role,
            name=name,
            date_of_birth=date_of_birth,
            login=login,

        )
        user.is_staff = True
        user.is_superuser = True
        user.set_password(password)
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):

    rus_validator = RegexValidator(
        regex=r'[а-яА-Я]+',
        message=_("Имя/Фамилия/Отчество должны содержать кириллицу")
    )
    name = models.CharField(_('first name'), max_length=20, validators=[rus_validator])
    email = models.EmailField(_('email address'), max_length=50, unique=True)
    date_of_birth = models.DateField(_('Дата рождения'))
    role = models.ForeignKey('Role', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Роль')
    login = models.CharField(_('Логин'), max_length=25, unique=True)
    is_active = models.BooleanField(_('active'), default=True)
    is_staff = models.BooleanField(_('staff status'), default=False)
    password = models.CharField(max_length=300, verbose_name='Пароль')

    objects = UserManager()
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name=_('groups'),
        blank=True,
        help_text=_(
            'The groups this user belongs to. A user will get all permissions granted to each of their groups.'),
        related_name='custom_user_groups',
        related_query_name='user',
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name=_('user permissions'),
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name='custom_user_permissions',
        related_query_name='user',
    )
    USERNAME_FIELD = 'login'
    REQUIRED_FIELDS = ['name','date_of_birth', 'email']
    is_archived = models.BooleanField(default=False, verbose_name="Архивирован")

    def delete(self, *args, **kwargs):
        """ Переопределяет метод удаления, помечая пользователя как архивированного. """
        self.is_archived = True
        self.is_active = False
        self.save()

    class Meta:
        verbose_name = _('Пользователь')
        verbose_name_plural = _('Пользователи')

    def clean(self):
        """ Валидация полей модесвли перед сохранением. """
        if self.date_of_birth:
            today = date.today()
            age = today.year - self.date_of_birth.year - (
                        (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
            if age < 0 or age > 100:
                raise ValidationError({'date_of_birth': 'Возраст участника должен быть от 0 до 100 лет.'})

            if age < 16:
                raise ValidationError({
                    'date_of_birth': _('Пользователь должен быть старше 16 лет.')
                })


    def save(self, *args, **kwargs):
        """ Сохранение пользователя с полной валидацией и шифрованием пароля. """
        self.full_clean()
        if not self.pk:
            self.password = make_password(self.password)
        if self.role is None and not self.is_superuser:
            if self.pk:
                old_password = User.objects.get(pk=self.pk).password
                self.password = old_password
            user_role, created = Role.objects.get_or_create(title='Клиент')
            self.role = user_role
        if self.pk and not is_password_usable(self.password):
            self.password = make_password(self.password)

        if not self.is_archived and not self.is_active:
            self.is_active = True
        if self.is_archived and self.is_active:
            self.is_active = False

        super().save(*args, **kwargs)

    def __str__(self):
        """ Возвращает строковое представление объекта User. """
        archived_status = " (Архивировано)" if self.is_archived else ""
        return f"{self.name} {self.login} {archived_status}"


class New(models.Model):
    title = models.TextField(
        verbose_name=_('Название'),
        validators=[
            MinLengthValidator(1, _("Название не может быть пустым."))
        ]
    )
    description = models.TextField(
        verbose_name=_('Описание'),
        validators=[
            MinLengthValidator(1, _("Описание не может быть пустым."))
        ]
    )
    author = models.ForeignKey(
        'User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_('Автор')
    )
    date_of_create = models.DateTimeField(editable=False, null=True, blank=True, verbose_name='Дата создания новости')
    is_archived = models.BooleanField(default=False, verbose_name="Архивирован")

    def save(self, *args, **kwargs):
        if not self.date_of_create:
            self.date_of_create = timezone.localtime(timezone.now())

        super(New, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """ Переопределяет метод удаления, помечая объект как архивированный вместо удаления. """
        self.is_archived = True
        self.save()

    def __str__(self):
        """ Возвращает строковое представление объекта Hotel. """
        archived_status = " (Архивировано)" if self.is_archived else ""
        return f"{self.title}, Автор: {self.author}{archived_status}"

    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"

    def get_view_count(self):
        """
        Возвращает количество просмотров для данной статьи
        """
        return self.views.count()


class Picture(models.Model):
    path = models.FileField(upload_to='static/img/', verbose_name="Изображение", validators=[
        FileExtensionValidator(['jpg', 'jpeg', 'png'], 'Только изображения форматов jpg, jpeg, png допустимы.'),
    ])
    new = models.ForeignKey(
        'New',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_('Новость')
    )
    is_archived = models.BooleanField(default=False, verbose_name="Архивирован")
    def delete(self, *args, **kwargs):
        """ Переопределяет метод удаления, помечая объект как архивированный вместо удаления. """
        self.is_archived = True
        self.save()

    def __str__(self):
        """ Возвращает строковое представление объекта Tour. """
        archived_status = " (Архивировано)" if self.is_archived else ""
        return f"{self.id} {self.new} {archived_status}"

    class Meta:
        verbose_name = "Изображение"
        verbose_name_plural = "Изображения"


class ViewCount(models.Model):
    """
    Модель просмотров для статей
    """
    new = models.ForeignKey('New', on_delete=models.CASCADE, related_name='views')
    ip_address = models.GenericIPAddressField(verbose_name='IP адрес')
    viewed_on = models.DateTimeField(auto_now_add=True, verbose_name='Дата просмотра')

    class Meta:
        ordering = ('-viewed_on',)
        indexes = [models.Index(fields=['-viewed_on'])]
        verbose_name = 'Просмотр'
        verbose_name_plural = 'Просмотры'

    def __str__(self):
        return self.new.title