from rest_framework import serializers
from .models import Book, Review
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError
from datetime import date
from django.core.validators import MaxLengthValidator
from django.utils.html import strip_tags


class UniqueTitleValidator:

    def __call__(self, value):
        if Book.objects.filter(title=value).exists():
            raise ValidationError('Book with this title already exists')

# could be used in all fields
class PastDateValidator:

    def __call__(self, value):
        if value > date.today():
            raise ValidationError('Date should be in past')
        

class CapitalizeTitle:

    def __call__(self, value):
        return value.title()


class UserSerializer(serializers.ModelSerializer):
    
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class ReviewSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)


    class Meta:
        model = Review
        fields = ['id', 'author', 'book', 'review']


    def create(self, validated_data):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['author'] = request.user
        return super().create(validated_data)
    

class BookSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)
    # 2
    title = serializers.CharField(max_length=30, required=True, validators=[UniqueTitleValidator(), ], trim_whitespace=True)
    author = serializers.CharField(required=True, validators=[MaxLengthValidator(10)])
    published_date = serializers.DateField(required=True, validators=[PastDateValidator()])

    # 1
    def to_internal_value(self, data):
        if 'title' in data:
            data['title'] = strip_tags(data['title'].strip())
        return super().to_internal_value(data)
    
    # 3
    def validate_title(self, value):
        if Book.objects.filter(title=value).exists():
            raise serializers.ValidationError('Duplcate title')
        return value
    

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # representation['title'] = instance.title.title()
        representation['title'] = CapitalizeTitle()(instance.title)
        return representation
    
    
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'description', 'published_date', 'is_published', 'reviews']
