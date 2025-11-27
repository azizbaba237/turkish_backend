# api/tests.py
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from .models import Product, Cart, CartItem

User = get_user_model()


class CartAPITestCase(TestCase):
    def setUp(self):
        """Initialisation avant chaque test"""
        self.client = APIClient()

        # Créer un utilisateur
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

        # Créer un deuxième utilisateur pour les tests d'isolation
        self.user2 = User.objects.create_user(
            username='testuser2',
            email='test2@example.com',
            password='testpass123'
        )

        # Créer des produits de test
        self.product1 = Product.objects.create(
            name='Test Product 1',
            price=100.00,
            description='Test description'
        )
        self.product2 = Product.objects.create(
            name='Test Product 2',
            price=200.00,
            description='Test description 2'
        )

        # Authentifier le client
        self.client.force_authenticate(user=self.user)

    def test_add_item_and_get_cart_persist_between_requests(self):
        """Test d'ajout d'item et persistance"""
        # Ajouter un item
        response = self.client.post('/api/cart/add/', {
            'product': self.product1.id,
            'quantity': 2,
            'color': 'red',
            'size': 'M'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()['items']), 1)

        # Vérifier la persistance
        resp = self.client.get('/api/cart/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp.json()['items']), 1)
        self.assertEqual(resp.json()['items'][0]['quantity'], 2)

    def test_cart_is_isolated_between_users(self):
        """Test d'isolation des paniers entre utilisateurs"""
        # User1 ajoute un produit
        self.client.post('/api/cart/add/', {
            'product': self.product1.id,
            'quantity': 1
        })

        # Vérifier le panier de user1
        resp = self.client.get('/api/cart/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp.json()['items']), 1)

        # Changer pour user2
        self.client.force_authenticate(user=self.user2)

        # Le panier de user2 doit être vide
        resp = self.client.get('/api/cart/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp.json()['items']), 0)

    def test_update_and_remove_item(self):
        """Test de mise à jour et suppression d'item"""
        # Ajouter un item
        response = self.client.post('/api/cart/add/', {
            'product': self.product1.id,
            'quantity': 1
        })
        item_id = response.json()['items'][0]['id']

        # Mettre à jour la quantité
        resp = self.client.post('/api/cart/update_item/', {
            'item_id': item_id,
            'quantity': 5
        })
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.json()['items'][0]['quantity'], 5)

        # Supprimer l'item
        resp = self.client.post('/api/cart/remove/', {
            'item_id': item_id
        })
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp.json()['items']), 0)

    def test_cart_persists_after_relogin(self):
        """Test de persistance après reconnexion"""
        # Ajouter un item
        self.client.post('/api/cart/add/', {
            'product': self.product1.id,
            'quantity': 1
        })

        # Se déconnecter
        self.client.force_authenticate(user=None)

        # Se reconnecter
        self.client.force_authenticate(user=self.user)

        # Vérifier que le panier existe toujours
        resp = self.client.get('/api/cart/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp.json()["items"]), 1)

    def test_sync_endpoint_merges_guest_cart_into_user_cart(self):
        """Test de synchronisation du panier invité vers utilisateur"""
        # Créer des items "invité" à synchroniser
        guest_items = [
            {
                'product': self.product1.id,
                'quantity': 2,
                'color': 'blue',
                'size': 'L'
            },
            {
                'product': self.product2.id,
                'quantity': 1,
                'color': 'red',
                'size': 'S'
            }
        ]

        # Synchroniser
        resp = self.client.post('/api/cart/sync/', {
            'items': guest_items
        }, format='json')

        self.assertIn(resp.status_code, (status.HTTP_200_OK, status.HTTP_201_CREATED, status.HTTP_204_NO_CONTENT))

        # Vérifier que les items sont dans le panier
        cart_resp = self.client.get('/api/cart/')
        self.assertEqual(len(cart_resp.json()['items']), 2)