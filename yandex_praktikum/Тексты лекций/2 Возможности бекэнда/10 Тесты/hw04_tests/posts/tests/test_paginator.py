from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from posts.models import Group, Post

User = get_user_model()


class PostPagesTests(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Создаем авторизованный клиент
        user = User.objects.create_user(username='template_user')
        cls.client = Client()
        cls.client.force_login(user)
        # Создадим запись в БД для группы
        test_group = Group.objects.create(
            title='Рассказ',
            slug='story',
            description='Рассказ любого содержания',
        )
        # Создадим посты
        for _ in range(13):
            Post.objects.create(
                text='Тестовый текст',
                author=user,
                group=test_group,
            )

    def test_first_page_contains_ten_records(self):
        """Проверка: количество постов на первой странице равно 10."""
        response = self.client.get(reverse('index'))
        self.assertEqual(len(response.context.get('page').object_list), 10)

    def test_second_page_contains_three_records(self):
        """Проверка: на второй странице должно быть три поста."""
        response = self.client.get(reverse('index') + '?page=2')
        self.assertEqual(len(response.context.get('page').object_list), 3)
