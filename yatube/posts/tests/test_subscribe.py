from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from posts.models import Follow

User = get_user_model()


class PostPagesTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.author = User.objects.create_user(username='author')

    def setUp(self):
        # Создаем авторизованный клиент
        self.user = User.objects.create_user(username='StasZatushevskii')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_subscribe(self):
        follow_count = Follow.objects.filter(author=self.author).count()
        # Создаём подпищника
        Follow.objects.create(user=self.user, author=self.author)
        # проверяем
        self.assertEqual(
            Follow.objects.filter(author=self.author).count(), follow_count + 1
        )
