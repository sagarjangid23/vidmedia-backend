from rest_framework import serializers
from vids.models import Video, Subtitle, SubtitleLanguage
from django.conf import settings
from django.core.files.base import ContentFile


class SubtitleLanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubtitleLanguage
        fields = "__all__"


class VideoSerializer(serializers.ModelSerializer):
    subtitle_files = serializers.SerializerMethodField()

    class Meta:
        model = Video
        fields = ["id", "title", "upload_date", "video_file", "subtitle_files"]

    def get_subtitle_files(self, obj):
        subtitles = [
            {
                "id": subtitle.id,
                "language": subtitle.language.name,
                "link": subtitle.subtitle_file.url,
                "code": subtitle.language.code,
            }
            for subtitle in obj.video_subtitles.all()
        ]
        return subtitles

    def validate_video_file(self, video_file):
        if video_file.size > settings.MAX_UPLOAD_SIZE:
            raise serializers.ValidationError("File size exceeds the maximum limit.")

        if not video_file.content_type.startswith("video/"):
            raise serializers.ValidationError(
                "Invalid file type. Only video files are allowed."
            )
        return video_file


class SubtitleCreateSerilizer(serializers.Serializer):
    start_time = serializers.CharField(allow_blank=False)
    end_time = serializers.CharField(allow_blank=False)
    text = serializers.CharField(allow_blank=False)


class SubtitleSerializer(serializers.ModelSerializer):
    subtitles = SubtitleCreateSerilizer(write_only=True, many=True)
    file = serializers.SerializerMethodField()

    class Meta:
        model = Subtitle
        fields = ["id", "title", "video", "language", "subtitles", "file"]

    def validate(self, data):
        video = data["video"]
        language = data["language"]

        if Subtitle.objects.filter(video=video, language=language).exists():
            raise serializers.ValidationError(
                {
                    "language": [
                        f"{str(language).capitalize()} Subtitle already exist for this video"
                    ]
                }
            )

        return data

    def validate_subtitles(self, subtitles):
        if not subtitles:
            raise serializers.ValidationError(f"Atleast 1 subtitle required")

        sorted_subtitles = sorted(subtitles, key=lambda x: x["start_time"])
        prev_end_time = None

        for subtitle in sorted_subtitles:
            start_time = subtitle["start_time"]
            end_time = subtitle["end_time"]

            if start_time >= end_time:
                raise serializers.ValidationError("End time must be after start time")

            if prev_end_time and start_time < prev_end_time:
                raise serializers.ValidationError("Subtitle time ranges cannot overlap")

            prev_end_time = end_time
        return subtitles

    def get_file(self, obj):
        return obj.subtitle_file.url

    def create(self, validated_data):
        title = validated_data["title"]
        video = validated_data["video"]
        language = validated_data["language"]
        subtitles = validated_data.pop("subtitles")

        subtitle_entries = "\n".join(
            (
                f"{entry['start_time']} --> {entry['end_time']}\n{entry['text']}\n"
                for entry in sorted(
                    subtitles, key=lambda x: (x["start_time"], x["end_time"])
                )
            )
        )
        subtitle_entries = "WEBVTT\n\n" + subtitle_entries

        subtitle = Subtitle.objects.create(
            title=title,
            video=video,
            language=language,
            subtitle_file=ContentFile(
                subtitle_entries,
                f"{title}_{language.name}.vtt",
            ),
        )
        return subtitle
