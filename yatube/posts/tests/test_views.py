from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from posts.models import Group, Post

User = get_user_model()


class PostPagesTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='тестовое название',
            slug='test-slug',
            description='Тестовое описание',
        )

    def setUp(self):
        # Создаем авторизованный клиент
        self.user = User.objects.create_user(username='StasZatushevskii')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        self.post = Post.objects.create(
            author=self.author,
            text='тестовый текст',
        )
        self.form_data = {
            'group': self.group.id,
            'text': 'Тестовый текст',
        }

    def test_pages_uses_correct_template(self):
        """имя_html_шаблона: reverse(name)"""
        templates_pages_names = {
            'posts/index.html': reverse('posts:index'),
            'posts/group_list.html': reverse(
                'posts:group_posts', kwargs={'slug': f'{self.group.slug}'}),
            'posts/profile.html': reverse(
                'posts:profile', kwargs={'username': self.user.username}),
            'posts/post_detail.html': reverse(
                'posts:post_detail', kwargs={'post_id': self.post.id}),
            'posts/create_post.html': reverse('posts:post_create'),
        }

        for template, reverse_name in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_post_list_page_show_correct_context(self):
        """Шаблон post_list сформирован с правильным контекстом."""
        response = (self.authorized_client.get(
            reverse('posts:group_posts', kwargs={
                'slug': f'{self.group.slug}'})))
        self.assertEqual(
            response.context.get('group').title, f'{self.group.title}')
        self.assertEqual(
            response.context.get('group').slug, f'{self.group.slug}')
        self.assertEqual(
            response.context.get(
                'group').description, f'{self.group.description}')

    def test_post_show_coreect_index(self):
        """на главной странице сайта"""
        response = (self.authorized_client.get(
            reverse('posts:index')))
        response.context.get('page_obj')
        counted_posts = len(response.context['page_obj'])
        response = self.authorized_client.post(
            reverse('posts:post_create'),
            data=self.form_data,
            follow=True
        )
        response = (self.authorized_client.get(
            reverse('posts:index')))
        response.context.get('page_obj')

        self.assertEqual(len(response.context['page_obj']), counted_posts + 1)

    def test_post_show_coreect_selected_group(self):
        """на странице выбранной группы"""
        response = (self.authorized_client.get(
            reverse('posts:group_posts', kwargs={
                'slug': f'{self.group.slug}'})))
        response.context.get('page_obj')
        counted_posts = len(response.context['page_obj'])
        response = self.authorized_client.post(
            reverse('posts:post_create'),
            data=self.form_data,
            follow=True
        )
        response = (self.authorized_client.get(
            reverse('posts:index')))
        response.context.get('page_obj')

        self.assertEqual(len(response.context['page_obj']), counted_posts + 1)

    def test_post_show_coreect_profile(self):
        """в профайле пользователя"""
        response = (self.authorized_client.get(
            reverse('posts:profile', kwargs={'username': self.user.username})))
        response.context.get('page_obj')
        counted_posts = len(response.context['page_obj'])
        response = self.authorized_client.post(
            reverse('posts:post_create'),
            data=self.form_data,
            follow=True
        )
        response = (self.authorized_client.get(
            reverse('posts:profile', kwargs={'username': self.user.username})))
        response.context.get('page_obj')

        self.assertEqual(len(response.context['page_obj']), counted_posts + 1)
