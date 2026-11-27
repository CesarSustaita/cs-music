from pathlib import Path
import yt_dlp

DOWNLOAD_FILES = Path("descargas")

def get_fileName_available(folder: Path, name: str, extension:str) -> Path:
    route = folder / f"{name}.{extension}"
    cont = 1

    while route.exists():
        route = folder / f"{name} ({cont}).{extension}"
        cont += 1
    return route

def link_downloader(url: str, extension_format: str = "m4a") -> dict:
    DOWNLOAD_FILES.mkdir(parents=True, exist_ok=True)

    try:
        with yt_dlp.YoutubeDL({"noplaylist": True, "quiet": True}) as ydl:
            info = ydl.extract_info(url, download=False)

        title = info.get("title", "Audio Download")
        title_clean = "".join(c for c in title if c not in r'\/:*?"<>|').strip()

        main_route = get_fileName_available(
            DOWNLOAD_FILES, title_clean, extension_format
        )

        ydl_set = {
                "format": "bestaudio/best",
                "outtmpl": str(main_route.with_suffix("")) + ".%(ext)s",
                "noplaylist": True,
                "postprocessors": [
                        {
                            "key": "FFmpegExtractAudio",
                            "preferredcodec": extension_format,
                            "preferredquality": "0",
                        }
                ],
            }

        with yt_dlp.YoutubeDL(ydl_set) as ydl:
            ydl.extract_info(url, download=True)

        return{
            "state": "Completado",
            "title": title_clean,
            "format": extension_format,
            "file": str(main_route),
        }
    except Exception as error:
        return{
            "state": "error",
            "details": str(error),
        }