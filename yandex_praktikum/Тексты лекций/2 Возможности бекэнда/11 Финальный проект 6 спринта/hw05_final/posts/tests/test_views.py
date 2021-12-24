from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from posts.models import Group, Post
from django import forms
from . import const
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
import shutil
import tempfile

User = get_user_model()


class PostPagesTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Создадим временную папку для медиа-файлов
        settings.MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)
        # Создадим запись в БД для проверки доступности адреса group/story/
        cls.group_note = Group.objects.create(**const.GROUP_NOTE)
        # Создадим запись в БД для проверки доступности адреса group/note/
        cls.group_story = Group.objects.create(**const.GROUP_STORY)
        # Создаем авторизованный клиент
        cls.user = User.objects.create_user(username=const.USER_NAME)
        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.user)
        # Загрузим в память картинку
        uploaded = SimpleUploadedFile(**const.LOAD_FILE)
        # Создадим тестовый пост
        cls.post = Post.objects.create(
            text=const.T_TEXT,
            author=cls.user,
            group=cls.group_story,
            image=uploaded,
        )

    @classmethod
    def tearDownClass(cls):
        # Удаляем временную директорию и всё её содержимое
        shutil.rmtree(settings.MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()

    # Проверка используемых шаблонов выполнена в test_urls.py

    # Проверим словарь context главной страницы index
    # И здесь мы проверим, что созданный пост появился на главной странице
    def test_index_pages_show_correct_context(self):
        """Шаблон index сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse('index'))
        post = response.context['page'][0]
        self.assertEqual(post.text, const.T_TEXT)
        self.assertIsNotNone(post.image)
        self.assertEqual(post.author, self.user)
        self.assertEqual(post.group, self.group_story)
        self.assertEqual(post.image, f'posts/{const.LOAD_FILE["name"]}')

    # Проверим словарь context страницы group
    # И созданный пост в этой группе
    def test_group_pages_show_correct_context(self):
        """Шаблон group сформирован с правильным контекстом."""
        response = self.authorized_client.get(
            reverse('group', kwargs={'slug': 'note'}))
        post = response.context['page'][0]
        group = response.context['group']
        self.assertEqual(group.title, const.GROUP_STORY['title'])
        self.assertEqual(group.description, const.GROUP_STORY['description'])
        self.assertEqual(post.text, const.T_TEXT)
        self.assertIsNotNone(post.image)
        self.assertEqual(post.author, self.user)
        self.assertEqual(post.group, self.group_story)

    # Проверим словарь context страницы профайла
    def test_profile_pages_show_correct_context(self):
        """Шаблон profile сформирован с правильным контекстом."""
        response = self.authorized_client.get(
            reverse('profile', args=[f'{self.user.username}']))
        post = response.context['page'][0]
        self.assertEqual(post.text, const.T_TEXT)
        self.assertIsNotNone(post.image)
        self.assertEqual(post.author, self.user)
        self.assertEqual(post.group, self.group_story)

    # Проверим словарь context страницы отдельного поста
    def test_post_pages_show_correct_context(self):
        """Шаблон post сформирован с правильным контекстом."""
        response = self.authorized_client.get(
            reverse('post', args=[f'{self.user.username}', f'{self.post.id}']))
        post = response.context['post']
        self.assertEqual(post.text, const.T_TEXT)
        self.assertIsNotNone(post.image)
        self.assertEqual(post.author, self.user)
        self.assertEqual(post.group, self.group_story)

    # Проверим отсутствие созданного поста на страницы group другой группы
    def test_group_pages_not_show_new_post(self):
        """Шаблон group не содержит искомый контекст."""
        response = self.authorized_client.get(
            reverse('group', kwargs={'slug': 'story'}))
        self.assertTrue(self.group_note not in response.context['page'])

    # Проверим словарь context страницы new (в ней передаётся форма)
    def test_new_pages_show_correct_context(self):
        """Шаблон new_post сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse('new_post'))
        # Словарь ожидаемых типов полей формы:
        # указываем, объектами какого класса должны быть поля формы
        form_fields = {
            'group': forms.fields.ChoiceField,
            'text': forms.fields.CharField,
        }

        # Проверяем, что типы полей формы в словаре context
        # соответствуют ожиданиям
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context['form'].fields[value]
                # Проверяет, что поле формы является экземпляром
                # указанного класса
                self.assertIsInstance(form_field, expected)
