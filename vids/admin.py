from django.contrib import admin
from .models import Video, Subtitle, SubtitleLanguage


admin.site.register(Video)
admin.site.register(Subtitle)
admin.site.register(SubtitleLanguage)
