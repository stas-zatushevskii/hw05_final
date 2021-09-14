import shutil
import tempfile

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db.models import Max
from django.test import Client, TestCase, override_settings
from django.urls import reverse
from posts.models import Group, Post

User = get_user_model()

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class PostCreateFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.post = Post.objects.create(
            author=cls.user,
            text='тестовая группа'
        )
        cls.group = Group.objects.create(title='Тестовая группа', slug='test')

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
        # Создаем неавторизованный клиент
        self.guest_client = Client()
        self.author_client = Client()
        self.authorized_client = Client()
        self.user = User.objects.create_user(username='StasZatushevskii')
        self.authorized_client.force_login(self.user)
        self.author_client.force_login(self.user)

    def test_create_post(self):
        post_count = Post.objects.count()

        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x02\x00'
            b'\x01\x00\x80\x00\x00\x00\x00\x00'
            b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
            b'\x00\x00\x00\x2C\x00\x00\x00\x00'
            b'\x02\x00\x01\x00\x00\x02\x02\x0C'
            b'\x0A\x00\x3B'
        )

        uploaded = SimpleUploadedFile(
            name='small.gif',
            content=small_gif,
            content_type='image/gif'
        )

        form_data = {
            'group': self.group.id,
            'text': 'Тестовый текст',
            'image': uploaded
        }
        response = self.authorized_client.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True
        )
        # прверка что после создания поста редирект прошёл
        self.assertRedirects(response, reverse(
            'posts:profile', kwargs={'username': self.user.username}))

        # прверка что пост создался
        self.assertEqual(Post.objects.count(), post_count + 1)

        # а существует ли он?
        last_post_id = Post.objects.aggregate(Max('pk'))['pk__max']
        self.assertTrue(Post.objects.filter(
            id=last_post_id,
            text=form_data['text'],
            group=form_data['group']).exists())

    def test_post_edit_(self):
        form_data_edit = {
            'group': self.group.id,
            'text': 'Тестовый отредоктированный текст'
        }

        response = self.author_client.post(
            reverse(
                'posts:post_edit',
                kwargs={'post_id': self.post.id}
            ), data=form_data_edit,
            follow=True
        )
        self.assertRedirects(response, reverse(
            'posts:post_detail', kwargs={'post_id': self.post.id})
        )
        # проверка что созданный пост != отредактированный пост
        self.post.refresh_from_db()
        self.assertNotEqual(self.post.text, form_data_edit['text'])
