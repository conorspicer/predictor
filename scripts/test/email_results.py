from django.core.mail import send_mail
from scripts.get_week import get_week
from django.template.loader import get_template


send_mail(
'Brilliantly witty subject line',
'Updated message.',
'conor@nfl-predictor.com',
['spicer.conor@gmail.com'],
fail_silently=True)
