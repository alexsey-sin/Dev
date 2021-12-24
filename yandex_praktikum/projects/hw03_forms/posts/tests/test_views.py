from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from posts.models import Group, Post
from django import forms

User = get_user_model()


class PostPagesTests(TestCase):
    group_note = None
    group_story = None
    new_post = None

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
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

    def setUp(self):
        # Создаем авторизованный клиент
        self.user = User.objects.create_user(username='template_user')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        self.post = Post.objects.create(
            text='Тестовый текст',
            author=self.user,
            group=self.group_story,
        )

    # Проверяем используемые шаблоны
    def test_pages_use_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        # Собираем в словарь пары "имя_html_шаблона: name"
        templates_pages_names = {
            'index.html': reverse('index'),
            'group.html': reverse('group', kwargs={'slug': 'note'}),
            'new_post.html': reverse('new_post'),
        }
        # Проверяем, что при обращении к name вызывается
        # соответствующий HTML-шаблон
        for template, reverse_name in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    # Проверим словарь context главной страницы index
    # И здесь мы проверим, что созданный пост появился на главной странице
    def test_index_pages_show_correct_context(self):
        """Шаблон index сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse('index'))
        self.assertEqual(response.context['page'][0].text, 'Тестовый текст')
        self.assertEqual(response.context['page'][0].author, self.user)
        self.assertEqual(response.context['page'][0].group, self.group_story)

    # Проверим словарь context страницы group
    # И созданный пост в этой группе
    def test_group_pages_show_correct_context(self):
        """Шаблон group сформирован с правильным контекстом."""
        response = self.authorized_client.get(
            reverse('group', kwargs={'slug': 'note'}))
        self.assertEqual(response.context['group'].title, 'Заметки')
        self.assertEqual(response.context['group'].description, (
            'Небольшие заметки любого содержания'))
        self.assertEqual(response.context['posts'][0].text, 'Тестовый текст')
        self.assertEqual(response.context['posts'][0].author, self.user)
        self.assertEqual(response.context['posts'][0].group, self.group_story)

    # Проверим отсутствие на страницы group другой группы созданного поста
    def test_group_pages_not_show_new_post(self):
        """Шаблон group не содержит искомый контекст."""
        response = self.authorized_client.get(
            reverse('group', kwargs={'slug': 'story'}))
        self.assertTrue(self.new_post not in response.context['posts'])

    # Проверим словарь context страницы new (в ней передаётся форма)
    def test_new_pages_show_correct_context(self):
        """Шаблон new_post сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse('new_post'))
        # Словарь ожидаемых типов полей формы:
        # указываем, объектами какого класса должны быть поля формы
        form_fields = {
            'group': forms.fields.ChoiceField,
            # При создании формы поля модели типа TextField
            # преобразуются в CharField с виджетом forms.Textarea
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
