from rest_framework.pagination import PageNumberPagination


class UserPagination(PageNumberPagination):
    """
    Custom pagination for User list view.
    """
    page_size = 10  # Number of records per page
    page_size_query_param = 'page_size'  # Allow client to override page size
    max_page_size = 100  # Maximum number of records per page
