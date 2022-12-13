from django.contrib import admin
from .models import Feedback
# Register your models here.

class FeedbackAdmin(admin.ModelAdmin):
    pass
admin.site.register(Feedback, FeedbackAdmin)
# Register your models here.

# Register your models here.
