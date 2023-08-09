import imaplib
import email
import json
import requests

def get_plain_text(email_message):
    if email_message.is_multipart():
        for part in email_message.walk():
            content_type = part.get_content_type()
            if content_type == "text/plain":
                return part.get_payload(decode=True).decode("utf-8")
    else:
        return email_message.get_payload(decode=True).decode("utf-8")


def count_word_occurrences(word, text):
    count = 0
    words = text.split()
    for w in words:
        if w.lower() == word.lower():
            count += 1
    return count

def get_email_content(username, password, server, port, shop):
    # Connect to the email server
    mail = imaplib.IMAP4_SSL(server, port)

    # Login to the email account
    mail.login(username, password)

    # Select the mailbox (e.g., INBOX)
    mail.select(shop)

    # Search for emails
    result, data = mail.search(None, "ALL")

    # Get the list of email IDs
    email_ids = data[0].split()

    # Fetch the first email
    if email_ids:
        index = len(email_ids)
        email_id = email_ids[index-1]
        result, data = mail.fetch(email_id, "(RFC822)")

        # Parse the email data
        raw_email = data[0][1]
        email_message = email.message_from_bytes(raw_email)

        # Get the email content
        email_subject = email_message["Subject"]
        email_from = email.utils.parseaddr(email_message["From"])[1]
        email_text = get_plain_text(email_message)
        
        monday = count_word_occurrences("monday", email_text)
        tuesday = count_word_occurrences("tuesday", email_text)
        wednesday = count_word_occurrences("wednesday", email_text)
        thursday = count_word_occurrences("thursday", email_text)
        friday = count_word_occurrences("friday", email_text)

        # Create a dictionary with the results
        result_dict = {
            "shop": shop,
            "monday": monday,
            "tuesday": tuesday,
            "wednesday": wednesday,
            "thursday": thursday,
            "friday": friday
        }
        
        # Logout and close the connection
        mail.logout()
        
        return result_dict


# Example usage
username = "Email"
password = "Password"
server = "imap.gmail.com"
port = 993

results = []
results.append(get_email_content(username, password, server, port, "WKFD"))
results.append(get_email_content(username, password, server, port, "WWK"))
results.append(get_email_content(username, password, server, port, "WST"))

# Format the message
message = "Fieldprint report:\n\n"
for result in results:
    shop = result["shop"]
    monday = result["monday"]
    tuesday = result["tuesday"]
    wednesday = result["wednesday"]
    thursday = result["thursday"]
    friday = result["friday"]
    
    message += f"{shop}:\n"
    message += f"    monday: {monday},\n"
    message += f"    tuesday: {tuesday},\n"
    message += f"    wednesday: {wednesday},\n"
    message += f"    thursday: {thursday},\n"
    message += f"    friday: {friday}\n\n"

# Define the Slack webhook URL
webhook_url = "Webhook"

# Send the message to Slack
response = requests.post(webhook_url, json={"text": message})

# Check if the request was successful
if response.status_code == 200:
    print("Message sent to Slack successfully.")
else:
    print("Failed to send the message to Slack. Status Code:", response.status_code)
