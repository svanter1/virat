from django.urls import reverse, resolve
from django.test import TestCase
from .views import *
from .models import *


class HomeTests(TestCase):
    def test_home_view_status_code(self):
        url = reverse('home')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_home_url_resolves_home_view(self):
        view = resolve('/')
        self.assertEquals(view.func, home)


class PassengerTests(TestCase):
    def test_passenger_view_status_code(self):
        url = reverse('passenger')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_passenger_url_resolves_passenger_view(self):
        view = resolve('/passenger')
        self.assertEquals(view.func, passenger)


class PaymentTests(TestCase):
    def test_payment_view_status_code(self):
        url = reverse('newpay')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_payment_url_resolves_payment_view(self):
        view = resolve('/payment')
        self.assertEquals(view.func, newpay)


class PaymentSuccessTests(TestCase):
    def test_payment_success_view_status_code(self):
        url = reverse('paymentsuccess')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_payment_success_url_resolves_payment_success_view(self):
        view = resolve('/success')
        self.assertEquals(view.func, paymentsuccess)


class ReservationTests(TestCase):
    def test_reservation_view_status_code(self):
        url = reverse('reservation')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_reservation_url_resolves_reservation_view(self):
        view = resolve('/reservation')
        self.assertEquals(view.func, reservation)


class CancellationTests(TestCase):
    def test_cancellation_view_status_code(self):
        url = reverse('cancellation')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_reservation_url_resolves_reservation_view(self):
        view = resolve('/cancellation')
        self.assertEquals(view.func, cancellation)