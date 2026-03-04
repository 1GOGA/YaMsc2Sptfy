# 📤 Upload to GitHub - Step by Step Guide

[English](#english) | [Русский](#русский)

---

## English

### ✅ Prerequisites
- GitHub account (create at https://github.com)
- Git installed on your computer (https://git-scm.com)
- The project is already initialized as a Git repository ✓

### 🚀 Step 1: Create a New Repository on GitHub

1. Go to https://github.com/new
2. Name: `YaMsc2Sptfy` (or your preferred name)
3. Description: `Migrate playlists from Yandex Music to Spotify with Python FastAPI`
4. **Important**: Select **Public** (to share open source)
5. **DO NOT** initialize with README (we already have one)
6. Click **"Create repository"**

### 📋 Step 2: Copy Your Repository URL

After creating, you'll see this page. Copy the HTTPS URL:
```
https://github.com/YOUR_USERNAME/YaMsc2Sptfy.git
```

### 🔗 Step 3: Add Remote and Push to GitHub

Replace `YOUR_USERNAME` with your actual GitHub username:

```bash
cd c:\Users\PytoshKa\Documents\YaMsc2Sptfy

# Add the remote repository
git remote add origin https://github.com/YOUR_USERNAME/YaMsc2Sptfy.git

# Rename branch to 'main' (GitHub default)
git branch -M main

# Push all commits to GitHub
git push -u origin main
```

### ✨ Step 4: Verify on GitHub

1. Go to https://github.com/YOUR_USERNAME/YaMsc2Sptfy
2. You should see all your files (README.md, app/, static/, etc.)
3. Scroll down to see the project description
4. ✅ Your project is now on GitHub!

### 🎯 What to Do Next

**Add a License:**
```bash
# Create a LICENSE file with MIT license
curl https://opensource.org/licenses/MIT -o LICENSE
git add LICENSE
git commit -m "Add MIT license"
git push
```

**Add Topics/Tags on GitHub:**
1. Go to your repository
2. Click "Settings" (top right)
3. Scroll to "Topics"
4. Add: `spotify`, `yandex-music`, `python`, `fastapi`, `playlist-migrator`, `music`

**Share Your Project:**
- Share the GitHub URL with friends
- Consider sharing on Reddit, HackerNews, ProductHunt

### 💡 Common Commands

**Check remote URL:**
```bash
git remote -v
```

**View Git status:**
```bash
git status
```

**Make a new commit after changes:**
```bash
git add .
git commit -m "Your commit message"
git push
```

**View commit history:**
```bash
git log --oneline
```

---

## Русский

### ✅ Предварительные требования
- Аккаунт GitHub (создайте на https://github.com)
- Git установлен на вашем компьютере (https://git-scm.com)
- Проект уже инициализирован как Git репозиторий ✓

### 🚀 Шаг 1: Создайте новый репозиторий на GitHub

1. Перейдите на https://github.com/new
2. Имя: `YaMsc2Sptfy` (или любое другое)
3. Описание: `Migrate playlists from Yandex Music to Spotify with Python FastAPI`
4. **Важно**: Выберите **Public** (чтобы поделиться открытым кодом)
5. **НЕ** инициализируйте с README (у нас уже есть один)
6. Нажмите **"Create repository"**

### 📋 Шаг 2: Скопируйте ваш URL репозитория

После создания вы увидите эту страницу. Скопируйте HTTPS URL:
```
https://github.com/ВАШ_ЮЗЕРНЕЙМ/YaMsc2Sptfy.git
```

### 🔗 Шаг 3: Добавьте удаленный репозиторий и загрузите на GitHub

Замените `ВАШ_ЮЗЕРНЕЙМ` на ваш фактический username на GitHub:

```bash
cd c:\Users\PytoshKa\Documents\YaMsc2Sptfy

# Добавьте удаленный репозиторий
git remote add origin https://github.com/ВАШ_ЮЗЕРНЕЙМ/YaMsc2Sptfy.git

# Переименуйте ветку на 'main' (стандарт GitHub)
git branch -M main

# Загрузите все коммиты на GitHub
git push -u origin main
```

### ✨ Шаг 4: Проверьте на GitHub

1. Перейдите на https://github.com/ВАШ_ЮЗЕРНЕЙМ/YaMsc2Sptfy
2. Вы должны увидеть все ваши файлы (README.md, app/, static/, и т.д.)
3. Прокрутите вниз, чтобы увидеть описание проекта
4. ✅ Ваш проект теперь на GitHub!

### 🎯 Что делать дальше

**Добавьте лицензию:**
```bash
# Создайте файл LICENSE с лицензией MIT
curl https://opensource.org/licenses/MIT -o LICENSE
git add LICENSE
git commit -m "Add MIT license"
git push
```

**Добавьте теги/темы на GitHub:**
1. Перейдите в ваш репозиторий
2. Нажмите "Settings" (справа сверху)
3. Найдите "Topics"
4. Добавьте: `spotify`, `yandex-music`, `python`, `fastapi`, `playlist-migrator`, `music`

**Поделитесь своим проектом:**
- Поделитесь ссылкой на GitHub с друзьями
- Рассмотрите публикацию на Reddit, HackerNews, ProductHunt

### 💡 Основные команды

**Проверить URL удаленного репозитория:**
```bash
git remote -v
```

**Посмотреть статус Git:**
```bash
git status
```

**Создать новый коммит после изменений:**
```bash
git add .
git commit -m "Your commit message"
git push
```

**Посмотреть историю коммитов:**
```bash
git log --oneline
```

---

## 📸 What Your GitHub Page Will Look Like

Your repository will display:
- ✅ Project name and description
- ✅ Language: Python (detected automatically)
- ✅ Files and folders
- ✅ README.md rendered nicely
- ✅ Star button for users to bookmark
- ✅ Fork button for users to contribute
- ✅ Issues and Pull Requests tabs

Perfect for an open source project! 🚀
