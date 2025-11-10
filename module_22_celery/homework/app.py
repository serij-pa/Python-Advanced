"""
В этом файле будет ваше Flask-приложение
"""
import os
import sqlite3
import zipfile
#from celery_task import process_image, celery, create_zip_send_email

from flask import Flask, render_template, request, jsonify
from celery import group, chain
from mail import send_email

app = Flask(__name__)
DOWNLOAD_PATH = "./download_files/images"
FILE_EXTENSION = {'png', 'jpg', 'jpeg', 'gif'}
USERS = []

def allowed_file(filename):
    # проверка, а совпадают ли расширения файлов с разрешенными
    allowed = '.' in filename and \
           filename.rsplit('.', 1)[1] in FILE_EXTENSION
    return allowed

app.config['UPLOAD_FOLDER'] = DOWNLOAD_PATH

@app.route("/")
def index():
    return render_template('index.html')


@app.route('/blur', methods=['GET', 'POST'])
def blur():
    if request.method == 'POST':
        # Если директория для хранения файлов не создана, создадим её.
        if not os.path.exists(DOWNLOAD_PATH):
            os.makedirs(DOWNLOAD_PATH)
        # Загрузим файлы картинок на сервер
        images = request.files.getlist('photo')
        file_names = []
        if images:
            for image in images:
                if allowed_file(image.filename):
                    image.save(os.path.join(DOWNLOAD_PATH, image.filename))
                    file_names.append(f"{DOWNLOAD_PATH}/{image.filename}")
            from celery_task import process_image, create_zip_send_email
            task_group = group(process_image.s(img_filename) for img_filename in file_names)
            task_zip_email = create_zip_send_email.s()
            result = chain(task_group | task_zip_email).apply_async()
            #result = task_group.apply_async()
            print(result)
            print(result.id)
            #result.save()

            return render_template(
                'tasks_is_done.html', group_id=result.id)
    return render_template('load_images.html')


@app.route('/status/<string:group_id>')
def get_status(group_id):
    """
    Возвращает информацию о задаче: прогресс (количество обработанных задач) и
    статус (в процессе обработки, обработано).
    """
    from celery_task import celery
    result = celery.GroupResult.restore(group_id)

    if result:
        info = {
            'task_count': len(result),
            'completed': result.completed_count(),
            'message': 'Отправлено письмо с архивом blur_photos.zip',}
        return render_template('tasks_status.html', info=info)
    return f'group_id: {group_id}'


#@app.route('/status', methods=['GET', 'POST'])
#def get_status_post():
#    """
#    Возвращает информацию о задаче: прогресс (количество обработанных задач) и
#    статус (в процессе обработки, обработано).
#    """
#    if request.method == 'POST':
#        group_id = request.form.get('task_id')
#        from celery_task import celery
#        result = celery.GroupResult.restore(group_id)
#        if result:
#            # Если группа с таким ID существует,
#            # возвращаем долю выполненных задач
#            status = result.completed_count() / len(result)
#            if int(status) == 1:
#                # Если все задачи выполнены, можно создать архив с blur-файлами
#                zip_file_name = "blur_photos.zip"
#                zip_object = zipfile.ZipFile(zip_file_name, 'w')
#                for file in result:
#                    zip_object.write(file.info, compress_type=zipfile.ZIP_DEFLATED)
#                zip_object.close()
#            else:
#                return f"Не все задачи еще выполнены"
#            # отправляем письмо и выводим сообщения
#            info = {
#                'task_count': len(result),
#                'completed': result.completed_count(),
#                'message': 'Отправлено письмо с архивом blur_photos.zip',}
#            send_email(group_id, 's.n.palagin@yandex.ru', 'blur_photos.zip')
#            return render_template('tasks_status.html', info=info)
#        return f'group_id: {group_id}'
#    return render_template('input_task_id.html')


@app.route('/subscribe', methods=['GET', 'POST'])
def subscribe():
    """
    Пользователь указывает почту и подписывается на рассылку. Каждую неделю ему
    будет приходить письмо о сервисе на почту.
    """
    if request.method == "POST":
        email = request.form.get('email')
        with sqlite3.connect('my_email.db') as conn:
            cursor = conn.cursor()
            cursor.execute('CREATE TABLE IF NOT EXISTS emails (id INTEGER PRIMARY KEY, email TEXT UNIQUE NOT NULL )')
            try:
                cursor.execute('INSERT INTO emails (email) VALUES (?)', (email, ))
            except sqlite3.IntegrityError as err:
                return render_template('error.html', error=err)
            conn.commit()
        phrase = 'подписались'
        return render_template('successfully.html', phrase=phrase)
    return render_template('input_email.html')


@app.route('/unsubscribe', methods=['GET', 'POST'])
def unsubscribe():
    """
    Пользователь указывает почту и отписывается от рассылки.
    """
    if request.method == "POST":
        email = request.form.get('email')
        with sqlite3.connect('my_email.db') as conn:
            cursor = conn.cursor()
            cursor.execute(f'DELETE FROM emails WHERE email="{email}"')
            conn.commit()
        phrase = 'отписались'
        return render_template('successfully.html', phrase=phrase)
    return render_template('input_email.html')


if __name__ == "__main__":
    app.run(debug=True)