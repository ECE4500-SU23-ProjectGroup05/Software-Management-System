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


def _create_notification_template(text=None):
    """
    Create the email template with given text
    :param text the specialized html text
    :return: a message object
    """
    subject = "Notification of Comparison Result | Testing"

    text_body = "Hello,\n\n" \
                "We have sent you this email in response to your request to " \
                "find the unauthorized software on your client.\n\n" \
                "For details, please refer to the attached csv file."

    html_text = ""

    html_text_default = """\
  <div style="font-size: 14px; line-height: 140%; text-align: left; word-wrap: break-word;">
<p style="font-size: 14px; line-height: 140%;"><span style="font-size: 18px; line-height: 25.2px; color: #666666;">Hello,</span></p>
<p style="font-size: 14px; line-height: 140%;"> <br></p>
<p style="font-size: 14px; line-height: 140%;"><span style="font-size: 18px; line-height: 25.2px; color: #666666;">We have sent you this email in response to your request to find the unauthorized software on your client.</span></p>
<p style="font-size: 14px; line-height: 140%;"> <br></p>
<p style="font-size: 14px; line-height: 140%;"><span style="font-size: 18px; line-height: 25.2px; color: #666666;">For details, please refer to the attached csv file.</span></p>
  </div>
  
    """

    _message = MIMEMultipart("mixed")
    _message["From"] = _config["sender"]
    _message["Subject"] = subject

    text_file = "./MyEmail/email_template_op.html"
    with open(text_file, "r") as body:
        html_text += body.read()

    html_text += html_text_default if text is None else text

    text_file = "./MyEmail/email_template_ed.html"
    with open(text_file, "r") as body:
        html_text += body.read()

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


def send_email(receiver, csv_name, data=None):
    """
    Send the html style email to the receiver
    :param receiver: the receiver email
    :param csv_name: the csv file to send
    :param data: the specialized data in the dict form of
                 {
                    "unauthorized": value,
                    "key": value
                 }
    :return: nothing
    """
    relative_path = "./"
    filename = relative_path + csv_name

    if data is None:
        _message = message
    else:
        _message = _create_specialized_email(csv_name, data)

    # Open csv file in binary mode
    try:
        with open(filename, "rb") as attachment:
            # Add file as application/octet-stream
            payload = MIMEBase("application", "octet-stream")
            payload.set_payload(attachment.read())

    except FileNotFoundError:
        print("No such file or directory: " + csv_name)
        print("NOTICE: Email sending is aborted.")
        return

    # Encode file in ASCII characters to send by email
    encoders.encode_base64(payload)

    # Add header as key/value pair to attachment part
    payload.add_header(
        "Content-Disposition",
        f"attachment; filename={csv_name}",
    )

    # Add attachment to message
    _message["To"] = receiver
    _message.attach(payload)

    # Convert message to string
    final_text = _message.as_string()

    try:
        # Create a secure SSL context
        context = ssl.create_default_context()

        with smtplib.SMTP_SSL(_config["smtp"], _config["port"], context=context) as server:
            server.login(_config["sender"], _config["pwd"])
            server.sendmail(_config["sender"], receiver, final_text)

        print(f"NOTICE: A notification email has been sent to the user: {receiver}.")

    except Exception as e:
        print(e)
        print("NOTICE: Email sending is aborted.")

    finally:
        for payload in _message.get_payload():
            if payload.get_content_type() == "application/octet-stream":
                _message.get_payload().remove(payload)


def _create_specialized_email(csv_name, data):
    """
    Create the specialized html style email
    :param csv_name: the csv file to send
    :param data: the specialized data in the dict form of
                 {
                    "unauthorized": value,
                    "key": value
                 }
    :return: nothing
    """
    ip_addr = csv_name[:-4].replace('~', '/')
    specialized_text = f"""\
  <div style="font-size: 14px; line-height: 140%; text-align: left; word-wrap: break-word;">
<p style="font-size: 14px; line-height: 140%;"><span style="font-size: 18px; line-height: 25.2px; color: #666666;">Hello,</span></p>
<p style="font-size: 14px; line-height: 140%;"> <br></p>
<p style="font-size: 14px; line-height: 140%;"><span style="font-size: 18px; line-height: 25.2px; color: #666666;">We have sent you this email in response to your request to find the unauthorized software on your client.</span></p>
<p style="font-size: 14px; line-height: 140%;"> <br></p>
<p style="font-size: 14px; line-height: 140%;"><span style="font-size: 18px; line-height: 25.2px; color: #666666;">According to the black/white list you provided, we detect that the client(s) on {ip_addr} has installed {data["unauthorized"]} unauthorized apps.</span></p>
<p style="font-size: 14px; line-height: 140%;"> <br></p>
<p style="font-size: 14px; line-height: 140%;"><span style="font-size: 18px; line-height: 25.2px; color: #666666;">For details, please refer to the attached csv file.</span></p>
  </div>

    """
    return _create_notification_template(specialized_text)


_config = _read_settings()
message = _create_notification_template()
