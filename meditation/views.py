import random
from django.shortcuts import render
from .models import Album, MusicFile


def index(request):
    # Determine language from GET (or POST) parameter; default is Vietnamese ("vi")
    lang = request.GET.get("lang", "vi")
    if request.method == "POST":
        lang = request.POST.get("lang", lang)

    # Translations dictionary for both languages
    if lang == "en":
        translations = {
            "page_title": "Meditation Timer - Setup",
            "heading": "Insight Meditation Options",
            "label_duration": "Meditation Duration:",
            "option_1": "1 minute (test)",
            "option_15": "15 minutes",
            "option_30": "30 minutes",
            "option_45": "45 minutes",
            "option_60": "60 minutes",
            "label_album": "Choose an Album:",
            "button_start": "Start",
            "checkbox_label": "Meditation Audio Talk",
            "select_duration": "Select Duration",
            "select_album": "Select an Album",
            "no_music_error": "No music files available in the selected album.",
            "session_title": "Meditation Session",
            "session_heading": "Meditation in Progress",
            "btn_pause": "Pause",
            "btn_resume": "Resume",
            "btn_exit": "Exit"
        }
    else:
        translations = {
            "page_title": "Bộ hẹn giờ thiền - Thiết lập",
            "heading": "Thiền Tứ Niệm Xứ",
            "label_duration": "Thời gian thiền:",
            "option_1": "1 phút (kiểm tra)",
            "option_15": "15 phút",
            "option_30": "30 phút",
            "option_45": "45 phút",
            "option_60": "60 phút",
            "label_album": "Lời Pháp:",
            "button_start": "Bắt đầu",
            "checkbox_label": "Sử dụng dẫn thiền",
            "select_duration": "Chọn thời gian thiền",
            "select_album": "Chọn Album",
            "no_music_error": "Không có tệp âm nhạc trong Album đã chọn.",
            "session_title": "Phiên thiền",
            "session_heading": "Đang thiền",
            "btn_pause": "Tạm dừng",
            "btn_resume": "Tiếp tục",
            "btn_exit": "Thoát"
        }

    albums = Album.objects.all()
    context = {
        "albums": albums,
        "lang": lang,
        "translations": translations,
    }

    if request.method == "POST":
        # Determine if audio talk is enabled
        audio_talk = request.POST.get("audio_talk", "off")
        audio_talk_enabled = (audio_talk == "on")

        try:
            meditation_duration = int(request.POST.get("duration"))
        except (TypeError, ValueError):
            meditation_duration = 60  # default to 60 minutes if invalid
        total_seconds = meditation_duration * 60

        if audio_talk_enabled:
            # If user wants audio talk, fetch an album & pick a random music file
            album_id = request.POST.get("album")
            music_files = list(MusicFile.objects.filter(album_id=album_id))
            if not music_files:
                context["error"] = translations["no_music_error"]
                return render(request, "meditation/index.html", context)

            selected_music = random.choice(music_files)
            context = {
                "total_seconds": total_seconds,
                "music_url": selected_music.file.url,
                "music_duration": selected_music.duration,
                "lang": lang,
                "translations": translations,
                "audio_talk_enabled": True,
            }
        else:
            # If user does NOT want audio talk, skip album/music logic
            context = {
                "total_seconds": total_seconds,
                "music_url": "",  # No music file
                "music_duration": 0,  # Zero duration
                "lang": lang,
                "translations": translations,
                "audio_talk_enabled": False,
            }

        return render(request, "meditation/timer.html", context)
    else:
        # GET request - show the selection form
        return render(request, "meditation/index.html", context)
