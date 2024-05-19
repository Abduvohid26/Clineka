from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
import os

phone_regex = RegexValidator(
    regex=r'^\+998([- ])?(90|91|93|94|95|98|99|33|97|71|88|20|)([- ])?(\d{3})([- ])?(\d{2})([- ])?(\d{2})$',
    message='Invalid phone number'
)



def validate_image(value):
    valid_extensions = ['.jpg', '.jpeg', '.png', '.svg']
    ext = os.path.splitext(value.name)[1]
    if not ext.lower() in valid_extensions:
        raise ValidationError('Faqat JPG, JPEG, PNG, SVG  formatidagi rasmlarni yuklang.')

    
    max_size = 4 * 1024 * 1024  # 4 MB
    if value.size > max_size:
        raise ValidationError('Rasm hajmi 4 MB dan katta bo\'lishi mumkin emas.')