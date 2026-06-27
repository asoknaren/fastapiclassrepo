from GoogleEmailService import *

class Notifier:
    def __init__(self, email_service):
        self.email_service = email_service

    def alert_user(self, email, message):
        if not message:
            return False
        self.email_service.send(to=email, body=message)
        print(f"Sending email to {email} with body: {message} successful")

        return True


if __name__ == "__main__":
    my_notifier = Notifier(email_service=GoogleEmailService())
    my_notifier.alert_user("user@example.com", "System failure!")   

