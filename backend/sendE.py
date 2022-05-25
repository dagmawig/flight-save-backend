from django.core.mail import send_mail



def sendEmail(subject, message, email):
    try:
        send_mail(
            subject,
            message,
            "111automail@gmail.com",
            [email],
            fail_silently=False,
        )
        return {"success": True, "error": None}
    except Exception as e:
        print(e)
        return {"success": False, "error": e}