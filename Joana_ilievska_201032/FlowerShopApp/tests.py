from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.test import RequestFactory
from FlowerShopApp.models import Flower, Order
from FlowerShopApp.views import customer_registration_view
from FlowerShopApp.views import customer_login_view


class RegistrationAndLogInTestCase(TestCase):
    def test_customer_registration_view(self):
        # Создавање објект за POST барање со податоци за регистрација
        factory = RequestFactory()
        request = factory.post(reverse('registration'), {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpassword',
        })

        # Извршување на самата регистрација со повикување на соодветно view.
        response = customer_registration_view(request)

        # Проверка на статусниот код на одговорот и очекуваното однесување.
        self.assertEqual(response.status_code, 302)  # Очекувана редирекција кон 'login'

        # Проверка дали корисник со даденото корисничко име е создаден во Тест базата на податоци.
        self.assertTrue(User.objects.filter(username='testuser').exists())

    def test_customer_login_view_successful_login(self):
        # Создавање објект за POST барање со податоци за регистрација
        factory = RequestFactory()
        request = factory.post(reverse('login'), {
            'username': 'testuser',
            'password': 'testpassword',
        })

        # Повикување на соодветно view.
        response = customer_login_view(request)

        # Проверка на статусниот код на одговорот.
        self.assertEqual(response.status_code, 200)  # Кодот 200 сигнализира успешна најава


class ProductPageTestCase(TestCase):  # Се користи база на податоци која е различна од постоечката и има опција после секој
    #тест истата да се испразни.
    def setUp(self):
        Flower.objects.create(
            name="Rose",
            color="Red",
            price=100.0,
            quantity=100,
            photo="path/to/rose.jpg"
        )
        Flower.objects.create(
            name="Tulip",
            color="Yellow",
            price=80.0,
            quantity=50,
            photo="path/to/tulip.jpg"
        )
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

    def test_flower_creation(self):
        # Преземање на цветовите од тестната база на податоци
        roses = Flower.objects.filter(name="Rose")
        tulips = Flower.objects.filter(name="Tulip")

        # Потврда дека цветовите се креирани точно
        self.assertEqual(roses.count(), 1)
        self.assertEqual(tulips.count(), 1)

    def test_products_page(self):
        response = self.client.get('/products/')  # Навигација до стрната со продукти

        # Проверка на статусниот код на одговорот
        self.assertEqual(response.status_code, 200)

        # Проверуваме дали постојат продукти со помош на assertContains
        self.assertContains(response, "Додади во кошница", html=True)

    def test_adding_to_basket(self):
        # Креирање на инстанца за тестирање
        flower = Flower.objects.create(name="Test Flower", color="Red", price=10.0, quantity=5)

        # Земање на url адреса до страницата со продукти
        url = reverse('products')

        # Симулација на пост барање во формата за додавање на производ во кошница
        response = self.client.post(url, {'product_id': flower.id})

        # Проверка дали барањето е успешно и корисникот е пренасочен.
        self.assertEqual(response.status_code, 302)  # 302 е статусен код за пренасочување
        redirect_url = response.url
        expected_redirect_url = reverse('products')
        self.assertEqual(redirect_url, expected_redirect_url)


class BasketPageTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

    def test_viewing_basket_and_checking_total_price(self):
        # Креирање инстанца од продуктот да послужи за тестирање
        flower = Flower.objects.create(name="Test Flower", color="Red", price=100.0, quantity=5, photo='rose.jpg')

        # Го додаваме продуктот во кошницата на најавениот корисник
        order = Order.objects.create(user=self.user, flower=flower)
        basket_url = reverse('basket')

        # Симулираме посета на кошничката
        basket_response = self.client.get(basket_url)

        # Проверка на стаатусен код 200=OK
        self.assertEqual(basket_response.status_code, 200)
        print(basket_response.content.decode('utf-8'))
        #Проверка на логиката за вкупна цена која треба да ја плати соодветен корисник.
        expected_total_price_text = "Вкупно: 250.0   ден."
        self.assertContains(basket_response, expected_total_price_text)

    def test_placing_order(self):

        basket_url = reverse('basket')

        # Симулираме посета на кошничката
        basket_response = self.client.get(basket_url)
        self.assertEqual(basket_response.status_code, 200)

        pay_on_delivery_url = reverse('thankyou')  # Со клик на плати при достава се пренасочуваме кон "ThankYou"

        # Симулираме клик на линкот со follow=True за да го следиме пренасочувањето
        response = self.client.get(pay_on_delivery_url, follow=True)

        # Проверка дали корисникот е пренасочен на страницата "ThankYou"
        self.assertEqual(response.status_code, 200)

        # Проверка на специфичен содржински текст на страницата за благодарност.
        self.assertContains(response, "Ви благодариме за нарачката !")


