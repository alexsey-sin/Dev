from django.test import TestCase
from posts.models import Group, Post
from django.contrib.auth.models import User
from . import const


class GroupModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Создаём тестовую запись в БД
        cls.group = Group.objects.create(**const.GROUP_MODEL)

    def test_verbose_name(self):
        """verbose_name в полях совпадает с ожидаемым."""
        for value, expected in const.FIELD_VERBOSE.items():
            with self.subTest(value=value):
                self.assertEqual(
                    self.group._meta.get_field(value).verbose_name, expected)

    def test_help_text(self):
        """help_text в полях совпадает с ожидаемым."""
        for value, expected in const.FIELD_HELP_TEXTS.items():
            with self.subTest(value=value):
                self.assertEqual(
                    self.group._meta.get_field(value).help_text, expected)

    def test_object_name_is_title_field(self):
        """В поле __str__  объекта group записано значение поля group.title."""
        expected_object_name = self.group.title
        self.assertEqual(expected_object_name, str(self.group))


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Создаем тестового пользователя
        cls.user = User(username=const.USER_NAME, password=const.T_PASSWORD)
        cls.user.save()
        cls.post = Post.objects.create(
            text=const.T_TEXT,
            author=cls.user,
        )

    def test_text_label(self):
        """verbose_name поля text совпадает с ожидаемым."""
        # Получаем из свойства класса Task значение verbose_name для text
        verbose = self.post._meta.get_field('text').verbose_name
        self.assertEquals(verbose, 'Текст')

    def test_text_help_text(self):
        """help_text поля text совпадает с ожидаемым."""
        # Получаем из свойства класса Task значение help_text для text
        help_text = self.post._meta.get_field('text').help_text
        self.assertEquals(help_text, 'Начните писать здесь')

    def test_object_name_is_title_field(self):
        """В поле __str__  объекта post записано значение поля post.title."""
        expected_object_name = self.post.text[:15]
        self.assertEqual(expected_object_name, str(self.post))
