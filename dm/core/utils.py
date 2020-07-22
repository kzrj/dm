# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import re

from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.exceptions import ValidationError as DRFValidationError

from rest_framework import status, exceptions
from rest_framework.views import exception_handler as drf_exception_handler
from rest_framework_jwt.settings import api_settings

from django.utils.encoding import force_text
from django.core.mail import send_mail
from django.db.utils import IntegrityError as DjangoIntegrityError


class CustomValidation(exceptions.APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Error'

    def __init__(self, detail, field, status_code):
        if status_code is not None:
            self.status_code = status_code
        if detail is not None:
            self.detail = {field: force_text(detail)}
        else: self.detail = {'detail': force_text(self.default_detail)}


'''' IMPORTANT: Note that the exception handler will only be called for responses generated by raised
 exceptions. It will not be used for any responses returned directly by the view, such as the 
 HTTP_400_BAD_REQUEST responses that are returned by the generic views when serializer validation 
 fails.
'''
def custom_exception_handler(exc, context):
    
    if isinstance(exc, CustomValidation):
        field = list(exc.detail.keys())[0]
        exc = DRFValidationError(detail={'message': field + ' ' + exc.detail[field]})

    if isinstance(exc, DjangoValidationError):
        if hasattr(exc, 'message_dict'):
            # TODO: handle many fields
            field = list(exc.detail.keys())[0]
            
            exc = DRFValidationError(detail={'message': field + ' ' + exc.detail[field]})
        else:
            exc = DRFValidationError(detail={'message': exc.message})

    if isinstance(exc, DjangoIntegrityError):
        exc = DRFValidationError(detail={'message': str(exc)})

    return drf_exception_handler(exc, context)


# def jwt_response_payload_handler(token, user=None, request=None):
#     return {
#         'token': token,
#         'user': WorkshopEmployeeSerializer(user.employee).data
#     }


def create_token(user):
    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

    payload = jwt_payload_handler(user)
    return jwt_encode_handler(payload)
