import os
import django
import sys
import pandas as pd
from django.utils.text import slugify
from django.db import transaction
import urllib.request
from django.core.files.base import ContentFile

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bookreview.settings')
django.setup()

from books.models import DataSeedTracker, Genre, Author, Publisher, Book, Tag, BookEdition

SEED_KEY = "seed_data_Nov_2025"

if DataSeedTracker.objects.filter(seed_key=SEED_KEY).exists():
    print("ĐÃ IMPORT RỒI → BỎ QUA")
    sys.exit(0)

print("BẮT ĐẦU IMPORT DỮ LIỆU...")

def safe_int(value, default=None):
    if pd.isna(value) or value in ['', None]:
        return default
    try:
        return int(float(str(value).strip()))
    except:
        return default

def safe_decimal(value, default=0.00):
    if pd.isna(value) or value in ['', None]:
        return default
    try:
        return float(str(value).strip())
    except:
        return default

def download_cover(book_instance, url):
    if not url or not url.startswith('http'):
        return
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=15) as response:
            filename = os.path.basename(url.split('?')[0])
            if not filename.lower().endswith(('.png', '.jpg', '.jpeg', '.webp', '.gif')):
                filename = f"{book_instance.slug}.jpg"
            book_instance.cover.save(filename, ContentFile(response.read()), save=True)
    except Exception as e:
        print(f"   → Lỗi tải ảnh: {url} | {e}")

@transaction.atomic
def seed():
    created_books = 0

    # 1. Authors
    if os.path.exists('author_data.csv'):
        df = pd.read_csv('author_data.csv', dtype=str).fillna('')
        for _, row in df.iterrows():
            name = row['name'].strip()
            if not name:
                continue
            slug = slugify(name)[:200]
            Author.objects.update_or_create(
                slug=slug,
                defaults={
                    'name': name,
                    'bio': row.get('biography', '')[:2000],
                    'birth_date': row.get('birth_date') if row.get('birth_date') else None,
                    'death_date': row.get('death_date') if row.get('death_date') else None,
                    'nationality': row.get('nationality', ''),
                    'website': row.get('website', '') if str(row.get('website','')).startswith('http') else '',
                    'is_active': True,
                }
            )

    # 2. Genres
    if os.path.exists('genres_data.csv'):
        df = pd.read_csv('genres_data.csv', dtype=str).fillna('')
        for _, row in df.iterrows():
            name = row['name'].strip()
            if not name:
                continue
            Genre.objects.update_or_create(
                slug=slugify(name)[:100],
                defaults={
                    'name': name,
                    'description': row.get('description', '')[:500],
                    'is_active': True
                }
            )

    # 3. Publishers
    if os.path.exists('publisher_data.csv'):
        df = pd.read_csv('publisher_data.csv', dtype=str).fillna('')
        for _, row in df.iterrows():
            name = row['name'].strip() or "Không rõ"
            Publisher.objects.update_or_create(
                slug=slugify(name)[:200],
                defaults={
                    'name': name,
                    'description': row.get('description', '')[:1000],
                    'website': row.get('website', '') if str(row.get('website','')).startswith('http') else '',
                    'is_active': True
                }
            )

    # 4. Tags
    all_tags = set()
    if os.path.exists('book_data.csv'):
        df_temp = pd.read_csv('book_data.csv', dtype=str).fillna('')
        for tag_str in df_temp['tag'].dropna():
            for t in str(tag_str).split(','):
                t = t.strip()
                if t:
                    all_tags.add(t)
        for tag_name in all_tags:
            Tag.objects.get_or_create(
                slug=slugify(tag_name)[:50],
                defaults={'name': tag_name, 'is_active': True}
            )


    # 5. Books
    if os.path.exists('book_data.csv'):
        df = pd.read_csv('book_data.csv', dtype=str).fillna('')
        for idx, row in df.iterrows():
            title = row['title'].strip()
            if not title:
                continue

            pub_name = row['publisher'].strip() or "Không rõ"
            publisher, _ = Publisher.objects.get_or_create(
                slug=slugify(pub_name), defaults={'name': pub_name}
            )

            base_slug = slugify(title)[:480]
            slug = base_slug
            i = 1
            while Book.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{i}"
                i += 1
            
            link_buy_url = row.get('link_buy', '').strip() if 'link_buy' in row else ''

            book = Book.objects.create(
                title=title,
                slug=slug,
                description=row['description'][:3000],
                year=safe_int(row['year']),
                pages=safe_int(row['pages']),
                publisher=publisher,
                avg_rating=safe_decimal(row['rating_avg'], 0.00),
                review_count=safe_int(row['review_count'], 0),
                rating_count=safe_int(row['review_count'], 0),
                link_buy=link_buy_url,
                language='vi',
                is_active=True,
            )
            created_books += 1
            print(f"[{created_books}] Đã tạo: {title}")

            cover_url = row['cover'].strip()
            if cover_url:
                download_cover(book, cover_url)

            for a_name in str(row['author']).split(','):
                a_name = a_name.strip()
                if a_name:
                    auth, _ = Author.objects.get_or_create(slug=slugify(a_name), defaults={'name': a_name})
                    book.authors.add(auth)

            for g_name in str(row['genres']).split(','):
                g_name = g_name.strip()
                if g_name:
                    genre, _ = Genre.objects.get_or_create(slug=slugify(g_name), defaults={'name': g_name})
                    book.genres.add(genre)

            for t_name in str(row['tag']).split(','):
                t_name = t_name.strip()
                if t_name:
                    tag, _ = Tag.objects.get_or_create(slug=slugify(t_name), defaults={'name': t_name})
                    book.tags.add(tag)

            BookEdition.objects.create(
                book=book,
                isbn13=row['isbn'][-13:] if row['isbn'] and len(row['isbn']) >= 13 else None,
                pages=safe_int(row['pages']),
                language='vi',
            )

    print(f"\nĐÃ IMPORT {created_books} SÁCH!")
    DataSeedTracker.objects.create(seed_key=SEED_KEY)

try:
    seed()
except Exception as e:
    print(f"LỖI: {e}")
    raise