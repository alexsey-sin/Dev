from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from . import const

from posts.models import Group, Post


class URLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Создадим запись в БД для проверки доступности адреса group/note/
        cls.group = Group.objects.create(**const.GROUP_NOTE)
        # Создадим клиентов и пользователей
        cls.guest_client = Client()
        cls.user = User.objects.create_user(username=const.USER_NAME)
        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.user)
        cls.user2 = User.objects.create_user(username=const.USER_NAME2)
        cls.authorized_client2 = Client()
        # Создадим тестовый пост
        cls.post = Post.objects.create(
            text=const.T_TEXT,
            author=cls.user,
            group=cls.group,
        )
        cls.url_names = [
            reverse('index'),
            reverse('group', kwargs={'slug': f'{cls.group.slug}'}),
            reverse('new_post'),
            reverse('profile', args=[f'{cls.user.username}']),
            reverse('post', args=[f'{cls.user.username}', f'{cls.post.id}']),
            reverse('post_edit', args=[f'{cls.user.username}',
                                       f'{cls.post.id}']),
            reverse('group', kwargs={'slug': 'to_check_for_404'}),
            reverse('follow_index'),
            reverse('add_comment', args=[f'{cls.user.username}',
                                         f'{cls.post.id}']),
        ]

    def test_urls_guest(self):
        """Проверка доступности страниц не авторизованному пользователю."""
        answer = [200, 200, 302, 200, 200, 302, 404, 302, 302]
        url_answer = dict(zip(self.url_names, answer))
        for rev_name, answer in url_answer.items():
            with self.subTest(url=rev_name):
                response = self.guest_client.get(rev_name)
                self.assertEqual(response.status_code, answer)

    def test_urls_auth(self):
        """Проверка доступности страниц авторизованному пользователю."""
        answer = [200, 200, 200, 200, 200, 200, 404, 200, 200]
        url_answer = dict(zip(self.url_names, answer))
        for rev_name, answer in url_answer.items():
            with self.subTest(url=rev_name):
                response = self.authorized_client.get(rev_name)
                self.assertEqual(response.status_code, answer)

    def test_urls_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        template = ['index.html', 'group.html', 'new_post.html',
                    'profile.html', 'post.html', 'new_post.html']
        url_template = dict(zip(self.url_names, template))
        for rev_name, template in url_template.items():
            with self.subTest(url=rev_name):
                response = self.authorized_client.get(rev_name)
                self.assertTemplateUsed(response, template)

    def test_urls_auth_not_author(self):
        """Проверка доступности страницы /<username>/<post_id>/edit/
        авторизованному пользователю не автору поста."""
        self.authorized_client2.force_login(self.user2)
        response = self.authorized_client2.get(reverse(
            'post_edit', args=[f'{self.user.username}', f'{self.post.id}']))
        self.assertEqual(response.status_code, 302)

    def test_urls_redirect_guest(self):
        """Проверка редиректа со страниц не авторизованного пользователя."""
        # Шаблоны по адресам и редиректам
        url_names = {
            reverse('new_post'): '/auth/login/?next=/new/',
            reverse('post_edit', args=[f'{self.user.username}',
                    f'{self.post.id}']
                    ): (f'/auth/login/?next=/{self.user.username}'
                        f'/{self.post.id}/edit/'),
        }
        for rev_name, template in url_names.items():
            with self.subTest(url=rev_name):
                response = self.guest_client.get(rev_name)
                self.assertRedirects(response, template)
