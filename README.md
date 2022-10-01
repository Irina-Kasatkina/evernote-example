# Консольные утилиты для работы с заметками Evernote

Этот набор скриптов предназначен для для работы с API [Evernote](https://evernote.com/intl/ru) - веб-сервиса для создания и хранения заметок:
- *list_notebooks.py* - выводит в консоль список всех блокнотов, хранящихся в вашем аккаунте Evernote;
- *dump_inbox.py* - выводит в консоль список заметок из конкретного блокнота Evernote;
- *add_note2journal* - создаёт запись по указанному шаблону и сохраняет ее в указанном блокноте Evernote.

## Установка

Для запуска скриптов вам понадобится Python 3.

Скачайте код с GitHub.

Для управления зависимостями Python желательно воспользоваться [virtualenv](https://pypi.org/project/virtualenv/).

Установите зависимости с помощью `pip` (или `pip3`, есть конфликт с Python2):
```
pip install -r requirements.txt
```

## Переменные окружения

Часть настроек утилит берётся из переменных окружения. Чтобы их определить, создайте файл `.env` в той же папке, где и скрипты, и запишите туда данные в таком формате: `ПЕРЕМЕННАЯ=значение`.

Доступно 6 переменных:

- `SANDBOX` - признак того, что как разработчик вы будете работать в "песочнице" (тестовом сервере для разработчиков) Evernote. Например: `SANDBOX=True`. Если вы собираетесь использовать утилиты на основном сервере Evernote, то установите значение `SANDBOX=False`.

- `EVERNOTE_SANDBOX_PERSONAL_TOKEN` - токен разработчика для работы в песочнице Evernote. Скрипты будут использовать его, если `SANDBOX=True`. Получить этот токен можно на сайте согласно [Инструкции](https://dev.evernote.com/doc/articles/dev_tokens.php);

- `EVERNOTE_PRODUCTION_PERSONAL_TOKEN` - токен разработчика для работы с продакшен сервером Evernote. Скрипты будут использовать его, если `SANDBOX=False`. Получение этого токена на сайте на данный момент закрыто, но согласно [Информации с форума](https://discussion.evernote.com/forums/topic/113349-developer-token-requests/) получить его можно, обратившись в службу поддержки.

- `INBOX_NOTEBOOK_GUID` - GUID блокнота на сайте Evernote, из которого выводит заметки скрипт `dump_inbox`.

- `JOURNAL_TEMPLATE_NOTE_GUID` - GUID заметки на сайте Evernote, которая будет использоваться скриптом `add_note2journal` как шаблон для создания других заметок.

- `JOURNAL_NOTEBOOK_GUID` - GUID блокнота на сайте Evernote, который будет использоваться скриптом `add_note2journal` для записи в этот блокнот заметок, генерируемых им по шаблону заметки с GUID, равным значению переменной окружения `JOURNAL_TEMPLATE_NOTE_GUID`.

## Запуск и описание работы скриптов

Для того, чтобы работать со скриптами, вам нужно получить на Evernote и занести в файл `.env` один из токенов `EVERNOTE_SANDBOX_PERSONAL_TOKEN` или `EVERNOTE_SANDBOX_PRODUCTION_TOKEN`, а также установить соответствующее значение переменной окружения `SANDBOX` в файле `.env`. Способ получения и занесения в файл `.env` этих токенов описан выше в разделе `Переменные окружения`.

### list_notebooks

Вывод в консоль списка блокнотов Evernote.

Для запуска скрипта наберите в командной строке консоли `cmd` команду:
```
python list_notebooks.py
```

Скрипт сделает запрос к API Evernote и выведет в консоль список всех блокнотов (GUID и заголовок), хранящихся в вашем аккаунте.
Например,
```
2dc0va53-2716-40s9-b60a-c1917683k9d9 - Первый блокнот
```

### dump_inbox

Вывод в консоль заметок из конкретного блокнота Evernote.

Для того, чтобы работать с этим скриптом, нужно, чтобы на сайте Evernote у вас имелся блокнот, в котором есть записи. 

Для создания блокнота и записей в нём:

1. Перейдите в браузере либо в [песочницу Evernote](https://sandbox.evernote.com/shard/s1/notestore) (если в файле `.env` вы установили `SANDBOX=True`), либо на [основной сайт Evernote](https://evernote.com/) (если в файле `.env` вы установили `SANDBOX=False`).

2. Создайте на сайте любой блокнот и любые записи в нём. 

3. Запустите скрипт `list_notebooks` и запишите GUID созданного вами блокнота в качестве значения переменной окружения `INBOX_NOTEBOOK_GUID` в файл `.env`. 

После этого можно запустить скрипт `dump_inbox`. Для запуска скрипта наберите в командной строке консоли команду:
```
python dump_inbox.py
```

Скрипт выведет в консоль GUID'ы и тексты заметок, которые вы вводили в созданный вами блокнот. Например,
```
--------- 1 ---------
Note GUID: 86c2366e-4691-4098-9527-d5c165dc8463e
Note title: My second note in Diary notebook
Text 1 of my second note in Diary notebook

--------- 2 ---------
Note GUID: 0477383c-524b-48bd-94d4-0d5eb67fc6ef
Note title: My first note in Diary notebook
Text 1 of my first note in Diary notebook
Text 2 of my first note in Diary notebook
```

#### Параметры командной строки

1. По умолчанию скрипт `dump_inbox` выводит 10 последних заметок. Но при запуске скрипта можно передать ему в качестве первого параметра командной строки число - максимальное количество выводимых заметок.

2. Как уже было сказано, GUID блокнота, из которого выводятся заметки, скрипт `dump_inbox` берёт из переменной окружения `INBOX_NOTEBOOK_GUID` в файле `.env`. Но также можно при запуске скрипта передать ему в качестве второго параметра командной строки GUID любого нужного вам блокнота, и тогда скрипт возьмёт этот параметр из командной строки.

### add_note2journal

Cоздание записи по указанному шаблону и сохранение ее в блокноте Evernote.

Для того, чтобы работать с этим скриптом, нужно, чтобы на сайте Evernote у вас, во-первых, имелась заметка, которую скрипт будет использовать в качестве шаблона, и во-вторых, блокнот (например, с именем `Дневник`), в который он будет записывать сгенерированные им по этому шаблону заметки.

Для этого:

1. Перейдите в браузере либо в [песочницу Evernote](https://sandbox.evernote.com/shard/s1/notestore) (если в файле `.env` вы установили `SANDBOX=True`), либо на [основной сайт Evernote](https://evernote.com/) (если в файле `.env` вы установили `SANDBOX=False`).

2. Создайте на сайте блокнот (например, `Дневник`).

3. Запустите скрипт `list_notebooks` и запишите GUID блокнота (например, "Дневник") в качестве значения переменной окружения `JOURNAL_NOTEBOOK_GUID` в файл `.env`.

4. Создайте на сайте заметку с заголовком "Заметка {date} {dow} # шаблон", которую скрипт будет использовать в качестве шаблона.

5. Запустите скрипт `dump_inbox`, указав в качестве второго параметра командной строки GUID того блокнота, в котором вы создали заметку-шаблон) - например,
```
python dump_inbox.py 10 3dc0va53-2716-40s9-b60a-c1917683k9d9
```
6. Запишите GUID заметки-шаблона (выведенный на экран консоли на предыдущем шаге) в качестве значения переменной окружения `JOURNAL_TEMPLATE_NOTE_GUID` в файл `.env`.

После этого можно запустить скрипт `add_note2journal`. Для запуска скрипта наберите в командной строке консоли команду:
```
python add_note2journal.py
```
Скрипт создаст заметку согласно шаблону (впишет в заголовок сегодняшнюю дату), сохранит её в блокноте "Дневник" на сайте Evernote и напечатает в консоли сообщение об успешном завершении своей работы - например:
<!-- {% raw %} -->
```
Title Context is:
{
    "date": "2022-10-01",
    "dow": "суббота"
}
Note created: Заметка 2022-10-01 суббота
Done
```
<!-- {% endraw %} -->

#### Параметр командной строки

По умолчанию скрипт `add_note2journal` заносит в заголовок заметки сегодняшнюю дату вместо `{date}` в шаблоне. Однако в качестве параметра командной строки можно указать другую дату - в формате `YYYY-MM-DD` - и тогда в заметку будет занесена именно дата из командной строки.