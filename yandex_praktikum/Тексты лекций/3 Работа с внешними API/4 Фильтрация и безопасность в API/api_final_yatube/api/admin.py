from django.contrib import admin
from .models import Post, Group, Comment, Follow


class GroupAdmin(admin.ModelAdmin):
    list_display = ('title', 'description',)
    search_fields = ('title',)
    empty_value_display = '-пусто-'


class PostAdmin(admin.ModelAdmin):
    list_display = ('text', 'group', 'pub_date', 'author')
    search_fields = ('text',)
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'


class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'text', 'author', 'created',)
    search_fields = ('post',)
    empty_value_display = '-пусто-'


class FollowAdmin(admin.ModelAdmin):
    list_display = ('user', 'following',)
    search_fields = ('user', 'following',)
    empty_value_display = '-пусто-'


admin.site.register(Group, GroupAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Follow, FollowAdmin)
