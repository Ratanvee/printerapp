from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid
from django.db import models
from django.conf import settings
from django.db import models
from django.conf import settings
from PyPDF2 import PdfReader


class CustomUser(AbstractUser):
    unique_url = models.SlugField(unique=True, blank=True, null=True)
    total_orders = models.PositiveIntegerField(default=0)  # Add this line
    total_revenue = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Add total revenue
    total_customers = models.PositiveIntegerField(default=0)  # New field

    def save(self, *args, **kwargs):
        if not self.unique_url:  # Generate only if empty
            base_url = self.username.lower().replace(" ", "-")
            unique_part = str(uuid.uuid4())[:8]
            self.unique_url = f"{base_url}-{unique_part}"

            # Ensure uniqueness in case of a rare conflict
            while CustomUser.objects.filter(unique_url=self.unique_url).exists():
                unique_part = str(uuid.uuid4())[:8]
                self.unique_url = f"{base_url}-{unique_part}"

        super().save(*args, **kwargs)


class Document(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_process', 'In Process'),
        ('completed', 'Completed'),
    ]

    file = models.FileField(upload_to="documents/")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    uploaded_at = models.DateTimeField(auto_now_add=True)


    PAPER_SIZE_CHOICES = [
        ('A4', 'A4'),
        ('A3', 'A3'),
        ('Letter', 'Letter'),
        ('Legal', 'Legal'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    file = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    num_copies = models.PositiveIntegerField(default=1)
    color_type = models.CharField(
        max_length=11,  # ✅ Increase max_length to fit the longest choice
        choices=[('black_white', 'Black & White'), ('color', 'Color'), ('both', 'Both')],
        default='black_white'
    )
    double_sided = models.BooleanField(default=False)
    paper_size = models.CharField(max_length=10, choices=PAPER_SIZE_CHOICES, default='A4')  # ✅ ADD THIS FIELD
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    num_pages = models.PositiveIntegerField(default=1)  # Stores page count
    
    def __str__(self):
        # if self.file:
        #     try:
        pdf = PdfReader(self.file)
        self.num_pages = len(pdf.pages)  # Count total pages
        print('NO. of pages : ', self.num_pages)
            # except:
        self.num_pages = 1  # Default to 1 if there's an error
        print('This is default value ')
        return f"{self.user.username} - {self.file.name}"
    
    # def save(self, *args, **kwargs):
    #     """Calculate the number of pages in the uploaded PDF before saving."""
    #     if self.file:
    #         try:
    #             pdf = PdfReader(self.file)
    #             self.num_pages = len(pdf.pages)  # Count total pages
    #             print('NO. of pages : ', self.num_pages)
    #         except:
    #             self.num_pages = 1  # Default to 1 if there's an error
    #             print('This is default value ')




from django.db import models

class Order(models.Model):
    customer_name = models.CharField(max_length=255)
    document = models.FileField(upload_to='uploads/')
    status = models.CharField(max_length=50, choices=[
        ('pending', 'Pending'),
        ('in_process', 'In Process'),
        ('completed', 'Completed')
    ], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer_name} - {self.status}"
