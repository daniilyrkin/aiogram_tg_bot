import yt_dlp
import subprocess
import os
import art


# Тут работал над возможностью скачиватьб музыку с ютуба. Сервер слабоват, поэтому оставил так


def download(url, path):
    ydl_opts = {
        'format': 'bestaudio/webm',
        'extract_audio': True,
        "outtmpl": "music/%(title)s.%(ext)s"
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        names = ydl.extract_info(url, download=True)
        name = names['title']

    src = f"{path}/{name}.webm"
    dst = f"music/{name}.mp3"

    subprocess.run(
        [
            "ffmpeg",
            "-i",
            src,
            "-ar",
            "44100",
            "-ac",
            "2",
            "-b:a",
            "320k",
            dst,
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,)

    print("Converted Successfully")
    os.remove(src)


def main(url):
    path = './music'
    list_url = url.split(' ')
    if not os.path.exists(path):
        os.makedirs(path)
    for url in list_url:
        download(url=url, path=path)


if __name__ == '__main__':
    art.tprint('PYTUBE', space=6)
    main()
