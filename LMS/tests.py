from django.test import TestCase
from LMS.models import *
from django.urls import reverse
from django.contrib import auth

# Create your tests here.
class CategoryMethodTests(TestCase):
    def test_ensure_views_are_positive(self):
        """
        Ensures the number of views in a given category is not negative
        """

        category = Category(name='test', views=-1)
        category.save()

        self.assertEqual((category.views >= 0 ), True)
    
    def test_slug_line_creation(self):
        """
        Checks to make sure that the category slug is created
        appropriately, i.e Classic Works should slug to classic-works
        """

        category = Category(name='Classic Works')
        category.save()

        self.assertEqual(category.slug, 'classic-works')

class ISBNMethodTests(TestCase):
        def test_ensure_views_are_positive(self):
            def add_category(self, name, views=0):
                category = Category(name=name)
                category.save()
                
                return category
        
            category = add_category("Tester",9)
            
            isbn = ISBN(ISBN=1, category=category, views=-1)
            isbn.save()

            self.assertEqual((isbn.views >= 0 ), True)

class SearchViewTests(TestCase):
    def test_search_view_with_no_categories(self):
        """
        Ensures that when no categories are present, the search page
        displays a view to reflect this
        """

        response = self.client.get(reverse('LMS:browse'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'There are no categories present.')
        self.assertQuerysetEqual(response.context['categories'], [])

    def add_category(self, name, views=0):
        category = Category(name=name)
        category.save()
        
        return category

    def test_search_view_with_categories(self):

        """
        Ensures categories are displayed correctly when present, also
        checks that the correct number of categories are present
        """

        self.add_category('Science Fictions')
        self.add_category('Romance')
        self.add_category('Philosophy')

        response = self.client.get(reverse('LMS:browse'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Science Fiction")
        self.assertContains(response, "Romance")
        self.assertContains(response, "Philosophy")

        num_categories = len(response.context['categories'])
        self.assertEquals(num_categories, 3)
    
    def test_category_that_already_exists_cannot_be_added_again(self):
        
        response = self.client.get(reverse('LMS:browse'))
        self.add_category('General Works')
        self.assertEquals(response.status_code, 200)
        self.add_category('General Works')
        self.assertEquals(response.status_code, 302)

class CategorySlugViewTests(TestCase):

    def test_category_slug_with_no_books_present(self):
        """
        Ensures that when no books are present, the category slugged page
        displays a view to reflect this
        """

        response = self.client.get('LMS/browse/general-works')

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'There are no books present.')
        self.assertQuerysetEqual(response.context['ISBN'], [])

    def add_ISBN(self, isbn, category, title, author, genre, views = 0):
        """
        This method adds an instance of an ISBN according to the ISBN model
        """
        def add_category(self, name, views=0):
            category = Category(name=name)
            category.save()
            
            return category
        
        category = add_category(category,9)
        isbn = ISBN(ISBN=isbn,category=category,title=title,author=author,genre=genre)
        isbn.save()
        return isbn

    def test_category_slug_with_books_present(self):

        self.add_ISBN(1000000, "General Workings", "A book", "A. Woman", "Romance")
        self.add_ISBN(1000001, "General Workings", "Another Book", "A. Notherwoman", "Murder Mystery")
        self.add_ISBN(1000002, "General Workings", "A Final Book", "A. Finalwoman", "Science Fiction")

        response = self.client.get('LMS/browse/general-works')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "A book")
        self.assertContains(response, "Another Book")
        self.assertContains(response, "A Final Book")

        num_ISBN = len(response.context['ISBN'])
        self.assertEquals(num_ISBN, 3)

class UserAuthenticationTests(TestCase):

    def test_unauthenticated_user_can_access_home(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
    
    def test_unauthenticated_user_can_access_browse(self):
        response = self.client.get(reverse('LMS:browse'))
        self.assertEqual(response.status_code, 200)

    def test_unauthenticated_user_can_access_search(self):
        response = self.client.get(reverse('LMS:search'))
        self.assertEqual(response.status_code, 200)
    
    def test_unauthenticated_user_cannot_access_staffpage(self):
        response = self.client.get(reverse('LMS:staff_page'))
        self.assertContains(response, "You are not authorised to view this page.")
    
    def test_unauthenticated_user_cannot_access_addbook(self):
        response = self.client.get(reverse('LMS:add_book'))
        self.assertContains(response, "You are not authorised to view this page.")

    def test_unauthenticated_user_cannot_access_addcategory(self):
        response = self.client.get(reverse('LMS:add_category'))
        self.assertContains(response, "You are not authorised to view this page.")

    def test_unauthenticated_user_cannot_access_addstaff(self):
        response = self.client.get(reverse('LMS:add_staff'))
        self.assertContains(response, "You are not authorised to view this page.")




class UserLoginOutTests(TestCase):

    def add_user(self, user, password, book_limit=10):
        """
        This method adds an instance of a user
        according to the user model
        """
        member = User(username=user, password=password)
        member.password = password
        
        member.save()
        return member


    def test_user_logs_in_successfully(self):

        self.add_user("TestUser", "TestUsersPassword2000")

        response = self.client.post(reverse('LMS:login'),
                                    {'username': 'TestUser',
                                    'password': 'TestUsersPassword2000'})
        self.assertEqual(response.status_code, 200)
        user = auth.get_user(self.client)
        self.assertContains(response, "You are now logged in as TestUser")


