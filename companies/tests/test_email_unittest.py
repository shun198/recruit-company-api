import json
from django.core import mail
from django.test import TestCase,Client
from django.template.loader import render_to_string
from unittest.mock import patch

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

    # Mock
    #
    def test_send_email_without_arguments_should_send_empty_email_without_mocking(self) -> None:
        client = Client()
        response = client.post(path="/api/send-email")
        response_content = json.loads(response.content)
        self.assertEqual(response.status_code,200)
        self.assertEqual(response_content["status"],"success")
        self.assertEqual(response_content["info"],"email sent successfully")

    def test_send_email_without_arguments_should_send_empty_email_with_mocking(self) -> None:
        client = Client()
        plaintext = render_to_string("../templates/welcome_email.txt")
        html_text = render_to_string("../templates/welcome_email.html")
        with patch(
            # viewsにあるsend_mailメソッドを指定
            "companies.views.mail.send_mail"
        ) as mocked_send_mail_function:
            response = client.post(path="/api/send-email")
            response_content = json.loads(response.content)
            self.assertEqual(response.status_code,200)
            self.assertEqual(response_content["status"],"success")
            self.assertEqual(response_content["info"],"email sent successfully")
            mocked_send_mail_function.assert_called_with(
                subject="ようこそメール",
                message=plaintext,
                from_email="send@mail.com",
                recipient_list=["recieve@mail.com"],
                html_message=html_text,
            )

    def test_send_email_with_get_verb_should_fail(self) -> None:
        client = Client()
        response = client.get(path="/api/send-email")
        assert response.status_code == 405
        assert json.loads(response.content) == {"detail":'メソッド "GET" は許されていません。'}
