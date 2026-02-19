from rest_framework.test import APITestCase
from django.urls import reverse
from accounts.models import Business, Role, User
from products.models import Product


class ProductWorkflowTest(APITestCase):

    def setUp(self):
        self.business = Business.objects.create(name="TestBiz")

        self.role = Role.objects.create(
            name="ADMIN",
            business=self.business,
            can_create_product=True,
            can_edit_product=True,
            can_delete_product=True,
            can_approve_product=True
        )

        self.user = User.objects.create_user(
            username="admin",
            password="password",
            business=self.business,
            role=self.role
        )

        self.client.force_authenticate(user=self.user)

    def test_create_product(self):
        response = self.client.post("/api/products/", {
            "name": "Phone",
            "description": "Smartphone",
            "price": 500
        })

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Product.objects.count(), 1)

    def test_approve_product(self):
        product = Product.objects.create(
            name="TV",
            description="Smart TV",
            price=1000,
            business=self.business,
            created_by=self.user
        )

         # Use reverse with router name
        url = reverse('products-approve', args=[product.id])
        response = self.client.post(url)

        self.assertEqual(response.status_code, 400)  # because product not PENDING
