import random
from django.shortcuts import render
from .models import Album, MusicFile


def format_music_duration(seconds):
    """Convert seconds to mm:ss format."""
    minutes = seconds // 60
    sec = seconds % 60
    return f"{minutes}:{sec:02d}"


def index(request):
    # Determine language (default to Vietnamese "vi")
    lang = request.GET.get("lang", "vi")
    if request.method == "POST":
        lang = request.POST.get("lang", lang)

    # Translation dictionaries
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
            "label_album": "Choose an Dhamma Talk:",
            "album_option_none": "Not use",
            "select_duration": "Select Duration",
            "select_album": "Select an Dhamma Talk",
            "button_start": "Start",
            "no_music_error": "No music files available in the selected Dhamma Talk.",
            "session_title": "Meditation Session",
            "btn_pause": "Pause",
            "btn_resume": "Resume",
            "btn_exit": "Exit",
            "start_session_prompt": "Tap to Start Meditation",
            "start_session_prompt_btn": "Start",
            "music_label": "Dhamma Talk: ",
            "no_music": "No Dhamma Talk"
        }
    else:
        translations = {
            "page_title": "Bộ hẹn giờ thiền - Thiết lập",
            "heading": "Thiền Chánh Niệm",
            "label_duration": "Thời gian thiền:",
            "option_1": "1 phút (kiểm tra)",
            "option_15": "15 phút",
            "option_30": "30 phút",
            "option_45": "45 phút",
            "option_60": "60 phút",
            "label_album": "Chọn Pháp thoại:",
            "album_option_none": "Không sử dụng",
            "select_duration": "Chọn thời gian thiền",
            "select_album": "Chọn Pháp thoại:",
            "button_start": "Bắt đầu",
            "no_music_error": "Không có lời Pháp trong Album đã chọn.",
            "session_title": "Thời Thiền",
            "btn_pause": "Tạm dừng",
            "btn_resume": "Tiếp tục",
            "btn_exit": "Thoát",
            "start_session_prompt": "Chạm để Bắt đầu Thiền",
            "start_session_prompt_btn": "Bắt đầu",
            "music_label": "Pháp thoại lúc: ",
            "no_music": "Không có Pháp thoại"
        }

    # Get all albums from the database
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
        # If the user selects "Not use" (value "0"), then no music will be played.
        if album_id == "0":
            context.update({
                "total_seconds": total_seconds,
                "music_url": "",
                "music_duration": 0,
                "music_duration_str": "",
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
            m_duration_str = format_music_duration(m_duration)
            # Determine when to start the music:
            # - If the music duration is greater than or equal to the meditation duration,
            #   the music starts immediately (music_start_time = total_seconds).
            # - Otherwise, the music starts when remaining time equals the music duration.
            if m_duration >= total_seconds:
                music_start_time = total_seconds
            else:
                music_start_time = m_duration
            context.update({
                "total_seconds": total_seconds,
                "music_url": selected_music.file.url,
                "music_duration": m_duration,
                "music_duration_str": m_duration_str,
                "music_start_time": music_start_time,
                "lang": lang,
                "translations": translations,
            })
        return render(request, "meditation/timer.html", context)
    else:
        return render(request, "meditation/index.html", context)
