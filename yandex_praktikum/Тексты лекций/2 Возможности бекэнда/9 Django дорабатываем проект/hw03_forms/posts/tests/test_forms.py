# Поля формы group и text проверены в методах теста модели
# и при генерации формы не переопределены
from django.test import TestCase, Client
from django.contrib.auth.models import User
from posts.models import Post
from django.urls import reverse


class PostCreateFormTests(TestCase):

    def setUp(self):
        # Создаем пользователя
        self.user = User.objects.create_user(username='BigBag')
        self.user.save()
        # Создаем клиента
        self.client = Client()
        # Авторизуем пользователя
        self.client.force_login(self.user)
        # Подготовим форму
        self.form_data = {
            'text': 'Тестовый текст',
            'author': self.user,
        }

    def test_create_post(self):
        """Валидная форма создает запись в Posts."""
        # Подсчитаем количество записей в Posts
        posts_count = Post.objects.count()
        # Отправляем POST-запрос
        response = self.client.post(
            reverse('new_post'),
            data=self.form_data,
            follow=True
        )
        # Проверим, не упало ли чего
        self.assertEqual(response.status_code, 200)
        # Проверяем, увеличилось ли число постов
        self.assertEqual(Post.objects.count(), posts_count+1)
        # Проверяем, сработал ли редирект
        self.assertRedirects(response, reverse('index'))
