from django.contrib import admin
from .models import ChaiVariety, ChaiReview, Store, ChaiCertificate, Favorite, ReviewComment, StoreRating

class ChaiReviewAdmin(admin.TabularInline):
    model = ChaiReview
    extra = 2

class ChaiVarietyAdmin(admin.ModelAdmin):
    list_display = ('name', 'chai_type', 'date_added', 'price')
    inlines = [ChaiReviewAdmin]
    search_fields = ('name', 'description')
    list_filter = ('chai_type', 'date_added')

class StoreAdmin(admin.ModelAdmin):
    list_display = ('name', 'store_location', 'date_added')
    filter_horizontal = ('chai_varieties',)
    search_fields = ('name', 'store_location')

class ChaiCertificateAdmin(admin.ModelAdmin):
    list_display = ('user', 'certificate_number', 'date_issued', 'valid_until')
    search_fields = ('certificate_number', 'user__username')

class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'chai_variety', 'date_added')
    search_fields = ('user__username', 'chai_variety__name')
    list_filter = ('date_added',)

class ReviewCommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'review', 'date_added', 'is_helpful')
    search_fields = ('user__username', 'comment_text')
    list_filter = ('date_added',)

class StoreRatingAdmin(admin.ModelAdmin):
    list_display = ('store', 'user', 'rating', 'date_added')
    search_fields = ('store__name', 'user__username')
    list_filter = ('rating', 'date_added')

admin.site.register(ChaiVariety, ChaiVarietyAdmin)
admin.site.register(ChaiReview)
admin.site.register(Store, StoreAdmin)
admin.site.register(ChaiCertificate, ChaiCertificateAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(ReviewComment, ReviewCommentAdmin)
admin.site.register(StoreRating, StoreRatingAdmin)
