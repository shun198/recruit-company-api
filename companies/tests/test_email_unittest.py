import json
from django.core import mail
from django.test import TestCase
from django.test import Client

class EmailUnitTest(TestCase):
    def test_send_email_should_succeed(self) -> None:
        with self.settings(
            EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend"
        ):
            # Send message
            mail.send_mail(
                subject="Test Subject",
                message="Test Message",
                from_email="testemail@example.com",
                recipient_list=["testemail2@example.com"],
                fail_silently=False,
            )
            # メールを一通送信
            self.assertEqual(len(mail.outbox),1)
            # メールの件名が正しい
            self.assertEqual(mail.outbox[0].subject,"Test Subject")

    def test_send_email_without_arguments_should_send_empty_email(self) -> None:
        client = Client()
        response = client.post(path="/api/send-email")
        response_content = json.loads(response.content)
        self.assertEqual(response.status_code,200)
        self.assertEqual(response_content["status"],"success")
        self.assertEqual(response_content["info"],"email sent successfully")
