from django.contrib import admin
from apps.usuario.models import Comment,SearchValues, Profile

admin.site.register(Comment)
admin.site.register(SearchValues)
admin.site.register(Profile)
