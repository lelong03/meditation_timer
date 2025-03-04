# Meditation Timer

Meditation Timer is a mobile-first, Django-based web application that allows users to choose a meditation duration, track progress with a circular timer, and optionally play guided meditation audio (Meditation Audio Talk). The app supports multi-language (Vietnamese and English) and features a modern, responsive UI optimized for mobile devices.

## Features

- **Meditation Timer:** Choose from durations such as 1 minute (for testing), 15, 30, 45, and 60 minutes.
- **Audio Talk Option:** Toggle the "Meditation Audio Talk" checkbox to enable or disable playing a guided audio track at the end of the session.
- **Albums & Music Management:** Manage music files via the Django admin. Each album can contain multiple music tracks with metadata like duration and order.
- **Modern Responsive UI:** Designed with a flat, modern aesthetic using pastel and radiant colors. The UI is optimized for mobile devices.
- **Session Controls:** Pause/Resume the timer and exit the session with intuitive icon-based controls.
- **Multi-Language Support:** Built-in support for Vietnamese (default) and English. Users can easily switch languages using a language toggle icon.

## Technologies Used

- **Backend:** Django (Python)
- **Frontend:** HTML, CSS, JavaScript, Font Awesome, Google Fonts
- **Deployment:** Gunicorn, Nginx, DigitalOcean (optional)
- **Version Control:** Git

## Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/yourusername/meditation_timer.git
   cd meditation_timer
   ```

2. **Create & Activate a Virtual Environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
   
3. **Install Dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Apply Migrations:**

    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

## Usage
1. **Run the Development Server:**

    ```bash
    python manage.py runserver
    ```