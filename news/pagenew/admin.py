from django.contrib import admin
from .models import Role, User, New, Picture
from .forms import RoleAdminForm,UserAdminForm, NewAdminForm, PictureAdminForm
from django.contrib.auth.forms import AdminPasswordChangeForm

class RoleAdmin(admin.ModelAdmin):
    """
        Класс RoleAdmin предназначен для настройки представления модели Role
        в административной панели.

        Атрибуты:
        - form: Класс формы для кастомизации отображения полей модели в админ-панели.
        - list_display: Список полей, которые будут отображаться в таблице списка объектов.
        - search_fields: Поля, по которым можно выполнять поиск объектов.
        - ordering: Порядок сортировки объектов в списке.
        - list_per_page: Количество объектов на странице.

        Методы:
        - delete_model: Переопределение метода при удалении одиночного объекта.
        - delete_queryset: Переопределение метода при удалении группы объектов.
    """
    form = RoleAdminForm
    list_display = ('title',)
    search_fields = ('title',)
    ordering = ('title',)
    list_per_page = 10

    def delete_model(self, request, obj):
        """ Переопределение метода удаления для одиночных объектов. """
        obj.delete()

    def delete_queryset(self, request, queryset):
        """ Переопределение метода удаления для группы объектов. """
        for obj in queryset:
            obj.delete()


admin.site.register(Role, RoleAdmin)


class UserAdmin(admin.ModelAdmin):
    """
       Класс UserAdmin предназначен для настройки представления модели User
       в административной панели.

       Атрибуты:
       - form: Класс формы для кастомизации отображения полей модели в админ-панели.
       - change_password_form: Форма для изменения пароля пользователя.
       - list_display: Список полей, которые будут отображаться в таблице списка объектов.
       - search_fields: Поля, по которым можно выполнять поиск объектов.
       - ordering: Порядок сортировки объектов в списке.
       - list_filter: Фильтры для упрощения поиска объектов по ключевым характеристикам.
       - list_per_page: Количество объектов на странице.

       Методы:
        - delete_model: Переопределение метода при удалении одиночного объекта.
        - delete_queryset: Переопределение метода при удалении группы объектов.
    """
    form = UserAdminForm
    change_password_form = AdminPasswordChangeForm
    list_display = ['name', 'email', 'login', 'role', 'is_archived']
    search_fields = ['name', 'email', 'login']
    ordering = ('name',)
    list_filter = ('role',)
    list_editable = ('is_archived',)
    list_per_page = 10

    def delete_model(self, request, obj):
        """ Переопределение метода удаления для одиночных объектов. """
        obj.delete()

    def delete_queryset(self, request, queryset):
        """ Переопределение метода удаления для группы объектов. """
        for obj in queryset:
            obj.delete()


admin.site.register(User, UserAdmin)


class NewAdmin(admin.ModelAdmin):
    """
       Класс UserAdmin предназначен для настройки представления модели User
       в административной панели.

       Атрибуты:
       - form: Класс формы для кастомизации отображения полей модели в админ-панели.
       - change_password_form: Форма для изменения пароля пользователя.
       - list_display: Список полей, которые будут отображаться в таблице списка объектов.
       - search_fields: Поля, по которым можно выполнять поиск объектов.
       - ordering: Порядок сортировки объектов в списке.
       - list_filter: Фильтры для упрощения поиска объектов по ключевым характеристикам.
       - list_per_page: Количество объектов на странице.

       Методы:
        - delete_model: Переопределение метода при удалении одиночного объекта.
        - delete_queryset: Переопределение метода при удалении группы объектов.
    """
    form = NewAdminForm
    list_display = ['id', 'title', 'author', 'date_of_create', 'is_archived']
    search_fields = ['title']
    list_filter = ('author',)
    list_editable = ('is_archived',)
    list_per_page = 10

    def delete_model(self, request, obj):
        """ Переопределение метода удаления для одиночных объектов. """
        obj.delete()

    def delete_queryset(self, request, queryset):
        """ Переопределение метода удаления для группы объектов. """
        for obj in queryset:
            obj.delete()


admin.site.register(New, NewAdmin)


class PictureAdmin(admin.ModelAdmin):
    """
       Класс UserAdmin предназначен для настройки представления модели User
       в административной панели.

       Атрибуты:
       - form: Класс формы для кастомизации отображения полей модели в админ-панели.
       - change_password_form: Форма для изменения пароля пользователя.
       - list_display: Список полей, которые будут отображаться в таблице списка объектов.
       - search_fields: Поля, по которым можно выполнять поиск объектов.
       - ordering: Порядок сортировки объектов в списке.
       - list_filter: Фильтры для упрощения поиска объектов по ключевым характеристикам.
       - list_per_page: Количество объектов на странице.

       Методы:
        - delete_model: Переопределение метода при удалении одиночного объекта.
        - delete_queryset: Переопределение метода при удалении группы объектов.
    """
    form = PictureAdminForm
    list_display = ['id', 'path', 'new', 'is_archived']
    search_fields = ['new']
    list_editable = ('is_archived',)
    list_per_page = 10

    def delete_model(self, request, obj):
        """ Переопределение метода удаления для одиночных объектов. """
        obj.delete()

    def delete_queryset(self, request, queryset):
        """ Переопределение метода удаления для группы объектов. """
        for obj in queryset:
            obj.delete()


admin.site.register(Picture, PictureAdmin)