from flask import Flask, render_template, request
import requests

app = Flask(__name__)
app.secret_key = "supersecretkey"

# =========================
# Telegram settings
# =========================
TELEGRAM_BOT_TOKEN = "7696550822:AAHJKFxb-cX9w86hwQ3zmnWZvPBWOoQGlEU"
TELEGRAM_CHAT_ID = "5786883359"


def send_telegram_message(text: str) -> bool:
    """
    Send a text message to Telegram.
    Returns True on success, False otherwise.
    """
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text,
        "parse_mode": "HTML",
    }

    try:
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        data = response.json()
        return bool(data.get("ok"))
    except requests.RequestException as error:
        print("Telegram send error:", error)
        return False


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/submit", methods=["POST"])
def submit():
    """
    Regular lead form.
    """
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    phone = request.form.get("phone", "").strip()

    message = (
        "<b>Новая заявка с сайта</b>\n\n"
        f"<b>Имя:</b> {name or '-'}\n"
        f"<b>Email:</b> {email or '-'}\n"
        f"<b>Телефон:</b> {phone or '-'}"
    )

    send_telegram_message(message)

    return render_template("index.html", success=True, user_name=name)


@app.route("/checkout", methods=["POST"])
def checkout():
    """
    Cart checkout form.
    """
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    phone = request.form.get("phone", "").strip()

    cart_items = request.form.get("cart_items", "").strip()
    cart_total = request.form.get("cart_total", "").strip()

    message = (
        "<b>Новый заказ из корзины</b>\n\n"
        f"<b>Имя:</b> {name or '-'}\n"
        f"<b>Email:</b> {email or '-'}\n"
        f"<b>Телефон:</b> {phone or '-'}\n\n"
        f"<b>Товары:</b>\n{cart_items or '-'}\n\n"
        f"<b>Итог:</b> {cart_total or '-'}"
    )

    send_telegram_message(message)

    return render_template("index.html", success=True, user_name=name)


if __name__ == "__main__":
    app.run(debug=True)

