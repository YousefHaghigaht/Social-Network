from django.contrib import admin
from .models import Post,Comment,Vote

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('user','slug')
    raw_id_fields = ('user',)
    prepopulated_fields = {'slug':('body',)}

admin.site.register(Comment)
admin.site.register(Vote)
