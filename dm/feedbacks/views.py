# -*- coding: utf-8 -*-
from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action

from feedbacks.models import Feedback, Like, Suggestion
from feedbacks.serializers import FeedbackSerializer, FeedbackEditSerializer, SuggestionSerializer
from feedbacks.filters import FeedbackFilter

from core.permissions import SuggestionPermission, OwnerCUDPermission


class FeedbackViewSet(viewsets.ModelViewSet):
    queryset = Feedback.objects.all().select_related('profile')
    serializer_class = FeedbackSerializer
    filter_class = FeedbackFilter
    # permission_classes = [OwnerCUDPermission, ]

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


class SuggestionViewSet(viewsets.ModelViewSet):
    queryset = Suggestion.objects.all()
    serializer_class = SuggestionSerializer
    permission_classes = [SuggestionPermission, ]

    def create(self, request):
        serializer = SuggestionSerializer(data=request.data)
        if serializer.is_valid():
            profile = None
            if hasattr(request.user, 'profile'):
                profile = request.user.profile

            Suggestion.objects.create(
                profile=profile,
                text=serializer.validated_data['text'],
                )
            return Response('Created', status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
