from django.contrib.sitemaps import Sitemap
from books.models import Book, Author
from reviews.models import Review


class BookSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.8

    def items(self):
        return Book.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.updated_at


class AuthorSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.7

    def items(self):
        return Author.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.updated_at


class ReviewSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.6

    def items(self):
        return Review.objects.filter(status='public', is_active=True)

    def lastmod(self, obj):
        return obj.updated_at
