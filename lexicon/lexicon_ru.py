MENU_COMMANDS_RU: dict[str, str] = {
    '/project': 'Получить информацию о проекте',
    '/top': 'Списки худших и лучших',
    '/aqi': 'Узнать качество воздуха',
    '/stat': 'Статистика',

}

LEXICON_RU: dict[str, str] = {
    '/start': '<b>Добрый день!</b>\n\nЭто бот для проекта '
              'МОВС 2023 - Анализ качества воздуха '
              '\n\nЧтобы посмотреть список доступных '
              'команд - обратитесь к меню. \n\n'
              'Чтобы узнать о возможностях в текстовом формате - наберите /help',
    'no_echo': 'Данный формат сообщений не поддерживается',
    '/help': 'Этот бот создан в рамках проекта по определению индекса качества воздуха. Он умеет:\n\n'
             '✅ Отправлять вас в gitHub\n\n'
             '✅ Связывать вас с автором\n\n'
             'Пока не умеет:\n\n'
             '❌ Делать предсказания по целому файлу\n\n'
             '❌ Работать с api для получения данных',
    'not admin': 'Увы, у вас нет доступа, так как вы не администратор.'
}
