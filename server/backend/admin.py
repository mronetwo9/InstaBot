from django.contrib import admin


from backend.models import BotUser, Video, ViewVideo, Template, Post


@admin.register(BotUser)
class BotUserAdmin(admin.ModelAdmin):
    exclude = ['bot_state']
    search_fields = ['full_name', 'chat_id', 'username']
    list_display = ['id', 'full_name', 'username', 'chat_id', 'balance',
                    'invited', 'created']


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ['id', 'video', 'created']


@admin.register(ViewVideo)
class ViewVideoAdmin(admin.ModelAdmin):
    list_display = ['id', 'video', 'user', 'sended', 'received']


@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
    list_display = ['id', 'title_verbose_name', 'type']


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    exclude = ['schedule']
    list_display = ['id', 'title', 'period', 'repeats']
