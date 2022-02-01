from django.core.mail import send_mail

def send_activation_code(email, activation_code):
    message = f"""
    Поздравляем! Вы зарегестрированы на нашем сайте.
    Пройдите активацию вашего аккаунта отправив
    на http://localhost/api/v1/activate/ этот код: {activation_code}
    """
    send_mail(
        'Активация аккаунта',
        message,
        'test@gmail.com',
        [email]
    )