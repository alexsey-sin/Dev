from django.test import TestCase, Client
from django.contrib.auth.models import User
from posts.models import Group


class URLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Создадим запись в БД для проверки доступности адреса group/note/
        Group.objects.create(
            title='Заметки',
            slug='note',
            description='Небольшие заметки любого содержания',
        )

    def setUp(self):
        # Устанавливаем данные для тестирования
        # Создаём экземпляр клиента. Он не авторизован.
        self.guest_client = Client()
        # Создаем пользователя
        self.user = User.objects.create_user(username='BigBag')
        # Создаем второй клиент
        self.authorized_client = Client()
        # Авторизуем пользователя
        self.authorized_client.force_login(self.user)

    def test_homepage(self):
        """Страница / доступна любому пользователю."""
        response = self.guest_client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_group_page(self):
        """Страница /group/ доступна любому пользователю."""
        response = self.guest_client.get('/group/note/')
        self.assertEqual(response.status_code, 200)

    def test_new_post_page_guest(self):
        """Страница /new/ не доступна не авторизованному пользователю."""
        response = self.guest_client.get('/new/')
        self.assertRedirects(response, '/auth/login/?next=/new/')

    def test_new_post_page_auth(self):
        """Страница /new/ доступна авторизованному пользователю."""
        response = self.authorized_client.get('/new/')
        self.assertEqual(response.status_code, 200)

    def test_urls_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        # Шаблоны по адресам
        templates_url_names = {
            'index.html': '/',
            'group.html': '/group/note/',
            'new_post.html': '/new/',
        }
        for template, reverse_name in templates_url_names.items():
            with self.subTest():
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)
