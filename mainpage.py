import os
import tkinter as tk
from dotenv import load_dotenv
from tkinter import messagebox
import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText

# ---------- EMAIL SENDING FUNCTION ----------
load_dotenv()

def send_email(to_email, subject, body):
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    sender_email = os.getenv('SENDER_EMAIL')
    sender_password = os.getenv('SENDER_PASSWORD')  # Use your Gmail App Password!

    msg = MIMEText(body, 'plain')
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = to_email

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)  # cleaner than sendmail
        server.quit()
        return True
    except Exception as e:
        messagebox.showerror("Email Error", f"Failed to send email:\n{e}")
        return False


# ---------- PRICE CHECK FUNCTION ----------
def check_price():
    url = url_entry.get().strip()
    try:
        target_price = float(price_entry.get().strip())
    except ValueError:
        messagebox.showerror("Input Error", "Please enter a valid number for target price.")
        return

    name = name_entry.get().strip()
    email = email_entry.get().strip()

    if not url or not name or not email:
        messagebox.showerror("Input Error", "Please fill in all fields.")
        return

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Accept-Language": "en-US,en;q=0.9"
    }

    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')

        title_tag = soup.find(id='productTitle')
        price_tag = soup.find('span', {'class': 'a-price-whole'})

        if not title_tag or not price_tag:
            messagebox.showerror("Scraping Error", "Could not find product title or price. Please check the URL or update selectors.")
            return

        title = title_tag.get_text(strip=True)
        price_text = price_tag.get_text().replace(',', '')
        current_price = float(price_text)

        result_text = f"Product: {title}\nCurrent Price: ₹{current_price}"
        result_label.config(text=result_text)

        if target_price <= current_price:
            subject = f"Price Alert: {title} is now ₹{current_price}"
            body = (f"Hi {name},\n\nThe price of the product you were tracking has dropped to ₹{current_price}.\n"
                    f"Product link: {url}\n\nHappy shopping!\nYour Price Tracker")
            if send_email(email, subject, body):
                messagebox.showinfo("Success", "Price is within your target! Notification email sent.")
        else:
            messagebox.showinfo("Price Check", "Price is still higher than your target.")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred:\n{e}")

# ---------- GUI SETUP ----------
root = tk.Tk()
root.title("Product Price Tracker")
root.geometry("600x600")
root.configure(bg="#e1f5fe")  # Same light blue theme
root.resizable(False, False)

# Center the window on screen
window_width = 600
window_height = 600
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = int((screen_width / 2) - (window_width / 2))
y = int((screen_height / 2) - (window_height / 2))
root.geometry(f"{window_width}x{window_height}+{x}+{y}")

# ---------- UI ELEMENTS ----------
tk.Label(root, text="Track Your Product Price", font=("Helvetica", 20, "bold"), bg="#e1f5fe", fg="#0277bd").pack(pady=20)

# URL
tk.Label(root, text="Product URL:", font=("Helvetica", 12), bg="#e1f5fe").pack(pady=(10, 0))
url_entry = tk.Entry(root, width=60, font=("Helvetica", 11))
url_entry.pack(pady=5)

# Target Price
tk.Label(root, text="Target Maximum Price (₹):", font=("Helvetica", 12), bg="#e1f5fe").pack(pady=(15, 0))
price_entry = tk.Entry(root, width=30, font=("Helvetica", 11))
price_entry.pack(pady=5)

# Name
tk.Label(root, text="Your Name:", font=("Helvetica", 12), bg="#e1f5fe").pack(pady=(15, 0))
name_entry = tk.Entry(root, width=40, font=("Helvetica", 11))
name_entry.pack(pady=5)

# Email
tk.Label(root, text="Your Email:", font=("Helvetica", 12), bg="#e1f5fe").pack(pady=(15, 0))
email_entry = tk.Entry(root, width=40, font=("Helvetica", 11))
email_entry.pack(pady=5)

# Button
check_button = tk.Button(
    root,
    text="Check Price & Notify",
    font=("Helvetica", 14),
    bg="#0288d1",
    fg="white",
    activebackground="#0277bd",
    padx=10,
    pady=5,
    command=check_price
)
check_button.pack(pady=30)

# Result
result_label = tk.Label(root, text="", font=("Helvetica", 12), bg="#e1f5fe", fg="#333")
result_label.pack(pady=10)

root.mainloop()
