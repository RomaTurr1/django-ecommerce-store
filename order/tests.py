from decimal import Decimal
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.admin.sites import site
from main.models import Category, Product
from .models import Order, OrderItem
from .forms import OrderForm
from .admin import OrderAdmin


class OrderWorkflowTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(name="clothes", slug="clothes")
        self.product1 = Product.objects.create(
            category=self.category,
            name="Джинсы",
            slug="jeans",
            price=Decimal("12000.00"),
            available=True
        )
        self.product2 = Product.objects.create(
            category=self.category,
            name="Футболка",
            slug="tshirt",
            price=Decimal("3500.00"),
            available=True
        )

    def test_empty_cart_redirect(self):
        """Проверка: для пустой корзины оформление должно быть недоступно."""
        response = self.client.get(reverse('create_order'))
        self.assertEqual(response.status_code, 302)

    def test_order_page_displays_cart_summary(self):
        """Проверка: на странице оформления над формой выводятся названия товаров,
        количество, стоимость каждой позиции и общая сумма."""
        session = self.client.session
        session['cart'] = {str(self.product1.id): 2, str(self.product2.id): 1}
        session.save()

        response = self.client.get(reverse('create_order'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product1.name)
        self.assertContains(response, self.product2.name)
        self.assertContains(response, "27500.00") # 12000*2 + 3500*1 = 27500

    def test_create_order_1_pickup_with_comment_no_email(self):
        """Заказ 1: самовывоз, с комментарием, без почты, из 2 разных товаров."""
        session = self.client.session
        session['cart'] = {str(self.product1.id): 1, str(self.product2.id): 2}
        session.save()

        order_data = {
            'user_name': 'Иван Иванов',
            'phone_number': '+79991112233',
            'delivery_method': 'pickup',
            'address': '',
            'email': '',
            'comment': 'Пожалуйста, упакуйте в подарочный пакет',
        }

        response = self.client.post(reverse('create_order'), data=order_data)
        self.assertEqual(response.status_code, 302)

        # Проверка создания заказа
        order = Order.objects.filter(user_name='Иван Иванов').first()
        self.assertIsNotNone(order)
        self.assertEqual(order.delivery_method, 'pickup')
        self.assertEqual(order.status, 'new')
        self.assertEqual(order.email, '')
        self.assertEqual(order.comment, 'Пожалуйста, упакуйте в подарочный пакет')

        # Проверка позиций заказа
        items = order.items.all()
        self.assertEqual(items.count(), 2)

        # Проверка очистки корзины
        self.assertNotIn('cart', self.client.session)

    def test_create_order_2_delivery_no_comment_with_email(self):
        """Заказ 2: доставка, с почтой, без комментария."""
        session = self.client.session
        session['cart'] = {str(self.product1.id): 1}
        session.save()

        order_data = {
            'user_name': 'Анна Смирнова',
            'phone_number': '+79998887766',
            'delivery_method': 'delivery',
            'address': 'ул. Ленина, д. 10, кв. 25',
            'email': 'anna@example.com',
            'comment': '',
        }

        response = self.client.post(reverse('create_order'), data=order_data)
        self.assertEqual(response.status_code, 302)

        order = Order.objects.filter(user_name='Анна Смирнова').first()
        self.assertIsNotNone(order)
        self.assertEqual(order.delivery_method, 'delivery')
        self.assertEqual(order.email, 'anna@example.com')
        self.assertEqual(order.comment, '')
        self.assertEqual(order.status, 'new')

    def test_order_form_does_not_contain_status(self):
        """Проверка: статус заказа не должен присутствовать в форме покупателя."""
        form = OrderForm()
        self.assertNotIn('status', form.fields)

    def test_admin_configuration(self):
        """Проверка конфигурации административной панели."""
        admin_instance = OrderAdmin(Order, site)
        self.assertIn('id', admin_instance.list_display)
        self.assertIn('user_name', admin_instance.list_display)
        self.assertIn('phone_number', admin_instance.list_display)
        self.assertIn('delivery_method', admin_instance.list_display)
        self.assertIn('status', admin_instance.list_display)

        self.assertIn('delivery_method', admin_instance.list_filter)
        self.assertIn('status', admin_instance.list_filter)

        self.assertIn('user_name', admin_instance.search_fields)
        self.assertIn('phone_number', admin_instance.search_fields)

        self.assertIn('status', admin_instance.list_editable)
