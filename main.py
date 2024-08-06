import unittest
import requests
from unittest.mock import patch, Mock, ANY
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class TestAbsFunction(unittest.TestCase):
    def test_positive_number(self):
        self.assertEqual(abs(10), 10)

    def test_negative_number(self):
        self.assertEqual(abs(-10), 10)

    def test_zero(self):
        self.assertEqual(abs(0), 0)


# A function that makes an api call gets a response and then returns the json object

def get_user_data(user_id):
    response = requests.get(f"https://api.example.com/users/{user_id}")
    return response.json()


class TestUserData(unittest.TestCase):
    # every get request will be mocked
    @patch('requests.get')
    def test_get_user_date(self, mock_get):
        mock_response = Mock()
        response_dict = {'name': 'John', 'email': 'john@gmail.com'}
        mock_response.json.return_value = response_dict
        mock_get.return_value = mock_response

        user_data = get_user_data(1)
        mock_get.assert_called_with(f"https://api.example.com/users/1")
        self.assertEqual(user_data, response_dict)


def send_email(smtp_server, smtp_port, from_addr, to_addr, subject, body):
    msg = MIMEMultipart
    msg['From'] = from_addr
    msg['To'] = to_addr
    msg['subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(from_addr, "Mypassword")
    text = msg.as_string()
    server.sendmail(from_addr, to_addr, text)
    server.quit()


class TestEmail(unittest.TestCase):
    @patch('smtplib.SMTP')
    def test_send_email(self, mock_smtp):
        instance = mock_smtp.return_value
        send_email("smtp.example.com", 587, "mymail@example.com", "hismail@example.com", "subject", "mailcontent")
        mock_smtp.assert_called_with("smtp.example.com", 587)
        instance.starttls.assert_called_with()
        instance.login.assert_called_with("mymail@example.com", "Mypassword")
        instance.sendmail.assert_called_with("mymail@example.com", "hismail@example.com", ANY)
        instance.quit.assert_called_with()


if __name__ == '__main__':
    unittest.main()
