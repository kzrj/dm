# -*- coding: utf-8 -*-
from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action

from feedbacks.models import Feedback, Like
from feedbacks.serializers import FeedbackSerializer, FeedbackEditSerializer
from feedbacks.filters import FeedbackFilter


class FeedbackViewSet(viewsets.ModelViewSet):
    queryset = Feedback.objects.all().select_related('profile')
    serializer_class = FeedbackSerializer
    filter_class = FeedbackFilter

    def create(self, request, serializer_class=FeedbackEditSerializer):
        serializer = FeedbackEditSerializer(data=request.data)
        if serializer.is_valid():
            profile = request.user.profile
            feedback = Feedback.objects.create_feedback(
                profile=profile,
                text=serializer.validated_data['text'],
                shop=serializer.validated_data.get('shop', None),
                rel_feedback=serializer.validated_data.get('rel_feedback', None),
                )
            return Response(
                {
                    "message": "Created.",
                    "feedback": FeedbackSerializer(feedback).data
                },
                status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        super().destroy(*args, **kwargs)
        return Response(serializer.data, status=status.HTTP_200_OK)