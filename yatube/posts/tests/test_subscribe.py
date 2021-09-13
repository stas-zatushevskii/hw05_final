from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from posts.models import Follow, Post


User = get_user_model()


class PostPagesTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.author = User.objects.create_user(username='author')
        cls.post = Post.objects.create(
            author=cls.user,
            text='тестовый текст',
        )

    def setUp(self):
        # Создаем авторизованный клиент
        self.user = User.objects.create_user(username='StasZatushevskii')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_subscribe(self):
        follow_count = Follow.objects.filter(author=self.post.author).count()
        # Создаём подпищника
        self.authorized_client.get(
            reverse('posts:profile_follow', kwargs={
                'username': self.author}),
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
        counted_posts = len(response.context['page_obj'])
        Follow.objects.create(user=self.user, author=self.author)
        response = (self.authorized_client.get(
            reverse('posts:follow_index')))

        response.context.get('page_obj')
        self.assertEqual(len(response.context['page_obj']), counted_posts + 1)
