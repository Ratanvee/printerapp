from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid




class CustomUser(AbstractUser):
    unique_url = models.SlugField(unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.unique_url:  # Generate only if it's empty
            base_url = self.username.lower().replace(" ", "-")
            unique_part = str(uuid.uuid4())[:8]  # Ensuring uniqueness
            self.unique_url = f"{base_url}-{unique_part}"

            # Ensure uniqueness in case of a rare conflict
            while CustomUser.objects.filter(unique_url=self.unique_url).exists():
                unique_part = str(uuid.uuid4())[:8]
                self.unique_url = f"{base_url}-{unique_part}"

        super().save(*args, **kwargs)




class Document(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="documents")
    file = models.FileField(upload_to="uploads/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.file.name} uploaded by {self.user.username}"
