from django.test import TestCase
from LMS.models import *
from django.urls import reverse
from django.contrib import auth

# Create your tests here.
class CategoryMethodTests(TestCase):
    """
    def test_ensure_views_are_positive(self):
        
        Ensures the number of views in a given category is not negative
        

        category = Category(name='test', views=-1)
        category.save()

        self.assertEqual((category.views >= 0 ), True)
    """
    
    def test_slug_line_creation(self):
        """
        Checks to make sure that the category slug is created
        appropriately, i.e Classic Works should slug to classic-works
        """

        category = Category(name='Classic Works')
        category.save()

        self.assertEqual(category.slug, 'classic-works')
"""
class ISBNMethodTests(TestCase):
    def test_ensure_views_are_positive(self):
        
        Ensures the number of views on a given books ISBN is not negative
        

        isbn = ISBN(ISBN= 01234567890, views=-1)
        category.save()

        self.assertEqual((category.views >= 0 ), True)
"""

class SearchViewTests(TestCase):
    def test_search_view_with_no_categories(self):
        """
        Ensures that when no categories are present, the search page
        displays a view to reflect this
        """

        response = self.client.get(reverse('/LMS/browse'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'There are no categories present.')
        self.assertQuerysetEqual(response.context['categories'], [])

    def add_category(name, views=0):
        category = Category.objects.get_or_create(name=name)[0]
        category.views = views
        
        category.save()
        return category

    def test_search_view_with_categories(self):

        """
        Ensures categories are displayed correctly when present, also
        checks that the correct number of categories are present
        """

        add_category('General Works')
        add_category('Drama')
        add_category('Philosophy')

        response = self.client.get(reverse('/LMS/browse'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "General Works")
        self.assertContains(response, "Drama")
        self.assertContains(response, "Philosophy")

        num_categories = len(response.context['categories'])
        self.assertEquals(num_categories, 3)

class CategorySlugViewTests(TestCase):

    """
    def test_category_slug_with_no_books_present(self):
        
        Ensures that when no books are present, the category slugged page
        displays a view to reflect this
        

        response = self.client.get(reverse('/LMS/browse/general-works'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'There are no books present.')
        self.assertQuerysetEqual(response.context['ISBN'], [])
    """

    def add_ISBN():
        """
        This method should add an instance of an ISBN according to the ISBN model
        """



    def test_category_slug_with_books_present(self):

        add_ISBN()
        add_ISBN()
        add_ISBN()

        response = self.client.get(reverse('/LMS/browse'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "name")
        self.assertContains(response, "name")
        self.assertContains(response, "name")

        num_ISBN = len(response.context['ISBN'])
        self.assertEquals(ISBN, 3)

class UserAuthenticationTests(TestCase):

    def test_unauthenticated_user_can_access_home(self):
        response = self.client.get(reverse('/LMS'))
        self.assertEqual(response.status_code, 200)
    
    def test_unauthenticated_user_can_access_browse(self):
        response = self.client.get(reverse('/LMS/browse'))
        self.assertEqual(response.status_code, 200)

    def test_unauthenticated_user_can_access_search(self):
        response = self.client.get(reverse('/LMS/search'))
        self.assertEqual(response.status_code, 200)
    
    def test_unauthenticated_user_cannot_access_staffpage(self):
        response = self.client.get(reverse('/LMS/staff_page'))
        self.assertContains(response, "You are not authorised to view this page.")
    
    def test_unauthenticated_user_cannot_access_addbook(self):
        response = self.client.get(reverse('/LMS/add_book'))
        self.assertContains(response, "You are not authorised to view this page.")
        
    def test_unauthenticated_user_cannot_access_addcategory(self):
        response = self.client.get(reverse('/LMS/add_category'))
        self.assertContains(response, "You are not authorised to view this page.")
        
    def test_unauthenticated_user_cannot_access_addstaff(self):
        response = self.client.get(reverse('/LMS/add_staff'))
        self.assertContains(response, "You are not authorised to view this page.")

class UserLoginOutTests(TestCase):

    def add_user():
        """
        This method should add an instance of a user
        according to the user model
        """

    def test_user_logs_in_successfully(self):

        add_user()

        response = self.client.post(reverse('/LMS/login'),
                                    {'username': 'username',
                                    'password': 'password'})
        self.assertEqual(response.status_code, 200)
        user = auth.get_user(self.client)
        assert user.is_authenticated()

