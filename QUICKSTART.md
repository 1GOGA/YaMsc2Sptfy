# ⚡ Quick Start Guide

**[EN](#english) | [РУ](#русский)**

---

## English

### 🚀 Running the Application in 5 Minutes

#### Step 1: Install Python Dependencies
```bash
pip install -r requirements.txt
```

#### Step 2: Create `.env` File
```bash
# Copy the example file
cp .env.example .env

# Or on Windows:
copy .env.example .env
```

#### Step 3: Add Spotify Credentials
Open `.env` and fill in your Spotify Developer credentials:
```env
SPOTIFY_CLIENT_ID=your_actual_client_id
SPOTIFY_CLIENT_SECRET=your_actual_client_secret
REDIRECT_URI=http://127.0.0.1:8000/auth/callback
DEBUG=True
```

⚠️ **Important**: Spotify does NOT allow `localhost` - use `127.0.0.1` instead!

**Where to get Spotify credentials:**
1. Go to https://developer.spotify.com/dashboard
2. Log in with your Spotify account
3. Click "Create an App"
4. Accept terms and create the app
5. Copy `Client ID` and `Client Secret`
6. In Settings, add Redirect URI: `http://127.0.0.1:8000/auth/callback` (⚠️ NOT localhost!)

#### Step 4: Run the Server
```bash
python main.py
```

✅ The app will start on `http://localhost:8000`

#### Step 5: Open in Browser
```
http://localhost:8000
```

**That's it!** 🎉

### 📝 Usage Tips

- Click **"Login with Spotify"** to authorize
- Paste a Yandex Music playlist URL (public playlists only)
- Example: `https://music.yandex.ru/users/yamusicbot/playlists/1015`
- Watch the live progress log
- Click the Spotify link to view your new playlist

### 🔧 Troubleshooting

**Error: "ModuleNotFoundError"**
- Make sure you installed requirements: `pip install -r requirements.txt`

**Error: "Port 8000 already in use"**
- Change APP_PORT in .env or kill the process using port 8000

**Error: "Invalid credentials"**
- Double-check your SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET in .env

---

## Русский

### 🚀 Запуск приложения за 5 минут

#### Шаг 1: Установите зависимости Python
```bash
pip install -r requirements.txt
```

#### Шаг 2: Создайте файл `.env`
```bash
# Скопируйте пример
cp .env.example .env

# Или на Windows:
copy .env.example .env
```

#### Шаг 3: Добавьте учетные данные Spotify
Откройте `.env` и заполните ваши учетные данные Spotify Developer:
```env
SPOTIFY_CLIENT_ID=ваш_actual_client_id
SPOTIFY_CLIENT_SECRET=ваш_actual_client_secret
REDIRECT_URI=http://localhost:8000/auth/callback
DEBUG=True
```

**Где получить учетные данные Spotify:**
1. Перейдите на https://developer.spotify.com/dashboard
2. Войдите в ваш аккаунт Spotify
3. Нажмите "Create an App"
4. Примите условия и создайте приложение
5. Скопируйте `Client ID` и `Client Secret`
6. В Settings добавьте Redirect URI: `http://localhost:8000/auth/callback`

#### Шаг 4: Запустите сервер
```bash
python main.py
```

✅ Приложение запустится на `http://localhost:8000`

#### Шаг 5: Откройте в браузере
```
http://localhost:8000
```

**Вот и все!** 🎉

### 📝 Советы по использованию

- Нажмите **"Войти со Spotify"** для авторизации
- Вставьте URL плейлиста Яндекс Музыки (только публичные)
- Пример: `https://music.yandex.ru/users/yamusicbot/playlists/1015`
- Смотрите живой лог прогресса
- Нажмите ссылку на Spotify, чтобы посмотреть вашу новую плейлист

### 🔧 Решение проблем

**Ошибка: "ModuleNotFoundError"**
- Убедитесь, что вы установили зависимости: `pip install -r requirements.txt`

**Ошибка: "Port 8000 already in use"**
- Измените APP_PORT в .env или завершите процесс, используя порт 8000

**Ошибка: "Invalid credentials"**
- Дважды проверьте ваши SPOTIFY_CLIENT_ID и SPOTIFY_CLIENT_SECRET в .env
