import unittest
import CBS_Email.Email 
from email.message import EmailMessage
from unittest.mock import Mock, patch

class TestEmailSending(unittest.TestCase):
  def setUp(self):
    # Create an email message
    self.msg = EmailMessage()
    self.msg['Subject'] = 'Test email'
    self.msg['From'] = 'pythonproject.team8@gmail.com'
    self.msg['To'] = 'adshree@deloitte.com'
    self.msg.set_content('This is a test email.')

  @patch('smtplib.SMTP')
  def test_send_email(self, mock_smtp):
    # Set up a mock SMTP server
    mock_server = Mock()
    mock_smtp.return_value = mock_server

    # Send the email
    # input format of Email function: [(account_id, balance, email, trans_id)]
    account_email_details_input = [('A0001','600','kidixit@deloitte.com','1'),('A0002','500','adshree@deloitte.com','2'),('A0003','-100','kidixit@deloitte.com','3'),('A0004','-200','adshree@deloitte.com','4')]
    CBS_Email.Email.Email.send_email(account_email_details_input)

    # Assert that the email was sent
    self.assertTrue(mock_server.send_message.called)
    self.assertEqual(mock_server.send_message.call_count, 1)
