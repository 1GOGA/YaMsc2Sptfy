# YaMsc2Sptfy - Yandex Music to Spotify Playlist Migrator

**[English](#english) | [Русский](#русский)**

---

## English

A modern web application that helps you migrate your public playlists from Yandex Music to Spotify. Written in Python (FastAPI) with a beautiful, responsive web interface.

## 🎵 Features

- **Simple URL Input**: Just paste a Yandex Music playlist link
- **Smart Track Matching**: Automatically searches for tracks on Spotify using artist and title
- **Real-time Progress**: Live event log showing what's happening step-by-step
- **Automatic Playlist Creation**: Creates a new playlist in your Spotify account
- **Batch Processing**: Efficiently handles up to 100 tracks per batch
- **Error Handling**: Gracefully handles missing tracks and API errors
- **Dark Mode**: Beautiful dark theme support
- **Fully Open Source**: Production-ready code ready for GitHub

## 📋 Requirements

- Python 3.10 or higher
- Spotify account (free or premium)
- Public Yandex Music playlist

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/YaMsc2Sptfy.git
cd YaMsc2Sptfy
```

### 2. Create Virtual Environment

```bash
# Using venv
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Or using Conda
conda create -n yamsc2sptfy python=3.10
conda activate yamsc2sptfy
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Spotify Developer Credentials

1. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Log in or create a Spotify account
3. Click "Create an App"
4. Accept the terms and create the app
5. Copy your `Client ID` and `Client Secret`
6. Go to "Edit Settings"
7. Add `Redirect URI`: `http://localhost:8000/auth/callback`

### 5. Configure Environment Variables

Copy the example environment file and fill in your Spotify credentials:

```bash
cp .env.example .env
```

Edit `.env` and add your Spotify credentials:

```env
SPOTIFY_CLIENT_ID=your_client_id_here
SPOTIFY_CLIENT_SECRET=your_client_secret_here
REDIRECT_URI=http://localhost:8000/auth/callback
DEBUG=True
```

**⚠️ Important**: Never commit `.env` to Git. It's already in `.gitignore`.

## 🏃 Running the Application

```bash
python main.py
```

The application will start on `http://localhost:8000`

Open your browser and navigate to `http://localhost:8000`

## 💻 Usage

1. **Login**: Click "Login with Spotify" and authorize the application
2. **Paste Playlist Link**: Enter a Yandex Music playlist URL, e.g.:
   - `https://music.yandex.ru/users/yamusicbot/playlists/1015`
   - Or just: `yamusicbot/1015`
3. **Start Migration**: Click "Start Migration" and watch the progress
4. **View Results**: After completion, click the link to open your new playlist on Spotify

## 📚 Architecture

### Project Structure

```
YaMsc2Sptfy/
├── app/
│   ├── __init__.py
│   ├── main.py                    # FastAPI app setup
│   ├── config.py                  # Settings from .env
│   ├── models.py                  # Pydantic request/response models
│   ├── security.py                # Token validation
│   ├── dependencies.py            # FastAPI dependency injection
│   ├── routers/
│   │   ├── auth.py               # Spotify OAuth routes
│   │   └── playlist.py           # Playlist migration routes
│   └── services/
│       ├── spotify_client.py     # Spotipy wrapper
│       ├── yandex_parser.py      # Yandex Music parser
│       └── playlist_converter.py # Conversion orchestration
├── static/
│   └── index.html                 # Single-page frontend (Tailwind CSS)
├── main.py                        # Entry point
├── requirements.txt               # Dependencies
├── .env.example                   # Environment template
├── .gitignore                     # Git ignore rules
└── README.md                      # This file
```

### Technology Stack

- **Backend**: 
  - FastAPI 0.104.1 - Modern Python web framework
  - Uvicorn 0.24.0 - ASGI server
  - Spotipy 2.23.0 - Spotify API client
  - yandex-music 4.1.0 - Yandex Music parser
  - Pydantic 2.5.0 - Data validation

- **Frontend**:
  - HTML5
  - Tailwind CSS 3 (CDN) - No build step required
  - Vanilla JavaScript (ES6+)

### API Endpoints

#### Authentication

- `GET /auth/login` - Initiate Spotify OAuth2 login
- `GET /auth/callback` - Handle OAuth2 callback
- `POST /auth/logout` - Logout and clear token
- `GET /auth/status` - Check authentication status

#### Playlist Migration

- `POST /api/migrate/` - Start a new migration job
  - Request: `{"yandex_playlist_url": "..."}`
  - Response: `{"job_id": "uuid", "message": "..."}`

- `GET /api/migrate/{job_id}/status` - Get current migration status
  - Response: `{"status": "pending|searching|creating|complete|error", "progress": int, "total": int, ...}`

- `GET /api/migrate/{job_id}/logs` - Get event logs (for polling)
  - Response: `[{"timestamp": "...", "level": "info|warning|error", "message": "..."}, ...]`

## 🔒 Security Considerations

- **Environment Variables**: All secrets are in `.env` (not committed to Git)
- **HTTPS in Production**: Configure HTTPS with proper certificates
- **Token Protection**: Spotify tokens stored in httponly cookies (secure flag for HTTPS)
- **CSRF Protection**: State tokens validate OAuth callback authenticity
- **Input Validation**: All user input validated with Pydantic
- **Error Handling**: Sensitive errors logged locally, generic messages sent to frontend

## ⚙️ Configuration

Edit the variables in `.env` to customize the application:

```env
# Spotify Settings
SPOTIFY_CLIENT_ID=...
SPOTIFY_CLIENT_SECRET=...
REDIRECT_URI=http://localhost:8000/auth/callback  # Change for production

# Application Settings
DEBUG=True          # Set to False for production
APP_NAME=YaMsc2Sptfy
APP_PORT=8000
```

## 🐛 Known Limitations

1. **Public Playlists Only**: Only supports public Yandex Music playlists
2. **Track Matching**: Not all Yandex tracks may be found on Spotify
3. **Artist Name Variations**: Different artist name formats can affect matching accuracy
4. **Quota Limits**: Spotify and Yandex have their own API rate limits
5. **Data Retention**: Migration history is not persisted (session-only)

## 📊 Troubleshooting

### Problem: "Connect to Spotify failed"
- **Solution**: Check that `SPOTIFY_CLIENT_ID` and `SPOTIFY_CLIENT_SECRET` are correct in `.env`

### Problem: "Playlist not found"
- **Solution**: Ensure the Yandex playlist is public, not private

### Problem: "Token expired"
- **Solution**: The app doesn't implement refresh tokens. Log out and log in again

### Problem: "Very few tracks found on Spotify"
- **Solution**: Spotify's search is strict about artist/title matching. Try searching manually for similar artists

### Problem: Port 8000 already in use
- **Solution**: Change `APP_PORT` in `.env` or kill the process using port 8000

## 🚀 Deployment

### Docker (Optional)

```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "main.py"]
```

Build and run:
```bash
docker build -t yamsc2sptfy .
docker run -p 8000:8000 --env-file .env yamsc2sptfy
```

### Production Checklist

- [ ] Set `DEBUG=False` in `.env`
- [ ] Configure HTTPS with proper certificates
- [ ] Update `REDIRECT_URI` to your production domain
- [ ] Use environment-specific `.env` files
- [ ] Consider using a production ASGI server like Gunicorn
- [ ] Add proper logging and monitoring
- [ ] Implement database for migration history (optional)
- [ ] Add rate limiting to API endpoints

## 📝 Development

### Adding Features

1. Create a new router in `app/routers/`
2. Include it in `app/main.py`
3. Follow the existing error handling patterns
4. Update documentation

### Testing

```bash
# Manual testing
curl http://localhost:8000/health

# Browser testing
# Visit http://localhost:8000 and test the UI
```

## 🔄 API Flow

```
User Login
    ↓
Spotify OAuth2 Authorization Code Flow
    ↓
User Authenticated (token stored in httponly cookie)
    ↓
User Submits Yandex Playlist URL
    ↓
POST /api/migrate/ → Returns job_id
    ↓
Frontend Polls: GET /api/migrate/{job_id}/status
    ↓
Backend Steps:
  1. Parse Yandex playlist (get track list)
  2. Search each track on Spotify
  3. Create new Spotify playlist
  4. Batch add tracks (max 100 per request)
  5. Return success with playlist URL
    ↓
Frontend Displays Results
```

## 📜 License

MIT License - Feel free to use this project for personal or commercial purposes.

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 💬 Support

For issues, questions, or suggestions, please open an issue on GitHub.

## 🙏 Acknowledgments

- [Spotipy](https://github.com/spotipy-dev/spotipy) - Spotify API wrapper
- [yandex-music](https://github.com/MarshalX/yandex-music-api) - Yandex Music parser
- [FastAPI](https://fastapi.tiangolo.com/) - Modern Python web framework
- [Tailwind CSS](https://tailwindcss.com/) - Utility-first CSS framework

---

Made with ❤️ for music lovers. Happy migrating! 🎵

---

## Русский

Современное веб-приложение, которое помогает переносить ваши публичные плейлисты из Яндекс Музыки на Spotify. Написано на Python (FastAPI) с красивым и адаптивным веб-интерфейсом.

### 🎵 Основные возможности

- **Простой ввод URL**: Просто вставьте ссылку на плейлист Яндекс Музыки
- **Умное поиск треков**: Автоматически ищет треки на Spotify по названию исполнителя и песни
- **Прямой эфир прогресса**: Живой лог событий, показывающий что происходит на каждом шаге
- **Автоматическое создание плейлиста**: Создает новый плейлист в вашем аккаунте Spotify
- **Пакетная обработка**: Эффективно обрабатывает до 100 треков за один запрос
- **Обработка ошибок**: Корректно обрабатывает пропущенные треки и ошибки API
- **Темный режим**: Красивая поддержка темной темы
- **Полностью открытый исходный код**: Готовый к публикации на GitHub код

### 📋 Требования

- Python 3.10 или выше
- Аккаунт Spotify (бесплатный или Premium)
- Публичный плейлист Яндекс Музыки

### 🚀 Установка

#### 1. Клонируйте репозиторий

```bash
git clone https://github.com/your-username/YaMsc2Sptfy.git
cd YaMsc2Sptfy
```

#### 2. Создайте виртуальное окружение

```bash
# Используя venv
python -m venv venv
source venv/bin/activate  # На Windows: venv\Scripts\activate

# Или используя Conda
conda create -n yamsc2sptfy python=3.10
conda activate yamsc2sptfy
```

#### 3. Установите зависимости

```bash
pip install -r requirements.txt
```

#### 4. Настройка учетных данных Spotify

1. Перейдите на [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Войдите или создайте аккаунт Spotify
3. Нажмите "Create an App"
4. Примите условия и создайте приложение
5. Скопируйте ваш `Client ID` и `Client Secret`
6. Перейдите в "Edit Settings"
7. Добавьте `Redirect URI`: `http://localhost:8000/auth/callback`

#### 5. Настройка переменных окружения

Скопируйте пример файла окружения и заполните ваши учетные данные Spotify:

```bash
cp .env.example .env
```

Отредактируйте `.env` и добавьте ваши учетные данные Spotify:

```env
SPOTIFY_CLIENT_ID=ваш_client_id_здесь
SPOTIFY_CLIENT_SECRET=ваш_client_secret_здесь
REDIRECT_URI=http://localhost:8000/auth/callback
DEBUG=True
```

**⚠️ Важно**: Никогда не коммитьте `.env` на Git. Он уже в `.gitignore`.

### 🏃 Запуск приложения

```bash
python main.py
```

Приложение запустится на `http://localhost:8000`

Откройте ваш браузер и перейдите на `http://localhost:8000`

### 💻 Использование

1. **Вход**: Нажмите "Войти со Spotify" и авторизуйте приложение
2. **Вставьте ссылку на плейлист**: Введите URL плейлиста Яндекс Музыки, например:
   - `https://music.yandex.ru/users/yamusicbot/playlists/1015`
   - Или просто: `yamusicbot/1015`
3. **Начните перенос**: Нажмите "Начать перенос" и отслеживайте прогресс
4. **Посмотрите результаты**: После завершения нажмите ссылку, чтобы открыть новый плейлист на Spotify

### 📚 Архитектура

#### Структура проекта

```
YaMsc2Sptfy/
├── app/
│   ├── __init__.py
│   ├── main.py                    # Инициализация FastAPI
│   ├── config.py                  # Настройки из .env
│   ├── models.py                  # Pydantic модели запросов/ответов
│   ├── security.py                # Валидация токенов
│   ├── dependencies.py            # Внедрение зависимостей FastAPI
│   ├── routers/
│   │   ├── auth.py               # Маршруты Spotify OAuth
│   │   └── playlist.py           # Маршруты миграции плейлистов
│   └── services/
│       ├── spotify_client.py     # Обертка Spotipy
│       ├── yandex_parser.py      # Парсер Яндекс Музыки
│       └── playlist_converter.py # Оркестрация преобразования
├── static/
│   └── index.html                 # Одностраничное приложение (Tailwind CSS)
├── main.py                        # Точка входа
├── requirements.txt               # Зависимости
├── .env.example                   # Шаблон окружения
├── .gitignore                     # Правила Git игнорирования
└── README.md                      # Этот файл
```

### Технологический стек

**Backend**:
- FastAPI 0.104.1 - Современный фреймворк Python
- Uvicorn 0.24.0 - ASGI сервер
- Spotipy 2.23.0 - Клиент Spotify API
- yandex-music 4.1.0 - Парсер Яндекс Музыки
- Pydantic 2.5.0 - Валидация данных

**Frontend**:
- HTML5
- Tailwind CSS 3 (CDN) - Никакого этапа сборки не требуется
- Vanilla JavaScript (ES6+)

### API маршруты

#### Аутентификация

- `GET /auth/login` - Инициировать вход через Spotify OAuth2
- `GET /auth/callback` - Обработка callback OAuth2
- `POST /auth/logout` - Выход и очистка токена
- `GET /auth/status` - Проверить статус аутентификации

#### Миграция плейлистов

- `POST /api/migrate/` - Запустить новую задачу миграции
  - Запрос: `{"yandex_playlist_url": "..."}`
  - Ответ: `{"job_id": "uuid", "message": "..."}`

- `GET /api/migrate/{job_id}/status` - Получить текущий статус миграции
  - Ответ: `{"status": "pending|searching|creating|complete|error", "progress": int, "total": int, ...}`

- `GET /api/migrate/{job_id}/logs` - Получить логи событий (для опроса)
  - Ответ: `[{"timestamp": "...", "level": "info|warning|error", "message": "..."}, ...]`

### 🔒 Вопросы безопасности

- **Переменные окружения**: Все секреты находятся в `.env` (не коммитятся на Git)
- **HTTPS в Production**: Настройте HTTPS с правильными сертификатами
- **Защита токенов**: Токены Spotify хранятся в httponly cookies (флаг secure для HTTPS)
- **Защита CSRF**: Токены состояния проверяют подлинность обратного вызова OAuth
- **Валидация входящих данных**: Все пользовательские входы проверяются с Pydantic
- **Обработка ошибок**: Чувствительные ошибки логируются локально, пользователям отправляются основные сообщения

### ⚙️ Конфигурация

Отредактируйте переменные в `.env` для настройки приложения:

```env
# Настройки Spotify
SPOTIFY_CLIENT_ID=...
SPOTIFY_CLIENT_SECRET=...
REDIRECT_URI=http://localhost:8000/auth/callback  # Измените для production

# Настройки приложения
DEBUG=True          # Установите False для production
APP_NAME=YaMsc2Sptfy
APP_PORT=8000
```

### 🐛 Известные ограничения

1. **Только публичные плейлисты**: Поддерживает только публичные плейлисты Яндекс Музыки
2. **Поиск треков**: Не все треки Яндекса могут быть найдены на Spotify
3. **Вариации имен артистов**: Различные форматы имен артистов могут влиять на точность поиска
4. **Квоты API**: Spotify и Яндекс имеют свои собственные ограничения API
5. **Сохранение данных**: История миграции не сохраняется (только в сессии)

### 📊 Решение проблем

#### Проблема: "Connect to Spotify failed"
- **Решение**: Проверьте, что `SPOTIFY_CLIENT_ID` и `SPOTIFY_CLIENT_SECRET` верны в `.env`

#### Проблема: "Playlist not found"
- **Решение**: Убедитесь, что плейлист Яндекса публичный, а не приватный

#### Проблема: "Token expired"
- **Решение**: Приложение не реализует refresh токены. Выйдите и войдите снова

#### Проблема: "Very few tracks found on Spotify"
- **Решение**: Поиск Spotify строг к совпадению названия. Попробуйте искать похожих артистов вручную

#### Проблема: "Port 8000 already in use"
- **Решение**: Измените `APP_PORT` в `.env` или завершите процесс, использующий порт 8000

### 🚀 Развертывание

#### Docker (опционально)

```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "main.py"]
```

Построить и запустить:
```bash
docker build -t yamsc2sptfy .
docker run -p 8000:8000 --env-file .env yamsc2sptfy
```

#### Контрольный список для Production

- [ ] Установите `DEBUG=False` в `.env`
- [ ] Настройте HTTPS с правильными сертификатами
- [ ] Обновите `REDIRECT_URI` на ваш домен production
- [ ] Используйте файлы `.env` специфичные для окружения
- [ ] Рассмотрите использование production ASGI сервера типа Gunicorn
- [ ] Добавьте правильное логирование и мониторинг
- [ ] Реализуйте базу данных для истории миграции (опционально)
- [ ] Добавьте ограничения скорости для API сущности

### 📝 Разработка

#### Добавление функций

1. Создайте новый маршрут в `app/routers/`
2. Включите его в `app/main.py`
3. Следуйте существующим паттернам обработки ошибок
4. Обновите документацию

#### Тестирование

```bash
# Ручное тестирование
curl http://localhost:8000/health

# Тестирование в браузере
# Посетите http://localhost:8000 и протестируйте UI
```

### 🔄 Поток работы API

```
Вход пользователя
    ↓
Поток авторизации Spotify OAuth2 (код авторизации)
    ↓
Пользователь аутентифицирован (токен сохранен в httponly cookie)
    ↓
Пользователь отправляет URL плейлиста Яндекса
    ↓
POST /api/migrate/ → Возвращает job_id
    ↓
Frontend опрашивает: GET /api/migrate/{job_id}/status
    ↓
Скачиваются шаги Backend:
  1. Парсинг плейлиста Яндекса (получение списка треков)
  2. Поиск каждого трека на Spotify
  3. Создание нового плейлиста Spotify
  4. Пакетное добавление треков (макс 100 за запрос)
  5. Возврат успеха с URL плейлиста
    ↓
Frontend показывает результаты
```

### 📜 Лицензия

MIT License - Свободно используйте этот проект в личных или коммерческих целях.

### 🤝 Участие в разработке

Приветствуются вклады! Пожалуйста:
1. Создайте fork репозитория
2. Создайте feature ветку
3. Коммитьте ваши изменения
4. Отправьте на ветку
5. Создайте Pull Request

### 💬 Поддержка

По вопросам, ошибкам или предложениям откройте issue на GitHub.

### 🙏 Благодарности

- [Spotipy](https://github.com/spotipy-dev/spotipy) - Обертка Spotify API
- [yandex-music](https://github.com/MarshalX/yandex-music-api) - Парсер Яндекс Музыки
- [FastAPI](https://fastapi.tiangolo.com/) - Современный фреймворк Python
- [Tailwind CSS](https://tailwindcss.com/) - Утилитарный CSS фреймворк

---

Сделано с ❤️ для любителей музыки. Счастливого переноса! 🎵
