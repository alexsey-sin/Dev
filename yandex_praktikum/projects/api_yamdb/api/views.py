from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, mixins, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.tokens import RefreshToken

from .filters import TitleFilter
from .models import User, Title, Category, Genre, Review, Comment
from .permissions import (IsAdminOrSuperUser, IsAdminOrDjangoAdminOrReadOnly,
                          IsModeratorOrAuthorOrReadOnly)
from .serializers import (ConfirmationSerializer, EmailSerializer,
                          UserSerializer, TitleSerializer,
                          TitleListSerializer, CategorySerializer,
                          GenreSerializer, ReviewSerializer,
                          CommentSerializer)


class ListCreateDestroyViewSet(
    mixins.ListModelMixin, mixins.CreateModelMixin,
    mixins.DestroyModelMixin, GenericViewSet
):
    pass


@api_view(['POST'])
@permission_classes([AllowAny])
def get_confirmation_code(request):
    serializer = EmailSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    email = serializer.data.get('email')
    user = User.objects.get_or_create(email=email, username=email)[0]
    confirmation_code = default_token_generator.make_token(user)
    mail_subject = 'Код подтверждения'
    message = f'Ваш код подтверждения: {confirmation_code}'
    send_mail(mail_subject, message, 'Yamdb', [email], fail_silently=False)

    return Response(f'На адрес {email} был выслан код подтверждения',
                    status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def get_jwt_token(request):
    serializer = ConfirmationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    email = serializer.data.get('email')
    confirmation_code = serializer.data.get('confirmation_code')
    user = get_object_or_404(User, email=email)

    if default_token_generator.check_token(user, confirmation_code):
        refresh = RefreshToken.for_user(user)
        return Response({
            'Your token': str(refresh.access_token)},
            status=status.HTTP_200_OK)

    return Response({'confirmation_code': 'Неверный код подтверждения'},
                    status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminOrSuperUser,)
    lookup_field = 'username'

    @action(methods=['PATCH', 'GET'], detail=False,
            permission_classes=(IsAuthenticated,))
    def me(self, request):
        serializer = UserSerializer(
            request.user, data=request.data, partial=True
        )
        role_old = request.user.role
        role_new = serializer.initial_data.get('role')
        # Здесь .get вернет None если роли нет
        # и первое условие проверки отработает
        if role_new and role_old != role_new and role_old != 'admin':
            return Response(status=status.HTTP_403_FORBIDDEN)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all().order_by('id')
    permission_classes = (IsAdminOrDjangoAdminOrReadOnly,)
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method in ['PATCH', 'POST']:
            return TitleListSerializer
        return TitleSerializer

    def perform_update(self, serializer):
        category_slug = self.request.data.get('category', None)
        genre_slug_list = self.request.data.getlist('genre', None)
        category = get_object_or_404(Category, slug=category_slug)
        genres = Genre.objects.filter(slug__in=genre_slug_list)
        serializer.save(genre=genres, category=category)


class CategoryViewSet(ListCreateDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrDjangoAdminOrReadOnly,)
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['name', ]
    lookup_field = 'slug'


class GenreViewSet(ListCreateDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrDjangoAdminOrReadOnly,)
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['name', ]
    lookup_field = 'slug'


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsModeratorOrAuthorOrReadOnly]

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs['title_id'])
        serializer.save(author=self.request.user, title=title)

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs['title_id'])
        return Review.objects.filter(title=title.id).order_by('id')


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsModeratorOrAuthorOrReadOnly]

    def perform_create(self, serializer):
        review = get_object_or_404(Review, id=self.kwargs['review_id'],
                                   title_id=self.kwargs['title_id'])
        serializer.save(author=self.request.user, review=review)

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs['review_id'],
                                   title_id=self.kwargs['title_id'])
        return Comment.objects.filter(review=review.id).order_by('id')
