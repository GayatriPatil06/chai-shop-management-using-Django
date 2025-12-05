from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from PIL import Image
import logging

logger = logging.getLogger(__name__)

class ChaiVariety(models.Model):
    CHAI_TYPE_CHOICE = [
        ('ML', 'Masala'),
        ('GR', 'Ginger'),
        ('KL', 'Kiwi'),
        ('PL', 'Plain'),
        ('EL', 'Elaichi'),
    ]
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='chais/')
    date_added = models.DateTimeField(default=timezone.now, db_index=True)
    chai_type = models.CharField(max_length=2, choices=CHAI_TYPE_CHOICE, default='ML', db_index=True)
    description = models.TextField(blank=True, default='')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=100.00)

    class Meta:
        ordering = ['-date_added']
        indexes = [
            models.Index(fields=['chai_type', '-date_added']),
        ]

    def __str__(self):
        return self.name
    
    def get_average_rating(self):
        """Get average rating for this chai"""
        from django.db.models import Avg
        avg = self.reviews.aggregate(Avg('rating'))['rating__avg']
        return round(avg, 2) if avg else 0
    
    def get_review_count(self):
        """Get total number of reviews"""
        return self.reviews.count()
    
    def get_favorite_count(self):
        """Get total number of favorites"""
        return self.favorited_by.count()

    def save(self, *args, **kwargs):
        """Override save to compress image on upload"""
        super().save(*args, **kwargs)
        
        # Compress image if it exists
        if self.image:
            try:
                img = Image.open(self.image.path)
                
                # Convert RGBA to RGB if necessary (for JPEG compatibility)
                if img.mode in ('RGBA', 'LA', 'P'):
                    rgb_img = Image.new('RGB', img.size, (255, 255, 255))
                    rgb_img.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                    img = rgb_img
                
                # Compress image: max width 800px, quality 85
                max_width = 800
                if img.width > max_width:
                    ratio = max_width / img.width
                    new_height = int(img.height * ratio)
                    img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)
                
                # Save compressed image
                img.save(self.image.path, 'JPEG', quality=85, optimize=True)
                logger.info(f"Image compressed for ChaiVariety: {self.name}")
            except Exception as e:
                logger.warning(f"Failed to compress image for {self.name}: {str(e)}")

class ChaiReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    chai_variety = models.ForeignKey(ChaiVariety, on_delete=models.CASCADE, related_name='reviews')
    review_text = models.TextField()
    rating = models.IntegerField(default=1, choices=[(i, i) for i in range(1, 6)])
    date_added = models.DateTimeField(default=timezone.now, db_index=True)
    comment_count = models.IntegerField(default=0)

    class Meta:
        ordering = ['-date_added']
        indexes = [
            models.Index(fields=['chai_variety', '-date_added']),
            models.Index(fields=['user', '-date_added']),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.chai_variety.name} Review"

class Store(models.Model):
    name = models.CharField(max_length=100)
    chai_varieties = models.ManyToManyField(ChaiVariety, related_name='stores')
    store_location = models.CharField(max_length=255)
    date_added = models.DateTimeField(default=timezone.now, db_index=True)

    class Meta:
        ordering = ['-date_added']
        indexes = [
            models.Index(fields=['-date_added']),
        ]

    def __str__(self):
        return self.name
    
    def get_average_rating(self):
        """Get average store rating"""
        from django.db.models import Avg
        avg = self.ratings.aggregate(Avg('rating'))['rating__avg']
        return round(avg, 2) if avg else 0
    
    def get_rating_count(self):
        """Get total number of ratings"""
        return self.ratings.count()

class ChaiCertificate(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='chai_certificate')
    certificate_number = models.CharField(max_length=20, unique=True, db_index=True)
    date_issued = models.DateTimeField(default=timezone.now, db_index=True)
    chai_variety = models.ForeignKey(ChaiVariety, on_delete=models.CASCADE, related_name='certificates')
    valid_until = models.DateTimeField()

    class Meta:
        ordering = ['-date_issued']
        indexes = [
            models.Index(fields=['user', '-date_issued']),
        ]

    def __str__(self):
        return f"Certificate {self.certificate_number} for {self.user.username}"

class Favorite(models.Model):
    """Users can mark chais as favorites"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorite_chais')
    chai_variety = models.ForeignKey(ChaiVariety, on_delete=models.CASCADE, related_name='favorited_by')
    date_added = models.DateTimeField(default=timezone.now, db_index=True)

    class Meta:
        unique_together = ('user', 'chai_variety')
        ordering = ['-date_added']
        indexes = [
            models.Index(fields=['user', '-date_added']),
        ]

    def __str__(self):
        return f"{self.user.username} favorites {self.chai_variety.name}"

class ReviewComment(models.Model):
    """Comments on chai reviews"""
    review = models.ForeignKey(ChaiReview, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.TextField()
    date_added = models.DateTimeField(default=timezone.now, db_index=True)
    is_helpful = models.IntegerField(default=0)  # Upvote count

    class Meta:
        ordering = ['-date_added']
        indexes = [
            models.Index(fields=['review', '-date_added']),
        ]

    def __str__(self):
        return f"{self.user.username} commented on {self.review}"

class StoreRating(models.Model):
    """Rate stores based on quality, service, etc."""
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField(blank=True)
    date_added = models.DateTimeField(default=timezone.now, db_index=True)

    class Meta:
        unique_together = ('store', 'user')
        ordering = ['-date_added']
        indexes = [
            models.Index(fields=['store', '-date_added']),
            models.Index(fields=['user', '-date_added']),
        ]

    def __str__(self):
        return f"{self.user.username} rated {self.store.name} - {self.rating}"
