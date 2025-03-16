import os
from flask import Flask, render_template, request
from flask_mail import Mail, Message
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

app = Flask(__name__)

# Настройки почты
app.config["MAIL_SERVER"] = os.getenv("MAIL_SERVER", "smtp.gmail.com")
app.config["MAIL_PORT"] = int(os.getenv("MAIL_PORT", 587))
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USE_SSL"] = False
app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")
app.config["MAIL_DEFAULT_SENDER"] = app.config["MAIL_USERNAME"]

mail = Mail(app)

# Маршрут для страницы кандидатов
@app.route("/candidates")
def candidates():
    return render_template("candidates.html")

# Маршрут для страницы клиентов
@app.route("/clients")
def clients():
    return render_template("clients.html")

# Обработчик формы кандидата
@app.route("/send_candidate", methods=["POST"])
def send_candidate():
    name = request.form["name"]
    surname = request.form["surname"]
    email = request.form["email"]
    phone = request.form["phone"]
    process = request.form["process"]
    categories = ", ".join(request.form.getlist("category"))
    experience = request.form.get("experience")
    info = request.form["info"]
    
    msg_body = f"""
    Новая заявка от кандидата:
    Имя: {name} {surname}
    Email: {email}
    Телефон: {phone}
    Процесс: {process}
    Категории: {categories}
    Опыт: {experience}
    Доп. информация: {info}
    """
    
    msg = Message("Новая заявка от кандидата", recipients=[app.config["MAIL_USERNAME"]])
    msg.body = msg_body
    
    mail.send(msg)
    return "Форма кандидата отправлена!"

# Маршрут для отправки данных формы клиентов
@app.route("/send_client", methods=["POST"])
def send_client():
    company = request.form["company"]
    email = request.form["email"]
    name = request.form["name"]
    phone = request.form["phone"]
    project = request.form["project"]
    specialists = request.form["specialists"]
    number = request.form["number"]
    info = request.form["info"]
    
    msg_body = f"""
    Новая заявка от компании:
    Компания: {company}
    Контактное лицо: {name}
    Email: {email}
    Телефон: {phone}
    Проект: {project}
    Специалисты: {specialists}, Количество: {number}
    Доп. информация: {info}
    """
    
    msg = Message("Новая заявка от клиента", recipients=[email])
    msg.body = msg_body
    mail.send(msg)
    
    return "Письмо успешно отправлено!"

if __name__ == "__main__":
    app.run(debug=True)
