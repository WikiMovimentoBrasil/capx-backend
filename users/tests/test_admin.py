from django.contrib import admin
from django.test import TestCase, RequestFactory
from unittest.mock import patch, call
from users.admin import AccountUserAdmin, ProfileInline
from users.models import CustomUser

class AccountUserAdminTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.admin = AccountUserAdmin(model=CustomUser, admin_site=admin.site)
    
    @patch('django.contrib.auth.admin.UserAdmin.add_view')
    def test_add_view(self, mock_add_view):
        request = self.factory.get('/admin/users/customuser/add/')
        
        # Call the add_view method
        self.admin.add_view(request)
        
        # Check that inlines is set to an empty list
        self.assertEqual(self.admin.inlines, [])
        
        # Check that the super add_view method was called
        mock_add_view.assert_called_once_with(request)
    
    @patch('django.contrib.auth.admin.UserAdmin.change_view')
    def test_change_view(self, mock_change_view):
        request = self.factory.get('/admin/users/customuser/1/change/')
        
        # Call the change_view method
        self.admin.change_view(request)
        
        # Check that inlines is set to [ProfileInline]
        self.assertEqual(self.admin.inlines, [ProfileInline])
        
        # Check that the super change_view method was called
        mock_change_view.assert_called_once_with(request)
