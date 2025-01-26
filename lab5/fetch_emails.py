import email
from email.header import decode_header
import argparse
from poplib import POP3_SSL
from imaplib import IMAP4_SSL


class EmailFetcher:
    def __init__(self, email_user, email_password, protocol="IMAP"):
        """
        Initialize the EmailFetcher class.

        :param email_user: Email address of the user.
        :param email_password: Password or app-specific password of the user.
        :param protocol: The email protocol to use ('IMAP' or 'POP3'). Default is 'IMAP'.
        """
        self.email_user = email_user
        self.email_password = email_password
        self.protocol = protocol.upper()

        if self.protocol == "IMAP":
            self.mail = IMAP4_SSL("imap.gmail.com")
            self.mail.login(email_user, email_password)
        elif self.protocol == "POP3":
            self.mail = POP3_SSL("pop.gmail.com")
            self.mail.user(email_user)
            self.mail.pass_(email_password)
        else:
            raise ValueError("Protocol must be 'IMAP' or 'POP3'.")

    def fetch_emails(self, folder="inbox", search_criteria="ALL"):
        """
        Fetch emails using the selected protocol.

        :param folder: The folder to fetch emails from (IMAP only).
        :param search_criteria: The search criteria (e.g., 'ALL', 'UNSEEN') for IMAP.
        """
        if self.protocol == "IMAP":
            self.fetch_imap_emails(folder, search_criteria)
        elif self.protocol == "POP3":
            self.fetch_pop3_emails()

    def fetch_imap_emails(self, folder="inbox", search_criteria="ALL"):
        """
        Fetch emails using the IMAP protocol.

        :param folder: The folder to fetch emails from (default 'inbox').
        :param search_criteria: The search criteria (e.g., 'ALL', 'UNSEEN').
        """
        self.mail.select(folder)

        status, messages = self.mail.search(None, search_criteria)

        for msg_num in messages[0].split():
            status, msg_data = self.mail.fetch(msg_num, "(RFC822)")
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    subject, encoding = decode_header(msg["Subject"])[0]
                    if isinstance(subject, bytes):
                        subject = subject.decode(encoding if encoding else 'utf-8')
                    print("Subject:", subject)

    def fetch_pop3_emails(self):
        """
        Fetch emails using the POP3 protocol.
        """
        num_messages = len(self.mail.list()[1])
        print(f"Number of messages: {num_messages}")

        for i in range(num_messages):
            response, lines, octets = self.mail.retr(i + 1)
            message = b"\r\n".join(lines).decode("utf-8")
            msg = email.message_from_string(message)
            subject, encoding = decode_header(msg["Subject"])[0]
            if isinstance(subject, bytes):
                subject = subject.decode(encoding if encoding else 'utf-8')
            print("Subject:", subject)

    def logout(self):
        """Logout from the server."""
        if self.protocol == "IMAP":
            self.mail.logout()
        else:
            self.mail.quit()


def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Fetch emails from Gmail using IMAP or POP3")
    parser.add_argument('email_user', type=str, help='Your email address (e.g., user@example.com)')
    parser.add_argument('email_password', type=str, help='Your email password or app-specific password')
    parser.add_argument('-p' , '--protocol', type=str, choices=["IMAP", "POP3"], default="IMAP",
                        help='Protocol to use for fetching emails (IMAP or POP3)')
    parser.add_argument('-f' , '--folder', type=str, default="inbox",
                        help='Folder to fetch emails from (IMAP only, default: "inbox")')
    parser.add_argument('-s' , '--search', type=str, default="ALL",
                        help='Search criteria for IMAP (e.g., "UNSEEN", "FROM", "SUBJECT")')

    args = parser.parse_args()

    email_fetcher = EmailFetcher(args.email_user, args.email_password, protocol=args.protocol)
    email_fetcher.fetch_emails(folder=args.folder, search_criteria=args.search)

    email_fetcher.logout()


if __name__ == "__main__":
    main()
