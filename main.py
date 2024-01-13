import telebot
import requests
from googlesearch import search
import socket
import os
from shutil import make_archive
from git import Repo
from termcolor import colored
from googletrans import Translator
from googletrans.constants import LANGUAGES
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random

pilihan = ['INDONESIA', 'KFC', 'MCD', 'DPR', 'PUAN', 'PAN', 'GRAB', 'GOFOOD', 'TC20', 'GALIRUS', 'CYBER', 'DARK WEB' , 'LIGHT WEB' , 'RED FORUM' , 'MALAYSIA']
pilihan_acak = random.choice(pilihan)

SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
SMTP_USERNAME = 'busines40send@gmail.com'
SMTP_PASSWORD = 'vurvrcdfumhhgszj'

os.system("clear")

menu = """
/gpt = Memainkan AI
/img = Photo Search dengab PIXABAY
/imgun = Photo search dengan UNSPLASH
/search = Penelusuran Google
/email = Mengirim pesan Email
/web = Memeriksa Situs ONLINE/OFFLINE
/ip = Menampillan IP Website
/tr = Translate
/bhs = Menampilkan semua bhs
/code = Menampilkan source code website
"""

logo = """
╭━━━━┳━━━┳╮╱╱╭━━━┳━━━┳━━━┳━━━┳━╮╭━╮╱╱╭━━╮╭━━━┳━━━━╮
┃╭╮╭╮┃╭━━┫┃╱╱┃╭━━┫╭━╮┃╭━╮┃╭━╮┃┃╰╯┃┃╱╱┃╭╮┃┃╭━╮┃╭╮╭╮┃
╰╯┃┃╰┫╰━━┫┃╱╱┃╰━━┫┃╱╰┫╰━╯┃┃╱┃┃╭╮╭╮┃╱╱┃╰╯╰┫┃╱┃┣╯┃┃╰╯
╱╱┃┃╱┃╭━━┫┃╱╭┫╭━━┫┃╭━┫╭╮╭┫╰━╯┃┃┃┃┃┣━━┫╭━╮┃┃╱┃┃╱┃┃
╱╱┃┃╱┃╰━━┫╰━╯┃╰━━┫╰┻━┃┃┃╰┫╭━╮┃┃┃┃┃┣━━┫╰━╯┃╰━╯┃╱┃┃
╱╱╰╯╱╰━━━┻━━━┻━━━┻━━━┻╯╰━┻╯╱╰┻╯╰╯╰╯╱╱╰━━━┻━━━╯╱╰╯
AUTHOR-DCM.X-505
"""

LANGAPI_API_ENDPOINT = "https://langapi.cyclic.app/api/openai"
PIXABAY_API_KEY = "41321022-6206229bc910e3e60741aa58a"
UNSPLASH_ACCESS_KEY = "E30XjkWr471P6AMbGube6txFD5so4oU6g-Zl2d_7gxU"
translator = Translator()

bot = telebot.TeleBot("6918238103:AAEWDRkGoi0ucwLBSQJsJn_jDcHyrekm_CE")

print(colored(f"{logo}","blue"))
print(colored("Bot Telegram Sudah Berjalan","yellow"))

@bot.message_handler(commands=["menu"])
def menu(message):
    bot.send_message(message.chat.id, f"""
/gpt = Memainkan AI
/img = Photo Search dengab PIXABAY
/imgun = Photo search dengan UNSPLASH
/search = Penelusuran Google
/email = Mengirim pesan Email
/web = Memeriksa Situs ONLINE/OFFLINE
/ip = Menampillan IP Website
/tr = Translate
/bhs = Menampilkan semua bhs
/code = Menampilkan source code website""")

@bot.message_handler(commands=["start"])
def handle_start(message):
    bot.send_message(message.chat.id, "Halo! Selamat datang di bot Telegram dcm.")

@bot.message_handler(commands=["img"])
def handle_pixabay_image_search(message):
    query = message.text.split(" ", 1)[1]
    image_url = get_pixabay_image(query)
    send_image(message.chat.id, image_url, query)

@bot.message_handler(commands=["imgun"])
def handle_unsplash_image_search(message):
    query = message.text.split(" ", 1)[1]
    image_url = get_unsplash_image(query)
    send_image(message.chat.id, image_url, query)

@bot.message_handler(commands=["search"])
def handle_google_search(message):
    query = message.text.split(" ", 1)[1]
    max_results = 50
    search_results = perform_google_search(query, max_results)
    send_search_results(message.chat.id, search_results, query)

@bot.message_handler(commands=['web'])
def check_website(message):
    url = message.text.split(maxsplit=1)[1] if len(message.text.split()) > 1 else None

    if not url:
        bot.reply_to(message, "Silakan masukkan URL.")
        return

    try:
        response = requests.get(url)
        if response.status_code == 200:
            bot.reply_to(message, "Website ONLINE")
        else:
            bot.reply_to(message, f"Website OFFLINE ({response.status_code} - {response.reason})")
    except requests.RequestException as e:
        bot.reply_to(message, f"Website OFFLINE (Error: {str(e)})")

@bot.message_handler(commands=['code'])
def get_website_code(message):
    url = message.text.split(maxsplit=1)[1] if len(message.text.split()) > 1 else None

    if not url:
        bot.reply_to(message, "Silakan masukkan URL.")
        return

    try:
        response = requests.get(url)
        if response.status_code == 200:
            source_code = response.text[:10000000]  
            bot.reply_to(message, f"Source Code dari {url}:\n\n{source_code}")
        else:
            bot.reply_to(message, f"Tidak dapat mengambil source code. Website OFFLINE ({response.status_code} - {response.reason})")
    except requests.RequestException as e:
        bot.reply_to(message, f"Tidak dapat mengambil source code. Website OFFLINE (Error: {str(e)})")


@bot.message_handler(commands=['id'])
def show_id(message):
    chat_id = message.chat.id

    user_id = message.from_user.id
    chat_type = message.chat.type

    if chat_type == 'private':
        bot.reply_to(message, f"ID Anda: {user_id}")
    else:
        bot.reply_to(message, f"ID Obrolan/Grup: {chat_id}")

@bot.message_handler(commands=['publik'])
def publish_bot(message):
    chat_id = message.chat.id

    bot.reply_to(message, "Bot telah dipublikasikan!\n"
                          f"Akses bot di: [Tautan Bot](https://t.me/{bot.get_me().username})")

@bot.message_handler(commands=["email"])
def handle_email_command(message):
    try:
        command_parts = message.text.split(" ", 2)
        if len(command_parts) < 3:
            raise ValueError("Please provide destination email and the message.")

        to_email = command_parts[1]
        subject = pilihan_acak
        body = command_parts[2]

        email_message = MIMEMultipart()
        email_message['From'] = f'{pilihan_acak} <{SMTP_USERNAME}>'
        email_message['To'] = to_email
        email_message['Subject'] = subject
        email_message.attach(MIMEText(body, 'plain'))

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.sendmail(SMTP_USERNAME, to_email, email_message.as_string())

        result_message = f"Email Message To {to_email} From {SMTP_USERNAME} For Subject {subject} Success."
    except smtplib.SMTPException as e:
        result_message = f"Error sending email: {e}"
    except ValueError as e:
        result_message = colored(f"Error: {e}", "red")

    bot.send_message(message.chat.id, result_message)

@bot.message_handler(commands=['tr'])
def translate_text(message):
    args = message.text.split()[1:]

    if len(args) < 2:
        bot.reply_to(message, 'Usage: /tr text target_language_code')
        return

    text_to_translate = ' '.join(args[:-1])
    target_language = args[-1]

    source_language = translator.detect(text_to_translate).lang

    translated_text = translator.translate(text_to_translate, dest=target_language).text

    bot.reply_to(message, f'Translated from {source_language.title()} to {target_language}: {translated_text}')


@bot.message_handler(commands=['bhs'])
def list_languages(message):
    languages = ', '.join([f'{code} ({country})' for code, country in LANGUAGES.items()])
    bot.reply_to(message, f'Supported languages: {languages}\n')

@bot.message_handler(commands=["gpt"])
def handle_gpt_request(message):
    query = message.text.split(" ", 1)[1]  

    api_params = {'text': query}
    response = requests.get(LANGAPI_API_ENDPOINT, params=api_params)
    if response.status_code == 200:
        result = response.json().get('result', 'No result received')
        bot.send_message(message.chat.id, f"Hasil dari permintaan GPT:\n\n{result}")
    else:
        bot.send_message(message.chat.id, "Tidak dapat mengambil hasil dari GPT. Coba lagi nanti.")

@bot.message_handler(commands=["imgser"])
def handle_imgser(message):
    try:
        query = message.text.split(" ", 1)[1]
        search_results = perform_google_search(query, 10)
        for result in search_results:
            bot.send_photo(message.chat.id, result["thumbnailUrl"])
            os.remove(image_path)
    except Exception as e:
        bot.send_message(message.chat.id, "Format perintah salah atau terjadi kesalahan.")

@bot.message_handler(commands=["kali"])
def handle_multiply(message):
    perform_calculation(message, "kali")

@bot.message_handler(commands=["mediafire"])
def handle_mediafire_link(message):
    try:
        link = message.text.split(" ", 1)[1]

        direct_download_link = get_mediafire_direct_link(link)

        file_path = download_file(direct_download_link)

        with open(file_path, 'rb') as file:
            bot.send_document(message.chat.id, file)

        os.remove(file_path)

    except Exception as e:
        bot.send_message(message.chat.id, "Format perintah salah atau terjadi kesalahan.")

def get_mediafire_direct_link(mediafire_link):
    response = requests.get(f"https://www.mediafire.com/primarymedia/{mediafire_link}/content")
    data = response.json()
    if "mediaUrl" in data:
        return data["mediaUrl"]
    return None

def download_file(url):
    response = requests.get(url)
    file_path = "./downloaded_file"
    with open(file_path, 'wb') as file:
        file.write(response.content)
    return file_path

@bot.message_handler(commands=["tambah"])
def handle_add(message):
    perform_calculation(message, "tambah")

@bot.message_handler(commands=["bagi"])
def handle_divide(message):
    perform_calculation(message, "bagi")

@bot.message_handler(commands=["kali*"])
def handle_multiply_star(message):
    perform_calculation(message, "kali")

@bot.message_handler(commands=["tambah+"])
def handle_add_plus(message):
    perform_calculation(message, "tambah")

@bot.message_handler(commands=["bagi/"])
def handle_divide_slash(message):
    perform_calculation(message, "bagi")

@bot.message_handler(commands=["kecepatan"])
def handle_speed(message):
    try:
        speed, time = map(float, message.text.split()[1:3])
        result = speed / time
        bot.send_message(message.chat.id, f"Kecepatan: {result} km/jam")
    except Exception as e:
        bot.send_message(message.chat.id, "Format perintah salah atau terjadi kesalahan.")

@bot.message_handler(commands=["ip"])
def handle_domain_to_ip(message):
    try:
        domain = message.text.split(" ", 1)[1]
        ip_address = socket.gethostbyname(domain)
        bot.send_message(message.chat.id, f"IP dari {domain}: {ip_address}")
    except Exception as e:
        bot.send_message(message.chat.id, "Format perintah salah atau terjadi kesalahan.")

@bot.message_handler(commands=["git"])
def handle_git_clone(message):
    try:
        repo_link = message.text.split(" ", 1)[1]
        download_path = f"./{repo_link.split('/')[-1]}"

        Repo.clone_from(repo_link, download_path)

        archive_path = make_archive(download_path, 'zip', download_path)

        with open(archive_path, 'rb') as archive:
            bot.send_document(message.chat.id, archive)

        os.remove(archive_path)
        shutil.rmtree(download_path)
        os.remove(archive)
        os.remove(download_path)

    except Exception as e:
        bot.send_message(message.chat.id, "Format perintah salah atau terjadi kesalahan.")

def get_pixabay_image(query):
    pixabay_url = f"https://pixabay.com/api/?key={PIXABAY_API_KEY}&q={query}&image_type=photo"
    response = requests.get(pixabay_url)
    data = response.json()
    if data["totalHits"] > 0:
        return data["hits"][0]["webformatURL"]
    return None

def get_unsplash_image(query):
    unsplash_url = f"https://api.unsplash.com/photos/random?query={query}&client_id={UNSPLASH_ACCESS_KEY}"
    response = requests.get(unsplash_url)
    data = response.json()
    if "urls" in data:
        return data["urls"]["regular"]
    return None

def perform_google_search(query, max_results):
    search_results = []
    for result in search(query, num=max_results, stop=max_results, pause=2):
        search_results.append(result)
    return search_results

def send_image(chat_id, image_url, query):
    if image_url:
        bot.send_photo(chat_id, image_url, caption=f"✅Hasil: {query}")
    else:
        bot.send_message(chat_id, "Tidak ada hasil gambar untuk query ini.")

def send_search_results(chat_id, search_results, query):
    if search_results:
        result_text = "\n".join([f"{index + 1}. {result}" for index, result in enumerate(search_results)])
        bot.send_message(chat_id, f"Hasil pencarian untuk '{query}':\n{result_text}")
    else:
        bot.send_message(chat_id, f"Tidak ada hasil pencarian untuk '{query}'.")

def perform_calculation(message, operation):
    try:
        numbers = list(map(float, message.text.split()[2:]))
        if operation == "kali":
            result = 1
            for number in numbers:
                result *= number
            bot.send_message(message.chat.id, f"Hasil perkalian: {result}")
        elif operation == "tambah":
            result = sum(numbers)
            bot.send_message(message.chat.id, f"Hasil penambahan: {result}")
        elif operation == "bagi":
            result = numbers[0] / numbers[1]
            bot.send_message(message.chat.id, f"Hasil pembagian: {result}")
    except Exception as e:
        bot.send_message(message.chat.id, "Format perintah salah atau terjadi kesalahan.")

@bot.message_handler(content_types=["text"])
def handle_text(message):
    bot.send_message(message.chat.id, f"Saya tidak mengerti maksud anda silakan /menu untuk melihat menu yg ada: {message.text}")

bot.polling()
