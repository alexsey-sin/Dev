# Поля формы group и text проверены в методах теста модели
# и при генерации формы не переопределены
from django.test import TestCase, Client
from django.contrib.auth.models import User
from posts.models import Group, Post
from django.urls import reverse
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
import shutil
import tempfile


class PostCreateFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Создадим временную папку для медиа-файлов
        settings.MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)
        # Создадим запись в БД для проверки доступности адреса group/story/
        cls.group = Group.objects.create(
            title='Рассказ',
            slug='story',
            description='Рассказ любого содержания',
        )
        # Тестовая байт-последовательность картинки
        test_gif = (
            b'\x47\x49\x46\x38\x39\x61\x02\x00'
            b'\x01\x00\x80\x00\x00\x00\x00\x00'
            b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
            b'\x00\x00\x00\x2C\x00\x00\x00\x00'
            b'\x02\x00\x01\x00\x00\x02\x02\x0C'
            b'\x0A\x00\x3B'
        )
        cls.uploaded = SimpleUploadedFile(
            name='test.gif',
            content=test_gif,
            content_type='image/gif'
        )

    def setUp(self):
        # Создаем пользователя
        self.user = User.objects.create_user(username='BigBag')
        self.user.save()
        # Создаем клиента
        self.client = Client()
        # Авторизуем пользователя
        self.client.force_login(self.user)

    @classmethod
    def tearDownClass(cls):
        # Удаляем временную директорию и всё её содержимое
        shutil.rmtree(settings.MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()

    def test_create_post(self):
        """Валидная форма создает запись в Posts."""
        # Подготовим форму
        self.form_data = {
            'text': 'Тестовый текст',
            'group': self.group.id,
            'image': self.uploaded,
        }
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
        self.assertEqual(Post.objects.count(), posts_count + 1)
        # Проверяем, сработал ли редирект
        self.assertRedirects(response, reverse('index'))

    def test_update_post(self):
        """Автор может изменить запись в Posts."""
        # Создадим запись в БД
        post = Post.objects.create(
            text='Тестовый текст',
            author=self.user,
        )
        # Подсчитаем количество записей в Posts
        posts_count = Post.objects.count()
        new_text = 'Новый тестовый текст'
        url = reverse(
            'post_edit', args=[f'{self.user.username}', f'{post.id}'])
        # Отправляем POST-запрос
        self.client.get(url)
        self.client.post(url, data={'text': new_text})
        # Проверяем, не увеличилось ли число постов
        self.assertEqual(Post.objects.count(), posts_count)
        post = Post.objects.filter(author=self.user, text=new_text).first()
        self.assertIsNotNone(post)
