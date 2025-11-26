FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    build-essential \
    libpq-dev \
    netcat-traditional \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Apply migrations
COPY book_data.csv \
     author_data.csv \
     publisher_data.csv \
     genres_data.csv \
     seed_data.py \
     ./

# Copy entrypoint
COPY entrypoint.sh /entrypoint.sh
RUN sed -i 's/\r$//' /entrypoint.sh && chmod +x /entrypoint.sh


# Collect static files
RUN python manage.py collectstatic --noinput || true

# Expose port
EXPOSE 8000

# Run gunicorn
ENTRYPOINT ["/entrypoint.sh"]
CMD ["gunicorn", "bookreview.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "4"]
