from django.core.mail import send_mail

def send_activation_code(email, activation_code):
    activation_url = f"http://localhost:8000/api/v1/activate/{activation_code}"
    message = f"""
    Поздравляем! Вы зарегестрированы на нашем сайте.
    Пройдите активацию вашего аккаунта по ссылке: {activation_url}
    """
    send_mail(
        'Активация аккаунта',
        message,
        'test@gmail.com',
        [email, ],
        fail_silently=False
    )