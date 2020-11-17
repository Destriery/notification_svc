import smtpd
import asyncore


class FakeSMTPServer(smtpd.SMTPServer):
    """A Fake smtp server"""

    def __init__(*args, **kwargs):
        smtpd.SMTPServer.__init__(*args, **kwargs)

    def process_message(*args, **kwargs):
        return None


if __name__ == "__main__":
    smtp_server = FakeSMTPServer(('localhost', 8025), None)
    try:
        asyncore.loop()
    except KeyboardInterrupt:
        smtp_server.close()
