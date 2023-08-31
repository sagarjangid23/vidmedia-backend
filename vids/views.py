from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from vids.models import Video, Subtitle, SubtitleLanguage
from vids.serializers import (
    VideoSerializer,
    SubtitleSerializer,
    SubtitleLanguageSerializer,
)


class SubtitleLanguageListView(APIView):
    def get(self, request):
        languages = SubtitleLanguage.objects.all()
        serializer = SubtitleLanguageSerializer(languages, many=True)
        return Response(
            {"success": True, "data": serializer.data}, status=status.HTTP_200_OK
        )


class VideoListCreateView(APIView):
    def get(self, request):
        videos = Video.objects.all()
        serializer = VideoSerializer(videos, many=True)
        return Response(
            {"success": True, "data": serializer.data}, status=status.HTTP_200_OK
        )

    def post(self, request):
        serializer = VideoSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                {"success": False, "data": {"message": serializer.errors}},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )

        serializer.save()

        return Response(
            {"success": True, "data": serializer.data}, status=status.HTTP_200_OK
        )


class VideoDeleteView(APIView):
    def delete(self, request, video_id):
        try:
            video = Video.objects.get(id=video_id)
        except Video.DoesNotExist:
            return Response({"success": False}, status=status.HTTP_404_NOT_FOUND)

        video.delete()

        return Response({"success": True}, status=status.HTTP_204_NO_CONTENT)


class SubtitleCreateView(APIView):
    def post(self, request):
        serializer = SubtitleSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                {"success": False, "data": {"message": serializer.errors}},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )

        serializer.save()

        return Response(
            {"success": True, "data": serializer.data}, status=status.HTTP_200_OK
        )


class SubtitleDeleteView(APIView):
    def delete(self, request, subtitle_id):
        try:
            subtitle = Subtitle.objects.get(id=subtitle_id)
        except Subtitle.DoesNotExist:
            return Response({"success": False}, status=status.HTTP_404_NOT_FOUND)

        subtitle.delete()

        return Response({"success": True}, status=status.HTTP_204_NO_CONTENT)
