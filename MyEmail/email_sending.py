import os
import ssl
import yaml
import smtplib

from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart


def _read_settings():
    """
    Read the sender email settings from settings.yml
    :return: a dictionary
    """
    dir_name = os.path.dirname(__file__)
    filepath = os.path.join(dir_name, "settings.yml")

    try:
        with open(filepath) as fin:
            settings = yaml.load(fin, Loader=yaml.FullLoader)

    except Exception as e:
        print(e)
        raise e

    return settings


def _create_notification_template():
    """
    Create the email template
    :return: a message object
    """
    subject = "Notification of Comparison Result | Testing"

    text_body = "Hello,\n\n" \
                "We have sent you this email in response to your request to " \
                "find the unauthorized software on your client.\n\n" \
                "For details, please refer to the attached csv file."

    _message = MIMEMultipart("mixed")
    _message["From"] = _config["sender"]
    _message["Subject"] = subject

    text_file = "./MyEmail/email_template.html"
    with open(text_file, "r") as body:
        html_text = body.read()

    msgAlternative = MIMEMultipart('alternative')
    _message.attach(msgAlternative)
    # msgText = MIMEText(text_body, "plain")
    msgText = MIMEText(html_text, "html")
    msgAlternative.attach(msgText)

    with open("./MyEmail/image-5.png", "rb") as img:
        msgImage = MIMEImage(img.read())

    # Define the image's ID as referenced above
    msgImage.add_header('Content-ID', '<image-5.png>')
    _message.attach(msgImage)

    with open("./MyEmail/image-4.png", "rb") as img:
        msgImage = MIMEImage(img.read())

    # Define the image's ID as referenced above
    msgImage.add_header('Content-ID', '<image-4.png>')
    _message.attach(msgImage)

    with open("./MyEmail/image-3.png", "rb") as img:
        msgImage = MIMEImage(img.read())

    # Define the image's ID as referenced above
    msgImage.add_header('Content-ID', '<image-3.png>')
    _message.attach(msgImage)

    with open("./MyEmail/image-2.png", "rb") as img:
        msgImage = MIMEImage(img.read())

    # Define the image's ID as referenced above
    msgImage.add_header('Content-ID', '<image-2.png>')
    _message.attach(msgImage)

    with open("./MyEmail/image-1.png", "rb") as img:
        msgImage = MIMEImage(img.read())

    # Define the image's ID as referenced above
    msgImage.add_header('Content-ID', '<image-1.png>')
    _message.attach(msgImage)

    return _message


def send_email(receiver, csv_name):
    """
    Send the html style email to the receiver
    :param receiver: the receiver email
    :param csv_name: the csv file to send
    :return: nothing
    """
    relative_path = "./"
    filename = relative_path + csv_name

    # Open csv file in binary mode
    try:
        with open(filename, "rb") as attachment:
            # Add file as application/octet-stream
            payload = MIMEBase("application", "octet-stream")
            payload.set_payload(attachment.read())

    except FileNotFoundError:
        print("No such file or directory: " + csv_name)
        return

    # Encode file in ASCII characters to send by email
    encoders.encode_base64(payload)

    # Add header as key/value pair to attachment part
    payload.add_header(
        "Content-Disposition",
        f"attachment; filename={csv_name}",
    )

    # Add attachment to message
    message["To"] = receiver
    message.attach(payload)

    # Convert message to string
    final_text = message.as_string()

    try:
        # Create a secure SSL context
        context = ssl.create_default_context()

        with smtplib.SMTP_SSL(_config["smtp"], _config["port"], context=context) as server:
            server.login(_config["sender"], _config["pwd"])
            server.sendmail(_config["sender"], receiver, final_text)

    except Exception as e:
        print(e)

    finally:
        for payload in message.get_payload():
            if payload.get_content_type() == "application/octet-stream":
                message.get_payload().remove(payload)


_config = _read_settings()
message = _create_notification_template()
