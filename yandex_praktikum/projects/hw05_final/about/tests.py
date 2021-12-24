from django.test import TestCase, Client
from django.contrib.auth.models import User
from posts.models import Group, Post
from django.urls import reverse


class URLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Создадим запись в БД для проверки доступности адреса group/note/
        cls.group = Group.objects.create(
            title='Заметки',
            slug='note',
            description='Небольшие заметки любого содержания',
        )
        # Создадим клиентов и пользователей
        cls.guest_client = Client()
        cls.user = User.objects.create_user(username='BigBag')
        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.user)
        cls.user2 = User.objects.create_user(username='LittleBig')
        cls.authorized_client2 = Client()
        # Создадим тестовый пост
        cls.post = Post.objects.create(
            text='Тестовый текст',
            author=cls.user,
            group=cls.group,
        )

    def test_urls_guest(self):
        """Проверка доступности страниц не авторизованному пользователю."""
        templates_url_names = {
            reverse('about:author'): 200,
            reverse('about:tech'): 200,
        }
        for rev_name, answer in templates_url_names.items():
            with self.subTest():
                response = self.guest_client.get(rev_name)
                self.assertEqual(response.status_code, answer)

    def test_urls_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        # Шаблоны по адресам
        templates_url_names = {
            reverse('about:author'): 'about.html',
            reverse('about:tech'): 'tech.html',
        }
        for rev_name, template in templates_url_names.items():
            with self.subTest():
                response = self.authorized_client.get(rev_name)
                self.assertTemplateUsed(response, template)
