# -*- coding: utf-8 -*-
from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action

from feedbacks.models import Feedback, Like
from feedbacks.serializers import FeedbackSerializer


class FeedbackViewSet(viewsets.ModelViewSet):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer

    def create(self, request):
 		serializer = FeedbackSerializer(data=request.data)
        if serializer.is_valid():
        	profile = request.user.profile
            feedback = Feedback.objects.create_feedback(
            	profile=profile,
            	text=serializer.validated_data['text'],
            	shop=serializer.validated_data['shop'],
            	rel_feedback=serializer.validated_data['rel_feedback'],
            	)
            return Response(
                {
                    "message": "Created.",
                    "feedback": FeedbackSerializer(feedback).data
                },
                status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)