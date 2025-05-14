from django.db import models
import os
from django.core.mail import EmailMessage
from django.conf import settings
from docxtpl import DocxTemplate
import uuid
from datetime import datetime

class PassTemplate(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    template_file = models.FileField(upload_to='templates/')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class Department(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Pass(models.Model):
    full_name = models.CharField(max_length=255)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    purpose = models.TextField()
    date_issued = models.DateTimeField(auto_now_add=True)
    valid_until = models.DateTimeField()
    email = models.EmailField()
    template = models.ForeignKey(PassTemplate, on_delete=models.SET_NULL, null=True, blank=True)
    generated_document = models.FileField(upload_to='passes/', null=True, blank=True)
    is_archived = models.BooleanField(default=False)
    
    def __str__(self):
        return f'{self.full_name} ({self.department})'
    
    def generate_document(self):
        if not self.template:
            # Use default template
            template_path = os.path.join(settings.BASE_DIR, '../templates/Blank_razovogo_propuska.docx')
        else:
            template_path = self.template.template_file.path
            
        doc = DocxTemplate(template_path)
        
        # Prepare context for the template
        context = {
            'full_name': self.full_name,
            'department': self.department.name,
            'purpose': self.purpose,
            'date_issued': self.date_issued.strftime('%d.%m.%Y'),
            'valid_until': self.valid_until.strftime('%d.%m.%Y'),
            'pass_id': str(self.id),
        }
        
        # Render the document
        doc.render(context)
        
        # Save the document
        filename = f"pass_{self.id}_{uuid.uuid4().hex[:8]}.docx"
        output_path = os.path.join(settings.MEDIA_ROOT, 'passes', filename)
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        doc.save(output_path)
        
        # Update the model
        self.generated_document = f'passes/{filename}'
        self.save(update_fields=['generated_document'])
        
        return self.generated_document
    
    def send_email(self):
        if not self.generated_document:
            self.generate_document()
            
        email = EmailMessage(
            subject=f'Pass for {self.full_name}',
            body=f'Please find attached your pass valid until {self.valid_until.strftime("%d.%m.%Y")}.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[self.email],
        )
        
        # Attach the document
        document_path = os.path.join(settings.MEDIA_ROOT, str(self.generated_document))
        email.attach_file(document_path)
        
        # Send the email
        return email.send() 