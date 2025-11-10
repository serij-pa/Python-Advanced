"""
В этом файле будут Celery-задачи
"""
import sqlite3
import zipfile
from celery import Celery
from celery.schedules import crontab
from app import app
from image import blur_image
from mail import send_email

celery = Celery(app.name,
                broker='redis://localhost:6379/0',
                backend='redis://localhost:6379/0',
                broker_connection_retry_on_startup=True,)

list_emails = ["sergey.palagin82@gmail.com", "s.n.palagin@yandex.ru"]

@celery.task
def process_image(image_name):
    new_image_name = blur_image(image_name)
    return f"{new_image_name}"

@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(hour="17", minute="30", day_of_week="wed"),
        sending_mails.s(),
        name="отправка писем"
    )
    return "Письмо отправлено"

@celery.task
def sending_mails():
    with sqlite3.connect("my_email.db") as conn:
        cursor = conn.cursor()
        result = cursor.execute('SELECT email FROM emails').fetchall()
        for res in result:
            send_email(order_id="выполнение задач",
                       receiver=res[0],
                       filename="blur_photos.zip")
        return "sending_mails"


@celery.task
def create_zip_send_email(group_id):
    result_zip = celery.GroupResult.restore(group_id)
    print(result_zip)
    zip_file_name = "blur_photos.zip"
    zip_object = zipfile.ZipFile(zip_file_name, 'w')
    for file in result_zip:
        zip_object.write(file.info, compress_type=zipfile.ZIP_DEFLATED)
    zip_object.close()
    with sqlite3.connect('my_email.db') as conn:
        cursor = conn.cursor()
        result_email = cursor.execute('SELECT email FROM emails').fetchall()
        for email in result_email:
            send_email(
                order_id='Выполнение периодических задач',
                receiver=email[0],
                filename='blur_photos.zip'
            )