import random
from django.shortcuts import render
from .models import Album, MusicFile


def index(request):
    lang = request.GET.get("lang", "vi")
    if request.method == "POST":
        lang = request.POST.get("lang", lang)

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
            "album_option_none": "Not use",
            "select_duration": "Select Duration",
            "select_album": "Select an Album",
            "button_start": "Start",
            "no_music_error": "No music files available in the selected album.",
            "session_title": "Meditation Session",
            "btn_pause": "Pause",
            "btn_resume": "Resume",
            "btn_exit": "Exit",
            "start_session_prompt": "Tap to Start Meditation",
            "start_session_prompt_btn": "Start"
        }
    else:
        translations = {
            "page_title": "Bộ hẹn giờ thiền - Thiết lập",
            "heading": "Tùy chọn Thiền Chánh Niệm",
            "label_duration": "Thời gian thiền:",
            "option_1": "1 phút (kiểm tra)",
            "option_15": "15 phút",
            "option_30": "30 phút",
            "option_45": "45 phút",
            "option_60": "60 phút",
            "label_album": "Chọn Album:",
            "album_option_none": "Không sử dụng",
            "select_duration": "Chọn thời gian thiền",
            "select_album": "Chọn Album",
            "button_start": "Bắt đầu",
            "no_music_error": "Không có tệp âm nhạc trong Album đã chọn.",
            "session_title": "Phiên Thiền",
            "btn_pause": "Tạm dừng",
            "btn_resume": "Tiếp tục",
            "btn_exit": "Thoát",
            "start_session_prompt": "Chạm để Bắt đầu Thiền",
            "start_session_prompt_btn": "Bắt đầu"
        }

    albums = Album.objects.all()
    context = {
        "albums": albums,
        "lang": lang,
        "translations": translations,
    }

    if request.method == "POST":
        try:
            meditation_duration = int(request.POST.get("duration"))
        except (TypeError, ValueError):
            meditation_duration = 60  # default to 60 minutes if invalid
        total_seconds = meditation_duration * 60

        album_id = request.POST.get("album")
        if album_id == "0":  # "Not use" option selected: no music.
            context.update({
                "total_seconds": total_seconds,
                "music_url": "",
                "music_duration": 0,
                "music_start_time": 0,
                "lang": lang,
                "translations": translations,
            })
        else:
            music_files = list(MusicFile.objects.filter(album_id=album_id))
            if not music_files:
                context["error"] = translations["no_music_error"]
                return render(request, "meditation/index.html", context)
            selected_music = random.choice(music_files)
            m_duration = selected_music.duration  # in seconds
            # Apply new logic:
            # if music duration >= meditation duration, play immediately (music_start_time = total_seconds).
            # Otherwise, start when remaining time equals music duration.
            if m_duration >= total_seconds:
                music_start_time = total_seconds
            else:
                music_start_time = m_duration
            context.update({
                "total_seconds": total_seconds,
                "music_url": selected_music.file.url,
                "music_duration": m_duration,
                "music_start_time": music_start_time,
                "lang": lang,
                "translations": translations,
            })
        return render(request, "meditation/timer.html", context)
    else:
        return render(request, "meditation/index.html", context)
