from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.utils.serializer_helpers import ReturnList
from common_config.message import *


class APIResponse(Response):
    """
    An HttpResponse that allows its data to be rendered into
    arbitrary media types.
    """

    def __init__(self, data=None, status=None,
                 template_name=None, headers=None,
                 exception=False, content_type=None,
                 custom_message=None):
        """
        Alters the init arguments slightly.
        For example, drop 'template_name', and instead use 'data'.
        Setting 'renderer' and 'media_type' will typically be deferred,
        For example being set automatically by the `APIView`.
        """
        super().__init__(None, status=status)

        if isinstance(data, Serializer):
            msg = (
                'You passed a Serializer instance as data, but '
                'probably meant to pass serialized `.data` or '
                '`.error`. representation.'
            )
            raise AssertionError(msg)

        self.data = data
        self.template_name = template_name
        self.exception = exception
        self.content_type = content_type
        self.status_code = status
        self.errors = None

        if isinstance(data, dict):
            self.errors = data.pop("errors", None)

        if headers:
            for name, value in headers.items():
                self[name] = value

        self.api_status = False
        self.message = "Failed"

        if self.status_code in [200, 201, 204, 208]:
            self.api_status = True
            if custom_message:
                self.message = custom_message
            else:
                self.message = "Success"
        elif "message" in self.data and self.status_code not in [200, 201, 208]:
            if isinstance(self.data, dict):
                if isinstance(self.data['message'], str) and "result" not in self.data:
                    self.data = {"message": self.data.values()}

        flag = False
        try:
            if self.data.get('custom_message'):
                self.message = self.data.pop('custom_message')
                flag = True
        except Exception as e:
            flag = False

        # validate self.data type is ReturnList object then removed blank set.
        if not flag and isinstance(self.data, ReturnList):
            error_list = []
            for error in self.data:
                if len(error) > 0 and self.status_code not in [200, 201, 208]:
                    error_list.append(error)

            if len(error_list) > 0:
                self.data = error_list
        if not flag:
            self.data = {
                'status': self.api_status,
                'code': self.status_code,
                'message': self.message,
                'data': self.data
            }
        else:
            self.data = {
                'status': self.api_status,
                'code': self.status_code,
                'message': self.message,
                'data': []
            }

        if self.errors is not None:
            if "message" in self.data:
                del self.data['message']

            self.data['errors'] = self.errors


class APIErrorResponse(Response):
    """
    An HttpResponse that allows its data to be rendered into
    arbitrary media types.
    """

    def get_error_message(self):
        if self.status_code == 400:
            return BAD_REQUEST
        elif self.status_code == 404:
            return RESOURCE_NOT_FOUND
        else:
            return UNEXPECTED_ERROR

    def __init__(self, message=None, data=None, status=None, custom_message=None):
        """
        Alters the init arguments slightly.
        For example, drop 'template_name', and instead use 'data'.
        Setting 'renderer' and 'media_type' will typically be deferred,
        For example being set automatically by the `APIView`.
        """
        super().__init__(None, status=status)

        if isinstance(data, Serializer):
            msg = (
                'You passed a Serializer instance as data, but '
                'probably meant to pass serialized `.data` or '
                '`.error`. representation.'
            )
            raise AssertionError(msg)

        if data is None:
            data = {}

        self.detail = data
        self.status_code = status
        if custom_message:
            self.message = custom_message
        else:
            self.message = "Failed"
        self.data = {
            'code': self.status_code,
            'message': self.message,
        }
