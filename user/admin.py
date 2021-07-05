from django.contrib.admin.sites import AdminSite
from django.contrib.auth.admin import UserAdmin
from django.conf import settings
from django.contrib import admin
from .models import MyUser

# Admin name -> http://localhost:8000/panel/admin
AdminSite.site_header = settings.SITE_HEADER
AdminSite.site_title = settings.SITE_TITLE
AdminSite.index_title = settings.INDEX_TITLE
AdminSite.site_url = settings.SITE_URL

# How user display on admin panel
@admin.register(MyUser)
class UserAdminConfig(UserAdmin, admin.ModelAdmin):
    list_display = ('email','username','first_name','last_name','is_active','is_staff','is_superuser')
    
    search_fields = ('email','first_name','last_name')
    
    list_filter = ('date_joined','is_active','is_staff','is_superuser')

    ordering = ('-date_joined',)

    list_editable = ('is_active','is_staff','is_superuser')

    list_per_page = 20

    list_display_links = ('email','username')

    # Display in admin
    fieldsets = (
        ('Personal', {'fields':('email','username','first_name','last_name','password')}),
        ('Permissions',{'fields':('is_active','is_staff','is_superuser')}),
        ('Group Permissions',{'fields':('groups',), 'classes': ('collapse',)}),
        ('info',{'fields':('date_joined','last_login')})
    )
    
    # Only read in admin
    readonly_fields = ('date_joined','last_login')

    # Adding in admin
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email','username','first_name','last_name','password1', 'password2','is_active','is_staff','is_superuser')}
        ),
        ('Group Permissions', {
            'classes': ('collapse',),
            'fields': ('groups',)}
        ),
    ) 