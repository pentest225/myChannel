from django.contrib import admin
from . import models
# Register your models here.
class MessageInline(admin.TabularInline):
    model = models.Message
    extra = 0

@admin.register(models.Salon)
class SalonAdmin(admin.ModelAdmin):
    list_display=('user','nom','date_add','date_upd','status')
    list_filter=('date_add','date_upd','status')
    search_fields=['nom']
    inlines=[MessageInline]
    
    
@admin.register(models.Message)
class MessageAdmin(admin.ModelAdmin):
    list_display=('user','salon','message','date_add','date_upd','status')
    list_filter=('date_add','date_upd','status')
    search_fields=['message']
    