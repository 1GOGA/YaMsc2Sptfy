# ⚡ БЫСТРАЯ САМШПАРГАЛКА - Запуск за 10 минут

## 1️⃣ ЧТО НУЖНО

- Python 3.10+ (https://python.org)
- Git (https://git-scm.com)
- Spotify аккаунт (https://spotify.com)

---

## 2️⃣ SPOTIFY КЛЮЧИ

1. https://developer.spotify.com/dashboard
2. Логин/регистрация
3. **Create an App**
   - Согласитесь с условияминажмите Create
4. **Edit Settings**
   - Добавьте Redirect URI: `http://127.0.0.1:8000/auth/callback`
   - Save
5. **Скопируйте:**
   - Client ID
   - Client Secret

---

## 3️⃣ СКАЧАЙТЕ ПРОЕКТ

```bash
git clone https://github.com/1GOGA/YaMsc2Sptfy.git
cd YaMsc2Sptfy
```

---

## 4️⃣ СОЗДАЙТЕ .env

```bash
copy .env.example .env
```

Откройте `.env` и заполните:
```env
SPOTIFY_CLIENT_ID=ваш_id
SPOTIFY_CLIENT_SECRET=ваш_secret
REDIRECT_URI=http://127.0.0.1:8000/auth/callback
DEBUG=True
```

---

## 5️⃣ УСТАНОВИТЕ ЗАВИСИМОСТИ

```bash
pip install -r requirements.txt
```

---

## 6️⃣ ЗАПУСТИТЕ

```bash
python main.py
```

---

## 7️⃣ ОТКРОЙТЕ В БРАУЗЕРЕ

```
http://127.0.0.1:8000
```

⚠️ **НЕ localhost!** Используйте `127.0.0.1`

---

## 8️⃣ ИСПОЛЬЗУЙТЕ

1. Нажмите "Войти со Spotify"
2. Авторизуйтесь
3. Вставьте ссылку на плейлист Яндекса
4. Нажмите "Начать перенос"
5. Готово! 🎵

---

## 🌍 РАЗВЕРТЫВАНИЕ ОНЛАЙН

**Railway.app (бесплатно, HTTPS):**

1. https://railway.app → Sign Up (GitHub login)
2. New Project → Deploy from GitHub repo
3. Выберите `1GOGA/YaMsc2Sptfy`
4. Добавьте переменные из `.env`
5. Когда развернется, получите URL
6. Обновите Redirect URI в Spotify на новый URL
7. Готово! Сайт живой! 🚀

---

## 🆘 ОШИБКИ

| Ошибка | Решение |
|--------|---------|
| ModuleNotFoundError | `pip install -r requirements.txt` |
| Port 8000 already in use | Измените APP_PORT в .env |
| Redirect URI mismatch | Проверьте что URL совпадает в Spotify |
| Cannot connect to Spotify | Проверьте CLIENT_ID и SECRET |

---

## 📚 ПОЛНЫЙ ГАЙД

Для деталей читайте: **RUSSIAN_GUIDE.md** в папке проекта

---

**ВСЕ ГОТОВО! УСПЕХОВ!** 🎉
