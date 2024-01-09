from django import forms
from .models import Role, User, Picture, New
from django.contrib.auth.hashers import make_password, is_password_usable
class RoleAdminForm(forms.ModelForm):
    """
       Форма административного интерфейса для управления ролями пользователей.

       Мета-класс:
       - model: Модель, используемая для формы (Role).
       - fields: Включение всех полей модели в форму.

       Методы:
       - __init__: Инициализация формы с установкой плейсхолдеров для поля названия роли.
    """
    class Meta:
        model = Role
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        """
            Инициализация формы. Установка плейсхолдера для поля названия роли.
        """
        super(RoleAdminForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs['placeholder'] = 'Введите название роли'


class PictureAdminForm(forms.ModelForm):

    class Meta:
        model = Picture
        fields = '__all__'


class NewAdminForm(forms.ModelForm):
    """
       Форма административного интерфейса для управления ролями пользователей.

       Мета-класс:
       - model: Модель, используемая для формы (Role).
       - fields: Включение всех полей модели в форму.

       Методы:
       - __init__: Инициализация формы с установкой плейсхолдеров для поля названия роли.
    """

    class Meta:
        model = New
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        """
            Инициализация формы. Установка плейсхолдера для поля названия роли.
        """
        super(NewAdminForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs['placeholder'] = 'Введите название роли'
        self.fields['description'].widget.attrs['placeholder'] = 'Введите описание'


class UserAdminForm(forms.ModelForm):
    """
        Форма административного интерфейса для управления пользователями.

        Мета-класс:
        - model: Модель, используемая для формы (User).
        - fields: Включение всех полей модели в форму.

        Методы:
        - __init__: Инициализация формы с кастомными плейсхолдерами для полей.
        - save: Сохранение данных формы, включая хеширование пароля и установку роли, если она не задана.
    """
    class Meta:
        model = User
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        """
            Инициализация формы. Установка плейсхолдеров для различных полей и обязательности поля роли.
        """
        super(UserAdminForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['placeholder'] = 'Введите email'
        self.fields['name'].widget.attrs['placeholder'] = 'Введите имя'
        self.fields['login'].widget.attrs['placeholder'] = 'Введите логин'
        self.fields['password'].widget.attrs['placeholder'] = 'Введите пароль'
        self.fields['date_of_birth'].widget.attrs['placeholder'] = 'Введите дату рождения'
        self.fields['role'].required = True

    def save(self, commit=True):
        """
            Сохранение данных формы. Хеширование пароля и установка роли 'Клиент', если не указана.
        """
        user = super(UserAdminForm, self).save(commit=False)
        user.full_clean()
        if not user.pk:
            user.password = make_password(user.password)
        if user.role is None and not user.is_superuser:
            if user.pk:
                old_password = User.objects.get(pk=user.pk).password
                user.password = old_password
            user_role, created = Role.objects.get_or_create(title='Клиент')
            user.role = user_role
        if user.pk and is_password_usable(user.password):
            user.password = make_password(user.password)
        if commit:
            user.save()
        return user
