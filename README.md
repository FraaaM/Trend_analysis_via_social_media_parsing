# Trend_analysis_via_social_media_parsing

Важно: для парсинга группы VK нужно вводить короткое имя: его можно найти в "Подробная информация", зайдя на страницу сообщества.  
Выглядеть оно будет прмерно так @example. Нужно только example!

# Константы VK API
VK_TOKEN = 'your token (get it when creating the VK app)/// ваш токен (поличите при создании приложения VK) '
VK_VERSION = '5.199'

# Константы VK API
VK_TOKEN = 'your token (get it when creating the VK app)/// ваш токен (поличите при создании приложения VK) '
VK_VERSION = '5.199'

# Константы Reddit API
REDDIT_CLIENT_ID = 'поличите при создании приложения Reddit ///check out when creating a reddit app'
REDDIT_CLIENT_SECRET = 'поличите при создании приложения Reddit ///check out when creating a reddit app'
REDDIT_USER_AGENT = 'RedditParser by /u/YOUR NAME'

1. Получение токена для VK
Войдите в свой аккаунт VK.
Перейдите в раздел для разработчиков.
Нажмите на кнопку "Создать приложение".
Укажите название приложения.
Выберите тип приложения (например, "Standalone").
Укажите ссылку на сайт (можно указать что-то вроде https://example.com). Можно https://localhost.
После создания приложения:
Перейдите в настройки приложения. Можно по ссылке: [text](https://id.vk.com/about/business/go/accounts/156837/apps)
Выберите своё приложение и во вкладке "Приложение" будут все необходимые данные.

2. Получение ключей для Reddit
Войдите в свой аккаунт Reddit.
Перейдите на страницу Reddit App Preferences.
Прокрутите вниз и нажмите "Создать приложение" или "Create App".
Укажите название приложения.
Выберите тип приложения:
Для десктопных приложений — Installed App.
Для веб-приложений — Web App.
Укажите описание и URL (можно использовать http://localhost для локальной разработки).
После создания приложения:
Скопируйте Client ID (это строка под заголовком "personal use script").
Скопируйте Secret Key.
Укажите произвольное значение для User-Agent (например, RedditParser by /u/YOUR_USERNAME).

