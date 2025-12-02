import ssl
import smtplib

def patch_smtp_ssl():
    # Создаем контекст, который НЕ проверяет сертификаты
    context = ssl._create_unverified_context()

    # Monkey-patch для smtplib.SMTP.starttls
    original_starttls = smtplib.SMTP.starttls

    def patched_starttls(self, *args, **kwargs):
        kwargs['context'] = context
        return original_starttls(self, *args, **kwargs)

    smtplib.SMTP.starttls = patched_starttls
