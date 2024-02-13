from django.contrib import admin
from .models import Role, User, New, Picture, ViewCount
from .forms import RoleAdminForm, UserAdminForm, NewAdminForm, PictureAdminForm, ViewCountAdminForm
from django.contrib.auth.forms import AdminPasswordChangeForm


class RoleAdmin(admin.ModelAdmin):
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


class ViewCountAdmin(admin.ModelAdmin):
    form = ViewCountAdminForm


admin.site.register(ViewCount, ViewCountAdmin)