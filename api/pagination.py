from rest_framework.pagination import PageNumberPagination

class CustomPagination(PageNumberPagination):
    def get_paginated_response(self, data, extra_data):
        response = super().get_paginated_response(data)
        response.data.update(extra_data)
        return response
