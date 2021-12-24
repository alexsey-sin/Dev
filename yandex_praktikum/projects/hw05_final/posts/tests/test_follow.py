from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from . import const
from posts.models import Post, Follow


class FollowTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Создадим клиентов и пользователей
        cls.guest_client = Client()
        cls.author = User.objects.create_user(username=const.AUTHOR_NAME)
        cls.user = User.objects.create_user(username=const.USER_NAME)
        cls.auth_client = Client()
        cls.auth_client.force_login(cls.user)
        cls.url = reverse('profile_follow', args=[f'{cls.author.username}'])

    def test_profile_follow_auth(self):
        """Проверка доступности подписки авторизованному пользователю."""
        # Подпишемся на автора
        follow_cnt = Follow.objects.count()
        response = self.auth_client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Follow.objects.count(), follow_cnt + 1)

    def test_profile_follow_auth_yes(self):
        """Проверка подписки авторизованного пользователя."""
        # Проверим что новая запись автора появится в ленте пользователя
        self.auth_client.get(self.url)
        response = self.auth_client.get(reverse('follow_index'))
        posts_cnt = len(response.context.get('page').object_list)
        Post.objects.create(
            text=const.T_TEXT,
            author=self.author,
        )
        response = self.auth_client.get(reverse('follow_index'))
        posts_cnt2 = len(response.context.get('page').object_list)
        self.assertEqual(posts_cnt2, posts_cnt + 1)

    def test_profile_unfollow_auth(self):
        """Проверка удаления подписки авторизованного пользователя."""
        self.auth_client.get(self.url)
        response = self.auth_client.get(reverse('follow_index'))
        posts_cnt = len(response.context.get('page').object_list)
        Post.objects.create(
            text=const.T_TEXT,
            author=self.author,
        )
        # Удалим свою подписку
        url = reverse('profile_unfollow', args=[f'{self.author.username}'])
        self.auth_client.get(url)
        # Проверим что новая запись автора исчезла из ленты пользователя
        response = self.auth_client.get(reverse('follow_index'))
        posts_cnt2 = len(response.context.get('page').object_list)
        self.assertEqual(posts_cnt2, posts_cnt)
