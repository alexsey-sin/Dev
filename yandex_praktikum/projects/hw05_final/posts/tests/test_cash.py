from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from posts.models import Group, Post
from . import const


User = get_user_model()


class PostPagesTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Создаем авторизованный клиент
        cls.user = User.objects.create_user(username=const.USER_NAME)
        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.user)

    def test_cash_index_page(self):
        """Кэширование главной страницы."""
        posts_count = Post.objects.count()
        # Сделаем запрос к главной странице и запомним её контент
        context1 = self.authorized_client.get(reverse('index')).content

        # Создадим запись в БД для группы
        group_story = Group.objects.create(**const.GROUP_STORY)
        Post.objects.create(
            text=const.T_TEXT,
            author=self.user,
            group=group_story,
        )
        # Проверяем, число постов должно увеличиться
        self.assertEqual(Post.objects.count(), posts_count + 1)
        # Сделаем второй запрос к главной странице
        context2 = self.authorized_client.get(reverse('index')).content
        # Если кэш работает - контент обновится позднее
        self.assertEqual(context1, context2)
