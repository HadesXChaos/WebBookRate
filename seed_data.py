# seed_data.py - PHIÊN BẢN HOÀN HẢO NHẤT 2025 (CẬP NHẬT TÁCH NHIỀU GENRES/TAGS)
import os
import django
import pandas as pd
import requests
from io import BytesIO
from django.core.files.images import ImageFile
from django.utils.text import slugify

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bookreview.settings')
django.setup()

from books.models import Author, Genre, Tag, Publisher, Book, BookEdition


CSV_PATH = 'book_data.csv' # Đảm bảo file CSV mới có tên này


def download_image(url):
    if not url or not str(url).startswith('http'):
        return None
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code == 200:
            filename = url.split('/')[-1].split('?')[0].split('#')[0][:100]
            if not filename.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
                filename += '.jpg'
            return ImageFile(BytesIO(response.content), name=filename)
    except Exception as e:
        print(f"   Lỗi tải ảnh: {e}")
    return None


def safe_get_or_create(model, name, field_name='name'):
    # Hàm này cố gắng tìm theo tên, sau đó theo slug, cuối cùng là tạo mới
    if not name or str(name).strip() in ['', 'nan', 'None']:
        name = "Không rõ"
    name = str(name).strip()
    slug = slugify(name)[:50]

    # Thử tìm theo tên hoặc slug
    try:
        obj = model.objects.get(**{field_name: name})
        if obj.slug != slug:
            obj.slug = slug
            obj.save(update_fields=['slug'])
        return obj
    except model.DoesNotExist:
        pass
    
    try:
        # Thử tìm theo slug nếu tìm theo tên không được
        return model.objects.get(slug=slug)
    except model.DoesNotExist:
        pass
    
    # Tạo mới
    try:
        return model.objects.create(**{field_name: name}, slug=slug)
    except:
        # Trường hợp tạo mới bị lỗi (ví dụ: slug quá dài hoặc trùng)
        try:
            # Thử lại lần nữa theo slug (đề phòng race condition)
            return model.objects.get(slug=slug)
        except:
            # Tạo mới với slug ngẫu nhiên hơn
            return model.objects.create(**{field_name: name}, slug=f"{slug}-{model.objects.count()}")


def seed():
    # Sử dụng try/except để đọc số lượng sách hiện có
    try:
        book_count = Book.objects.count()
    except Exception as e:
        print(f"Lỗi khi kiểm tra sách hiện có: {e}. Coi như chưa có sách.")
        book_count = 0

    if book_count > 0:
        print(f"ĐÃ CÓ {book_count} cuốn sách → Bỏ qua import.")
        return

    print("BẮT ĐẦU IMPORT SÁCH TỪ book_data.csv (Định dạng mới)...")
    # Đọc CSV với dtype=str để đảm bảo mọi giá trị được đọc dưới dạng chuỗi
    try:
        df = pd.read_csv(CSV_PATH, dtype=str).fillna('')
    except FileNotFoundError:
        print(f"LỖI: Không tìm thấy file CSV tại đường dẫn: {CSV_PATH}")
        return

    total = len(df)
    success_count = 0

    for idx, row in df.iterrows():
        title = str(row['title']).strip()
        print(f"[{idx+1}/{total}] Đang thêm: {title[:60]}{'...' if len(title)>60 else ''}")

        try:
            # === 1. Tác giả (author) ===
            authors = []
            # Cột mới là 'author', có thể chứa nhiều tác giả cách nhau bằng dấu ','
            author_names = [a.strip() for a in str(row['author']).split(',') if a.strip() and a.strip() not in ['nan', '.', 'DK', 'None']]
            if not author_names:
                author_names = ["Không rõ tác giả"]
                
            for name in author_names:
                author = safe_get_or_create(Author, name)
                authors.append(author)

            # === 2. Thể loại (genres) - Tách bằng dấu ',' và tạo nhiều đối tượng ===
            genres = []
            # Tách chuỗi genres bằng dấu phẩy
            genre_names = [g.strip() for g in str(row['genres']).split(',') if g.strip() and g.strip() not in ['nan', '']]
            if not genre_names:
                genre_names = ["Sách khác"]
            
            for name in genre_names:
                genre = safe_get_or_create(Genre, name)
                genres.append(genre)

            # === 3. Tag - Tách bằng dấu ',' và tạo nhiều đối tượng ===
            tags = []
            # Tách chuỗi tag bằng dấu phẩy
            tag_names = [t.strip() for t in str(row['tag']).split(',') if t.strip() and t.strip() not in ['nan', '']]
            if not tag_names:
                tag_names = ["Uncategorized"] # Vẫn giữ một tag mặc định nếu không có

            for name in tag_names:
                tag = safe_get_or_create(Tag, name)
                tags.append(tag)


            # === 4. Nhà xuất bản (publisher) ===
            publisher_name = str(row['publisher']).strip()
            if not publisher_name or publisher_name in ['nan', '', 'None']:
                publisher_name = "NXB Tổng hợp TP.HCM"
            publisher = safe_get_or_create(Publisher, publisher_name)

            # === 5. Slug sách (tránh trùng) ===
            base_slug = slugify(title)
            slug = base_slug
            counter = 1
            while Book.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            
            # Xử lý các trường số và chuỗi
            year_val = None
            try:
                year_str = str(row['year']).strip()
                if year_str and year_str != 'nan':
                    year_val = int(year_str)
            except ValueError:
                pass 
            
            pages_val = None
            try:
                pages_str = str(row['pages']).strip().replace(',', '') # Loại bỏ dấu phẩy nếu có
                if pages_str and pages_str != 'nan':
                    pages_val = int(pages_str)
            except ValueError:
                pass

            rating_avg_val = 4.0
            try:
                rating_avg_str = str(row['rating_avg']).strip().replace(',', '.') # Chuyển dấu phẩy thành dấu chấm
                if rating_avg_str and rating_avg_str != 'nan':
                    rating_avg_val = round(float(rating_avg_str), 2)
            except ValueError:
                pass
            
            review_count_val = 50 + idx # Giá trị mặc định/random nếu không có
            try:
                review_count_str = str(row['review_count']).strip().replace(',', '')
                if review_count_str and review_count_str != 'nan':
                    review_count_val = int(review_count_str)
            except ValueError:
                pass
            
            description_val = str(row['description']).strip()
            if not description_val:
                # Tạo mô tả mặc định dựa trên các genre đã tách
                description_val = f"Sách hay thuộc thể loại {', '.join(genre_names)}."

            # === 6. Tạo sách ===
            book = Book.objects.create(
                title=title,
                slug=slug,
                description=description_val, 
                year=year_val,
                pages=pages_val, 
                language='vi', 
                publisher=publisher,
                avg_rating=rating_avg_val, 
                review_count=review_count_val, 
                is_active=True
            )

            book.authors.set(authors)
            # Gán nhiều genres
            book.genres.set(genres) 
            # Gán nhiều tags
            book.tags.set(tags)     

            # === 7. Ảnh bìa ===
            cover_url = str(row['cover']).strip()
            if cover_url and cover_url.startswith('http'):
                img = download_image(cover_url)
                if img:
                    # Lưu ảnh bìa
                    book.cover.save(img.name, img, save=True)

            # === 8. Edition (Xuất bản phẩm) ===
            isbn13_val = str(row['isbn']).strip().replace('-', '') # Loại bỏ dấu gạch ngang
            if not (isbn13_val and isbn13_val != 'nan' and len(isbn13_val) == 13 and isbn13_val.isdigit()):
                isbn13_val = None 
            
            BookEdition.objects.create(
                book=book,
                isbn13=isbn13_val,
                format='paperback', 
                pages=pages_val, 
                language='vi'
            )
            
            # Bỏ qua price và link_buy

            success_count += 1
            print(f"[{idx+1}/{total}] ĐÃ THÊM: {title} ({row['year']}) - {publisher_name}")

        except Exception as e:
            print(f"LỖI [{idx+1}]: {title} → {e}")

    print(f"\nĐÃ THÊM THÀNH CÔNG {success_count}/{total} CUỐN SÁCH!")

if __name__ == '__main__':
    seed()