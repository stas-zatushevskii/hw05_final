from django.urls import reverse
from django.conf import settings
from django.test import Client, TestCase
from django.urls import reverse
from posts.models import Post, Group, User
from django.core.cache import cache


class CacheContentTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.post = Post.objects.create(
            text='Тестовый текст',
            author=User.objects.create_user(username='test_user'),
            group=Group.objects.create(
                title='Тестовая группа',
                slug='test_slug',
                description='test description'
            )
        )

    def setUp(self):
        self.user = self.post.author
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_index_page_cached(self):
        # Проверка главной страницы
        response = self.authorized_client.get(reverse('posts:index'))
        first_render = response.content

        self.post.delete()

        response = self.authorized_client.get(reverse('posts:index'))
        self.assertEqual(first_render, response.content)

        cache.clear()

        response = self.authorized_client.get(reverse('posts:index'))
        self.assertNotEqual(first_render, response.content)
