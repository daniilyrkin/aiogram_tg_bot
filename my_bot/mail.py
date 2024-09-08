import random
import string
import requests

# Олноразовая почта. Та же что и в боте, просто работа через консоль

API = 'https://www.1secmail.com/api/v1/'
domain_list = [
    "1secmail.com",
    "1secmail.org",
    "1secmail.net",
    "wwjmp.com",
    "esiix.com",
    "xojxe.com",
    "yoggm.com"]


def generate_username():
    domain = random.choice(domain_list)
    name = string.ascii_lowercase + string.digits
    username = ''.join(random.choice(name) for i in range(10))
    mail = f'{username}@{domain}'
    return mail


def check_mail(mail=''):
    text_mail = ''
    req_mail = f'{API}?action=getMessages&login={mail.split("@")[0]}&domain={mail.split("@")[1]}'
    data = requests.get(req_mail).json()
    length = len(data)
    if length == 0:
        print('[-] Нет сообщений')
    else:
        id_list = []
        for i in data:
            for k, v in i.items():
                if k == 'id':
                    id_list.append(v)
        print('[+] У вас есть сообщения')
        for i in id_list:
            read_msg = f'{API}?action=readMessage&login={mail.split("@")[0]}&domain={mail.split("@")[1]}&id={i}'
            r = requests.get(read_msg).json()
            sender = r['from']
            subject = r['subject']
            date = r['date']
            content = r['textBody']
            text_mail += f'Отправитель: {sender}\nДата: {date}\nТема: {subject}\nСодержание: {content}'
        print(text_mail)


def main():
    q = int(input('Введите количество почт: '))
    if q == 1:
        mail = generate_username()
        mail_req = f'{API}?login={mail.split("@")[0]}&domain={mail.split("@")[1]}'
        response = requests.get(mail_req)
        print(f'Ваша временная почта: {mail}')
    elif q == 0:
        q = int(input('Введите количество почту: '))
        check_mail(q)


if __name__ == '__main__':
    main()
