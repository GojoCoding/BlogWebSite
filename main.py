from flask import Flask, render_template, request
import smtplib
import requests

MY_EMAIL = "jimmm776@gmail.com"
MY_PASSWORD = "gxuvodshpzaiquzm"

# USE YOUR OWN npoint LINK! ADD AN IMAGE URL FOR YOUR POST. 👇
posts = requests.get("https://api.npoint.io/52cf2c6706c6cbf4e2a6").json()

app = Flask(__name__)


@app.route('/')
def get_all_posts():
    return render_template("index.html", all_posts=posts)


@app.route("/about")
def about():
    return render_template("about.html")


@app.get("/contact")
def contact():
    return render_template("contact.html")


@app.post("/contact")
def form_retrieve():
    data = request.form
    send_email(data["name"], data["email"], data["number"], data["message"])
    return render_template("contact.html", web_state=request.method)


def send_email(name, email, number, message):
    email_message = f"Subject: New Message\n\nName: {name}\nEmail: {email}\nPhone: {number}\nMessage: {message}"
    with smtplib.SMTP("smtp.gmail.com", 587) as connection:
        connection.starttls()
        connection.login(MY_EMAIL, MY_PASSWORD)
        connection.sendmail(MY_EMAIL, [email], email_message)

# SOLUTION WAY -- All in one function, use .route decorator and if statement within function
# @app.route("/contact", methods=["GET", "POST"])
# def contact():
#     if request.method == "POST":
#         data = request.form
#         print(data["name"])
#         print(data["email"])
#         print(data["phone"])
#         print(data["message"])
#         return "<h1>Successfully sent your message</h1>"
#     return render_template("contact.html")


@app.route("/post/<int:index>")
def show_post(index):
    requested_post = None
    for blog_post in posts:
        if blog_post["id"] == index:
            requested_post = blog_post
    return render_template("post.html", post=requested_post)


if __name__ == "__main__":
    app.run(debug=True, port=5001)
