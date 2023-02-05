from rest_framework import viewsets, mixins

class GenresCategoriesMixin(mixins.ListModelMixin,
                    mixins.DestroyModelMixin,
                    mixins.CreateModelMixin,
                    viewsets.GenericViewSet):
    pass