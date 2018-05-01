import logging
import smtplib
from email.header import Header
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import List

from src.notifications.template import build_template, get_pdf_attachment, PdfFile
from src.setup import get_setup

SES_PORT = 587


def __build_msg_html(
        sender: str,
        receiver: List[str],
        subject: str,
        txt: str,
        html: str,
        attachments: List[PdfFile],
) -> MIMEMultipart:
    msg_root = MIMEMultipart('mixed')
    msg_root['Subject'] = Header(subject, 'utf-8')
    msg_root['From'] = sender
    msg_root['To'] = ', '.join(receiver)
    msg = MIMEMultipart('alternative')

    msg.attach(MIMEText(txt, 'plain', 'utf-8'))
    if html is not None:
        msg.attach(MIMEText(html, 'html', 'utf-8'))
    if attachments:
        for attachment in attachments:
            msg_root.attach(MIMEApplication(
                attachment.data,
                Content_Disposition=f'attachment; filename="{attachment.filename}"',
                Name=attachment.filename,
            ))
    msg_root.attach(msg)
    return msg_root


def send(
        sender: str,
        receiver: str,
        subject_template: str,
        text_template: str,
        html_template: str,
        pdfs: List[dict],
        template_data: dict,
) -> None:
    body_html = build_template(html_template, template_data)
    body_text = build_template(text_template, template_data)
    subject = build_template(subject_template, template_data)
    attachments: List[PdfFile] = []
    for pdf in pdfs:
        attachments.append(get_pdf_attachment(pdf.get('template'), template_data, pdf.get('filename')))
    __send_to_ses(sender, receiver, subject, body_text, body_html, attachments)


def __send_to_ses(
        sender: str,
        receiver: str,
        subject: str,
        txt: str,
        html: str,
        attachments: List[PdfFile],
) -> None:
    if get_setup().is_debug:
        logging.info('Not sending real emails in debug mode (activate with DEBUG=true environment variable)')
        logging.info('sender:       %s', sender)
        logging.info('receiver:     %s', receiver)
        logging.info('subject:      %s', subject)
        logging.info('txt:          %s', txt)
        logging.info('html:         %s', html)
        logging.info('attachments:  %s', "\n".join([str(a) for a in attachments]))
        logging.info('done logging')
        return

    logging.info(f'Sending email with subject {subject!r} to {receiver!r} from {sender!r}')
    try:
        smtp = smtplib.SMTP(f'email-smtp.{get_setup().email_credentials.aws_region}.amazonaws.com', SES_PORT)
        smtp.starttls()
        smtp.login(get_setup().email_credentials.api_key, get_setup().email_credentials.api_secret)
        msg = __build_msg_html(sender, receiver.split(','), subject, txt, html, attachments)
        smtp.sendmail(sender, receiver.split(','), msg.as_string())
        smtp.quit()
        logging.info(f'Sent email with subject {subject!r} to {receiver!r} from {sender!r}')
    except OSError as e:
        logging.error(f'Error {e} occurred during sending email with subject {subject!r} to {receiver!r} from '
                      f'{sender!r}')
