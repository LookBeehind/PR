# Dicol Oliviu
### TI-211 FR
### Lab 5 - Aplicație de tip client Email
### --------------------------------------------------------------------------------------------------------------------
## To run the app, you need to provide the arguments:
## Send an E-mail:
### The options:
1. From
2. To
3. Subject
4. Body
5. Attachment
6. Password

### Please fill the required fields and run the code:
`python send_mail.py "your_email" "recipient_email" "Subject Text" "Body of the email" "un_fisier.txt" "your_password"`

## Fetch the E-mails:
## The options:
1. User
2. Password
3. -p: Protocol (IMAP or POP3) to use for fetching emails (default: IMAP)
4. -f: Folder to fetch emails from (default: "inbox")
5. -s: Search criteria for fetching emails (default: "ALL")

### Please fill the required fields and run the code:
#### Default options:
`python fetch_emails.py "your_email" "your_password"`

#### Set specific criteria:
##### Example filter
`python fetch_emails.py "your_email" "your_password" -p IMAP -f INBOX -s "FROM 'no-reply@accounts.google.com'"`

#### Since the POP3 does not have the flexibility to filter e-mails server-side, we can just run:
`python fetch_emails.py "your_email" "your_password" -p POP3`

### --------------------------------------------------------------------------------------------------------------------
## Examples 
### Example Folders:
1. **INBOX**: The folder containing incoming messages.
2. **Sent**: The folder where sent messages are stored.
3. **Drafts**: The folder for messages that are saved as drafts.
4. **Spam**: The folder containing spam or junk emails.
5. **Trash**: The folder where deleted emails are stored.
6. **All Mail**: The folder that contains all emails, including archived messages.
7. **Starred**: The folder for messages that you’ve marked as important or starred.
8. **Important**: The folder where Gmail stores emails marked as important.

### Example Search Criteria:
1. **ALL**: Selects all messages in the folder.
2. **UNSEEN**: Selects messages that have not been read.
3. **SEEN**: Selects messages that have been read.
4. **ANSWERED**: Selects messages that have been replied to.
5. **FROM**: Selects messages from a specific sender (e.g., `"FROM 'sender@example.com'"`).
6. **TO**: Selects messages sent to a specific recipient.
7. **SUBJECT**: Selects messages containing specific text in the subject line.
8. **BODY**: Selects messages containing specific text in the body.
9. **SINCE**: Selects messages sent since a specific date.
10. **BEFORE**: Selects messages sent before a specific date.
11. **ON**: Selects messages sent on a specific date.
12. **LARGER**: Selects messages larger than a specific size (e.g., `LARGER 50000` for messages larger than 50 KB).
13. **SMALLER**: Selects messages smaller than a specific size.
