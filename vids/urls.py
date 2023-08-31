from django.urls import path
from .views import (
    SubtitleLanguageListView,
    VideoListCreateView,
    VideoDeleteView,
    SubtitleCreateView,
    SubtitleDeleteView,
)

urlpatterns = [
    path("languages/", SubtitleLanguageListView.as_view(), name="language-list"),
    path("videos/", VideoListCreateView.as_view(), name="video-list-create"),
    path("videos/<video_id>/", VideoDeleteView.as_view(), name="video-delete"),
    path("subtitles/", SubtitleCreateView.as_view(), name="subtitle-create"),
    path(
        "subtitles/<subtitle_id>/", SubtitleDeleteView.as_view(), name="subtitle-delete"
    ),
]
