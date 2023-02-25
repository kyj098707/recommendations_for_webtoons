
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from recommendationapp.models import Member
 
class MemberAdmin(UserAdmin):
    # 관리자 화면에 보여질 칼럼 지정
    list_display = ('email','last_login','is_admin','is_staff')
    search_fields = ('email', 'username')
    readonly_fields = ('uid', 'last_login')
 
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
 
admin.site.register(Member, MemberAdmin)