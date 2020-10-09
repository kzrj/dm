# -*- coding: utf-8 -*-
from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action

from feedbacks.models import Feedback, Like
from feedbacks.serializers import FeedbackSerializer


class FeedbackViewSet(CoreViewSet, viewsets.ModelViewSet):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer