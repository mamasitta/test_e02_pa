from rest_framework.views import APIView
from .models import Book, Review
from .serializers import BookSerializer, ReviewSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .permissions import CanUpdateReview, ISAdminOrReviewAuthor

# Create your views here.

class BookList(APIView):

    def get(self, request):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)


    def post(self, request):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def book_detail(request, pk):
    try:
        book = Book.objects.get(pk=pk)
    except Book.DoesNotExist:
        return Response(status=404)


    if request.method == 'GET':
        serializer = BookSerializer(book)
        return Response(serializer.data, status=200)
    

    elif request.method == 'PUT':
        serializer = BookSerializer(book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)
    
    elif request.method == 'PATCH':
        serializer = BookSerializer(book, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)
    
    elif request.method == 'DELETE':
        book.delete()
        return Response(status=204)
    

class ReviewListCreateAPIView(APIView):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticatedOrReadOnly, ]

    def get(slef, request):
        reviews = Review.objects.all()
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = ReviewSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    

from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

from django.http import HttpResponse
def token(request):
    user = User.objects.get(username='test2')
    token = Token.objects.create(user=user)
    return HttpResponse(token)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
@authentication_classes([TokenAuthentication, ])
def review_detail(request, pk):
    try:
        review = Review.objects.get(pk=pk)
    except Review.DoesNotExist:
        return Response(status=404)
    

    if request.method == 'GET':
        serializer = ReviewSerializer(review)
        return Response(serializer.data, status=200)
    
    elif request.method in ['PUT', 'PATCH']:
        permission = CanUpdateReview()
        if not permission.has_object_permission(request=request, obj=review):
            return Response({"error": "You dont have permission"}, status=403)
        
        partial = request.method == 'PATCH'
        serializer = ReviewSerializer(
            review, 
            data=request.data, 
            context={'request': request}, 
            partial=partial)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, 400)
    
    elif request.method == 'DELETE':
        permission = ISAdminOrReviewAuthor()
        if not permission.has_object_permission(request=request, obj=review):
            return Response({"error": "You dont have permission"}, status=403)
        
        review.delete()
        return Response(status=204)
        



        


    
