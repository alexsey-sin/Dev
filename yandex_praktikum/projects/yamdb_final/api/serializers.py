from django.db.models import Avg
from rest_framework import serializers

from api.models import Category, Comment, Genre, Review, Title, User


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)


class ConfirmationSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    confirmation_code = serializers.CharField(required=True)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'username', 'role', 'email',
                  'first_name', 'last_name', 'bio')
        model = User


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField('get_rating')
    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(many=False, read_only=True)

    def get_rating(self, obj):
        rating = Review.objects.filter(title_id=obj.pk).aggregate(
            rating=Avg('score')).get('rating')
        reviews_exists = Review.objects.exists()
        return None if not reviews_exists else rating

    class Meta:
        model = Title
        fields = '__all__'


class TitleListSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        many=True,
        slug_field='slug',
        queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        many=False,
        slug_field='slug',
        queryset=Category.objects.all()
    )

    class Meta:
        model = Title
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')

    def validate(self, data):
        user = self.context['request'].user
        title_id = self.context['view'].kwargs['title_id']
        method = self.context['request'].method
        if method == 'POST' and Review.objects.filter(
                title_id=title_id, author_id=user
        ).exists():
            raise serializers.ValidationError('Вы уже оставляли отзыв')
        return data

    def validate_score(self, value):
        if 1 <= value <= 10:
            return value
        raise serializers.ValidationError('Рейтинг должен быть от 1 до 10')


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
