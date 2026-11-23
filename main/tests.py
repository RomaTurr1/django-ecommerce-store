from decimal import Decimal
from django.test import TestCase, Client
from django.urls import reverse
from .models import Category, Product, Review
from .forms import ReviewForm


class ReviewFeatureTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(name="gadzhety", slug="gadzhety")
        self.product1 = Product.objects.create(
            category=self.category,
            name="Смартфон X",
            slug="smartfon-x",
            price=Decimal("50000.00"),
            available=True
        )
        self.product2 = Product.objects.create(
            category=self.category,
            name="Ноутбук Pro",
            slug="noutbuk-pro",
            price=Decimal("120000.00"),
            available=True
        )

    def test_empty_reviews_message(self):
        """Если список пуст, выводится сообщение 'У этого товара пока нет отзывов'."""
        url = reverse('product_detail', kwargs={'pk': self.product1.pk, 'slug': self.product1.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "У этого товара пока нет отзывов")

    def test_create_review_success_and_ordering(self):
        """Отправка отзыва: привязка к товару, редирект, отображение первым в списке и формат '4/5'."""
        url = reverse('product_detail', kwargs={'pk': self.product1.pk, 'slug': self.product1.slug})

        # Старый отзыв
        Review.objects.create(
            product=self.product1,
            author="Алексей",
            rating=5,
            text="Отличный телефон!"
        )

        # Отправляем новый отзыв
        response = self.client.post(url, data={
            'author': 'Мария',
            'rating': 4,
            'text': 'Хороший экран'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, url)

        # Проверяем страницу товара после редиректа
        follow_response = self.client.get(url)
        self.assertEqual(follow_response.status_code, 200)
        self.assertContains(follow_response, "Мария")
        self.assertContains(follow_response, "Хороший экран")
        self.assertContains(follow_response, "4/5")

        # Проверяем, что новый отзыв идет первым
        reviews = list(follow_response.context['reviews'])
        self.assertEqual(len(reviews), 2)
        self.assertEqual(reviews[0].text, "Хороший экран")
        self.assertEqual(reviews[0].author, "Мария")
        self.assertEqual(reviews[1].author, "Алексей")

    def test_reviews_isolation_between_products(self):
        """У каждого товара должны быть только его собственные отзывы."""
        Review.objects.create(
            product=self.product1,
            author="Пользователь 1",
            rating=5,
            text="Отзыв для товара 1"
        )
        Review.objects.create(
            product=self.product2,
            author="Пользователь 2",
            rating=3,
            text="Отзыв для товара 2"
        )

        url1 = reverse('product_detail', kwargs={'pk': self.product1.pk, 'slug': self.product1.slug})
        url2 = reverse('product_detail', kwargs={'pk': self.product2.pk, 'slug': self.product2.slug})

        response1 = self.client.get(url1)
        self.assertContains(response1, "Отзыв для товара 1")
        self.assertNotContains(response1, "Отзыв для товара 2")

        response2 = self.client.get(url2)
        self.assertContains(response2, "Отзыв для товара 2")
        self.assertNotContains(response2, "Отзыв для товара 1")

    def test_validation_empty_author_preserves_text(self):
        """При пустом имени форма не проходит валидацию, текст отзыва сохраняется."""
        url = reverse('product_detail', kwargs={'pk': self.product1.pk, 'slug': self.product1.slug})
        response = self.client.post(url, data={
            'author': '',
            'rating': 4,
            'text': 'Текст комментария без автора'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Текст комментария без автора')
        self.assertTrue(response.context['form'].errors)
        self.assertIn('author', response.context['form'].errors)
