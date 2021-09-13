from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from posts.models import Follow, Post

User = get_user_model()


class PostPagesTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='StasZatushevskii')
        cls.author = User.objects.create_user(username='author')
        cls.post = Post.objects.create(
            author=cls.author,
            text='тестовый текст',
        )
        # Создаем авторизованный клиент
        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.user)

    def test_subscribe(self):
        follow_count = Follow.objects.filter(author=self.author).count()
        # Создаём подпищника
        self.authorized_client.get(
            reverse('posts:profile_follow', kwargs={
                'username': self.post.author.username}),
            follow=True
        )
        # проверяем
        self.assertEqual(
            Follow.objects.filter(author=self.author).count(), follow_count + 1
        )

    def test_index_subscribe(self):
        response = (self.authorized_client.get(
            reverse('posts:follow_index')))
        response.context.get('page_obj')
        counted_posts = Follow.objects.filter(user=self.user).count()
        Follow.objects.create(user=self.user, author=self.author)
        response = (self.authorized_client.get(
            reverse('posts:follow_index')))

        response.context.get('page_obj')
        self.assertEqual(Follow.objects.filter(
            user=self.user).count(), counted_posts + 1)
