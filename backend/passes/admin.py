from django.contrib import admin
from .models import Department, Pass, PassTemplate

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(PassTemplate)
class PassTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at')
    search_fields = ('name', 'description')
    list_filter = ('created_at',)

@admin.register(Pass)
class PassAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'department', 'purpose', 'date_issued', 'valid_until', 'is_archived')
    list_filter = ('department', 'date_issued', 'valid_until', 'is_archived')
    search_fields = ('full_name', 'purpose', 'email')
    date_hierarchy = 'date_issued'
    actions = ['generate_documents', 'send_emails', 'archive_passes']
    
    def generate_documents(self, request, queryset):
        for pass_obj in queryset:
            pass_obj.generate_document()
        self.message_user(request, f"Generated documents for {queryset.count()} passes.")
    generate_documents.short_description = "Generate documents for selected passes"
    
    def send_emails(self, request, queryset):
        success_count = 0
        for pass_obj in queryset:
            try:
                pass_obj.send_email()
                success_count += 1
            except:
                continue
        self.message_user(request, f"Sent emails for {success_count} out of {queryset.count()} passes.")
    send_emails.short_description = "Send emails for selected passes"
    
    def archive_passes(self, request, queryset):
        queryset.update(is_archived=True)
        self.message_user(request, f"Archived {queryset.count()} passes.")
    archive_passes.short_description = "Archive selected passes" 