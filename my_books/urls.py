
from django.urls import path
from .views import BookList, book_detail, ReviewListCreateAPIView, token, review_detail


app_name = 'books'
urlpatterns = [
    path('books/', BookList.as_view(), name='books-list'),
    path('books/<int:pk>/', book_detail, name='book-detail'),

    path('reviews/', ReviewListCreateAPIView.as_view(), name='reviews-list'),
    path('reviews/<int:pk>/', review_detail, name='review-detail'), 
    # TEST Token view
    path('token/', token),
]