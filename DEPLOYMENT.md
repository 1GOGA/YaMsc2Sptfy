# 🚀 Deployment Guide - Host Your App Online

[English](#english) | [Русский](#русский)

---

## English

### The Problem with Localhost

Spotify does NOT allow `localhost` as a redirect URI for security reasons. You must use:
- ✅ `http://127.0.0.1:PORT` for local development 
- ✅ `https://your-domain.com/auth/callback` for production
- ❌ `http://localhost:PORT` (NOT allowed)

### Solution: Deploy to a Free Cloud Service

Here are the easiest ways to deploy your app for **FREE**:

---

## Option 1: Railway.app (Recommended - Easiest)

### Steps:

1. **Sign up at Railway:** https://railway.app (use GitHub login)

2. **Create a new project:**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Select your `YaMsc2Sptfy` repository
   - Railway will auto-deploy

3. **Get your app URL:**
   - Go to "Settings" → "Domain"
   - You'll get: `https://yamsc2sptfy-production.up.railway.app`

4. **Update .env in Railway:**
   - Go to "Variables"
   - Add all your environment variables:
     ```
     SPOTIFY_CLIENT_ID=your_id
     SPOTIFY_CLIENT_SECRET=your_secret
     REDIRECT_URI=https://yamsc2sptfy-production.up.railway.app/auth/callback
     DEBUG=False
     ```

5. **Update Spotify Developer Settings:**
   - Go to https://developer.spotify.com/dashboard
   - Edit your app
   - Add Redirect URI: `https://yamsc2sptfy-production.up.railway.app/auth/callback`

6. **Open your app:**
   - Visit: `https://yamsc2sptfy-production.up.railway.app`

✅ **Done!** Your app is now live on HTTPS!

---

## Option 2: Render.com

### Steps:

1. **Sign up at Render:** https://render.com (use GitHub login)

2. **Create Web Service:**
   - Click "New +"
   - Select "Web Service"
   - Connect your GitHub repository
   - Name: `yamsc2sptfy`
   - Build command: `pip install -r requirements.txt`
   - Start command: `python main.py`

3. **Add Environment Variables:**
   - Go to "Environment"
   - Add all variables (SPOTIFY_CLIENT_ID, etc.)
   - Set `REDIRECT_URI=https://yamsc2sptfy.onrender.com/auth/callback`

4. **Update Spotify Settings:**
   - Add: `https://yamsc2sptfy.onrender.com/auth/callback`

5. **Your app will be at:**
   - `https://yamsc2sptfy.onrender.com`

---

## Option 3: Vercel (For Frontend Only)

If you only want to host the frontend:

1. **Sign up:** https://vercel.com
2. **Import project**
3. **Deploy**

(For backend + frontend together, use Railway or Render)

---

## Option 4: Docker + Local HTTPS (Advanced)

For local testing with HTTPS:

```bash
# Install mkcert (creates local SSL certificates)
choco install mkcert  # Windows

# Create certificates
mkcert localhost 127.0.0.1

# Update Redirect URI in Spotify:
# https://127.0.0.1:8000/auth/callback
```

---

## Comparison Table

| Service | Ease | Cost | SSL | Recommendation |
|---------|------|------|-----|-----------------|
| Railway | ⭐⭐⭐⭐⭐ | Free | ✅ | **BEST** |
| Render | ⭐⭐⭐⭐ | Free | ✅ | Good |
| Vercel | ⭐⭐⭐⭐⭐ | Free | ✅ | Frontend only |
| Heroku | ⭐⭐⭐ | Paid | ✅ | Not recommended (paid now) |

---

## 🔒 Security Best Practices for Production

1. **Use HTTPS only:** Set `DEBUG=False` and use HTTPS redirect URI
2. **Keep secrets safe:** Never commit `.env` file (it's in `.gitignore`)
3. **Update the app:** Use environment variables for all sensitive data
4. **Monitor logs:** Check server logs for errors

---

## Troubleshooting Deployment

**Error: "Invalid redirect_uri"**
- Make sure your `.env` has the exact URL matching Spotify settings

**Error: "Module not found"**
- Check `requirements.txt` has all dependencies
- Restart the deployment

**Cannot access the app**
- Check that the domain is correct
- Give Railway/Render a few minutes to deploy

---

---

## Русский

### Проблема с Localhost

Spotify НЕ разрешает `localhost` в redirect URI по соображениям безопасности. Вы должны использовать:
- ✅ `http://127.0.0.1:PORT` для локальной разработки
- ✅ `https://your-domain.com/auth/callback` для production
- ❌ `http://localhost:PORT` (НЕ разрешено)

### Решение: Развертывание на бесплатном облачном сервисе

Вот самые простые способы развернуть ваше приложение **бесплатно**:

---

## Вариант 1: Railway.app (Рекомендуется - Самый легкий)

### Шаги:

1. **Зарегистрируйтесь на Railway:** https://railway.app (используйте GitHub login)

2. **Создайте новый проект:**
   - Нажмите "New Project"
   - Выберите "Deploy from GitHub repo"
   - Выберите ваш репозиторий `YaMsc2Sptfy`
   - Railway автоматически развернет приложение

3. **Получите URL вашего приложения:**
   - Перейдите в "Settings" → "Domain"
   - Вы получите: `https://yamsc2sptfy-production.up.railway.app`

4. **Обновите .env в Railway:**
   - Перейдите в "Variables"
   - Добавьте все переменные окружения:
     ```
     SPOTIFY_CLIENT_ID=ваш_id
     SPOTIFY_CLIENT_SECRET=ваш_secret
     REDIRECT_URI=https://yamsc2sptfy-production.up.railway.app/auth/callback
     DEBUG=False
     ```

5. **Обновите Spotify Developer Settings:**
   - Перейдите на https://developer.spotify.com/dashboard
   - Отредактируйте ваше приложение
   - Добавьте Redirect URI: `https://yamsc2sptfy-production.up.railway.app/auth/callback`

6. **Откройте ваше приложение:**
   - Посетите: `https://yamsc2sptfy-production.up.railway.app`

✅ **Готово!** Ваше приложение теперь в сети на HTTPS!

---

## Вариант 2: Render.com

### Шаги:

1. **Зарегистрируйтесь на Render:** https://render.com (используйте GitHub login)

2. **Создайте Web Service:**
   - Нажмите "New +"
   - Выберите "Web Service"
   - Подключите ваш GitHub репозиторий
   - Имя: `yamsc2sptfy`
   - Build команда: `pip install -r requirements.txt`
   - Start команда: `python main.py`

3. **Добавьте переменные окружения:**
   - Перейдите в "Environment"
   - Добавьте все переменные (SPOTIFY_CLIENT_ID, и т.д.)
   - Установите `REDIRECT_URI=https://yamsc2sptfy.onrender.com/auth/callback`

4. **Обновите Spotify Settings:**
   - Добавьте: `https://yamsc2sptfy.onrender.com/auth/callback`

5. **Ваше приложение будет по адресу:**
   - `https://yamsc2sptfy.onrender.com`

---

## Вариант 3: Vercel (Только фронтенд)

Если вы хотите только разместить фронтенд:

1. **Зарегистрируйтесь:** https://vercel.com
2. **Импортируйте проект**
3. **Разверните**

(Для backend + frontend вместе используйте Railway или Render)

---

## Вариант 4: Docker + Локальный HTTPS (Продвинутый)

Для локального тестирования с HTTPS:

```bash
# Установите mkcert (создает локальные SSL сертификаты)
choco install mkcert  # Windows

# Создайте сертификаты
mkcert localhost 127.0.0.1

# Обновите Redirect URI в Spotify:
# https://127.0.0.1:8000/auth/callback
```

---

## Таблица сравнения

| Сервис | Легкость | Цена | SSL | Рекомендация |
|--------|----------|------|-----|--------------|
| Railway | ⭐⭐⭐⭐⭐ | Бесп. | ✅ | **ЛУЧШИЙ** |
| Render | ⭐⭐⭐⭐ | Бесп. | ✅ | Хороший |
| Vercel | ⭐⭐⭐⭐⭐ | Бесп. | ✅ | Только фронтенд |
| Heroku | ⭐⭐⭐ | Платн. | ✅ | Не рекомендуется |

---

## 🔒 Практики безопасности для Production

1. **Используйте только HTTPS:** Установите `DEBUG=False` и используйте HTTPS redirect URI
2. **Храните секреты в безопасности:** Никогда не коммитьте `.env` файл (уже в `.gitignore`)
3. **Обновляйте приложение:** Используйте переменные окружения для всех чувствительных данных
4. **Отслеживайте логи:** Проверяйте логи сервера на ошибки

---

## Решение проблем при развертывании

**Ошибка: "Invalid redirect_uri"**
- Убедитесь, что ваш `.env` имеет точный URL, совпадающий с Spotify settings

**Ошибка: "Module not found"**
- Проверьте, что `requirements.txt` имеет все зависимости
- Перезагрузите deployment

**Не можете получить доступ к приложению**
- Проверьте, что домен правильный
- Дайте Railway/Render несколько минут на развертывание
