from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import pre_delete
from django.dispatch import receiver


class Video(models.Model):
    title = models.CharField(max_length=100)
    video_file = models.FileField(upload_to="videos/")
    upload_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.title)


@receiver(pre_delete, sender=Video)
def remove_video_file(**kwargs):
    instance = kwargs.get("instance")
    instance.video_file.delete(save=False)


class SubtitleLanguage(models.Model):
    code = models.CharField(max_length=5)
    name = models.CharField(max_length=20)

    def __str__(self):
        return str(self.name)


class Subtitle(models.Model):
    title = models.CharField(max_length=20)
    video = models.ForeignKey(
        Video, on_delete=models.CASCADE, related_name="video_subtitles"
    )
    language = models.ForeignKey(
        SubtitleLanguage, on_delete=models.CASCADE, related_name="language_subtitles"
    )
    subtitle_file = models.FileField(upload_to="subtitles/")

    def __str__(self):
        return str(self.title)


@receiver(pre_delete, sender=Subtitle)
def remove_subtitle_file(**kwargs):
    instance = kwargs.get("instance")
    instance.subtitle_file.delete(save=False)
