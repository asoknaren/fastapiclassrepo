from unittest.mock import MagicMock
from notifier import Notifier

def test_alert_user_sends_email():
    # 1. ARRANGE
    mock_email_service = MagicMock()
    notifier = Notifier(email_service=mock_email_service)

    # 2. ACT
    notifier.alert_user("user@example.com", "System failure!")

    # 3. ASSERT
    # MagicMock lets us look back in time and inspect the call
    mock_email_service.send.assert_called_once_with(
        to="user@example.com", 
        body="System failure!"
    )
