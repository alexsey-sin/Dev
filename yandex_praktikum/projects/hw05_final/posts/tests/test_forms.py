from django.contrib.auth import get_user_model
from django.test import Client, TestCase, override_settings
from django.urls import reverse
from posts.models import Group, Post
from . import const
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
import shutil
import tempfile

User = get_user_model()

# Создадим временную папку для медиа-файлов
TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class PostCreateFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Создадим запись в БД для группы
        cls.group = Group.objects.create(**const.GROUP_NOTE)
        # Создаем авторизованный клиент
        cls.user = User.objects.create_user(username=const.USER_NAME)
        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.user)

    @classmethod
    def tearDownClass(cls):
        # Удаляем временную директорию и всё её содержимое
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()

    def test_create_post(self):
        """Валидная форма создает запись в Posts."""
        # Подсчитаем количество записей в Posts
        posts_count = Post.objects.count()
        # Подготовим форму
        uploaded = SimpleUploadedFile(** const.LOAD_FILE2)
        data = {
            'text': const.T_TEXT,
            'group': self.group.id,
            'image': uploaded,
        }
        # Отправим
        response = self.authorized_client.post(
            reverse('new_post'),
            data=data,
            follow=True
        )
        # Проверим, не упало ли чего
        self.assertEqual(response.status_code, 200)
        # Проверяем, увеличилось ли число постов
        self.assertEqual(Post.objects.count(), posts_count + 1)
        # Проверяем, сработал ли редирект
        self.assertRedirects(response, reverse('index'))
        # Проверим что появился пост именно тот который создали
        self.assertTrue(
            Post.objects.filter(
                text=const.T_TEXT,
                group=self.group.id,
                image=f'posts/{const.LOAD_FILE2["name"]}'
            ).exists()
        )

    def test_create_post_invalid_content(self):
        """Форма c некорректным файлом не создается"""
        posts_count = Post.objects.count()
        uploaded = SimpleUploadedFile('test.txt', b'test')
        data = {
            'text': const.T_TEXT,
            'group': self.group.id,
            'image': uploaded,
        }
        response = self.authorized_client.post(
            reverse('new_post'),
            data=data,
            follow=True
        )
        # Проверим, не упало ли чего
        self.assertEqual(response.status_code, 200)
        # Проверяем, не увеличилось ли число постов
        self.assertEqual(Post.objects.count(), posts_count)
