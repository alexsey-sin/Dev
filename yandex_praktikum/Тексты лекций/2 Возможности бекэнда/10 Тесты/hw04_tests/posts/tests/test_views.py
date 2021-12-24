from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from posts.models import Group, Post
from django import forms
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
        cls.group_note = Group.objects.create(
            title='Рассказ',
            slug='story',
            description='Рассказ любого содержания',
        )
        # Создадим запись в БД для проверки доступности адреса group/note/
        cls.group_story = Group.objects.create(
            title='Заметки',
            slug='note',
            description='Небольшие заметки любого содержания',
        )
        # Создаем авторизованный клиент
        cls.user = User.objects.create_user(username='template_user')
        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.user)
        # Тестовая байт-последовательность картинки
        test_gif = (
            b'\x47\x49\x46\x38\x39\x61\x02\x00'
            b'\x01\x00\x80\x00\x00\x00\x00\x00'
            b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
            b'\x00\x00\x00\x2C\x00\x00\x00\x00'
            b'\x02\x00\x01\x00\x00\x02\x02\x0C'
            b'\x0A\x00\x3B'
        )
        uploaded = SimpleUploadedFile(
            name='test.gif',
            content=test_gif,
            content_type='image/gif'
        )
        # Создадим тестовый пост
        cls.post = Post.objects.create(
            text='Тестовый текст',
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
        self.assertEqual(post.text, 'Тестовый текст')
        self.assertIsNotNone(post.image)
        self.assertEqual(post.author, self.user)
        self.assertEqual(post.group, self.group_story)

    # Проверим словарь context страницы group
    # И созданный пост в этой группе
    def test_group_pages_show_correct_context(self):
        """Шаблон group сформирован с правильным контекстом."""
        response = self.authorized_client.get(
            reverse('group', kwargs={'slug': 'note'}))
        post = response.context['page'][0]
        group = response.context['group']
        self.assertEqual(group.title, 'Заметки')
        self.assertEqual(group.description, (
            'Небольшие заметки любого содержания'))
        self.assertEqual(post.text, 'Тестовый текст')
        self.assertIsNotNone(post.image)
        self.assertEqual(post.author, self.user)
        self.assertEqual(post.group, self.group_story)

    # Проверим словарь context страницы профайла
    def test_profile_pages_show_correct_context(self):
        """Шаблон profile сформирован с правильным контекстом."""
        response = self.authorized_client.get(
            reverse('profile', args=[f'{self.user.username}']))
        post = response.context['page'][0]
        self.assertEqual(post.text, 'Тестовый текст')
        self.assertIsNotNone(post.image)
        self.assertEqual(post.author, self.user)
        self.assertEqual(post.group, self.group_story)

    # Проверим словарь context страницы отдельного поста
    def test_post_pages_show_correct_context(self):
        """Шаблон post сформирован с правильным контекстом."""
        response = self.authorized_client.get(
            reverse('post', args=[f'{self.user.username}', f'{self.post.id}']))
        post = response.context['post']
        self.assertEqual(post.text, 'Тестовый текст')
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
