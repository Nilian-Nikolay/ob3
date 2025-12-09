\# Комплексный план безопасности для проекта "Notes" (MEETOPIA / учебный пример)



Дата: 2025-11-26  

Основано на ПР №4 / настройки из ПР №5.



\## 1. Цели и требования безопасности

\- Защитить конфиденциальность данных пользователей (пароли, сессии).

\- Предотвратить типичные веб-атаки: XSS, CSRF, SQLi, Clickjacking.

\- Минимизировать утечки информации (заголовки Server, стек-трейсы).

\- Обеспечить контроль качества безопасности на этапе CI (SAST).

\- Поддерживать процесс регулярного тестирования (DAST, pentests).



\## 2. Оценка угроз (резюме на основе ранее проведённых тестов)

\- \*\*SQL Injection\*\* — обнаружены уязвимые endpoints `/vuln\_login`, `/vuln\_register` (сырые sqlite3-конкатенации). Риск: \*\*HIGH\*\*.

\- \*\*Debug mode / Werkzeug debugger\*\* — запуск `app.run(debug=True)` обнаружен Bandit (B201). Риск: \*\*HIGH\*\*.

\- \*\*Отсутствующие/слабые HTTP-заголовки безопасности\*\* — CSP, X-Frame-Options, X-Content-Type-Options, HSTS частично отсутствуют. Риск: \*\*MEDIUM\*\*.

\- \*\*Информационные утечки\*\* — заголовок `Server: Werkzeug/... Python/...` даёт версию сервера. Риск: \*\*LOW / MEDIUM\*\*.

\- \*\*CSRF\*\* — отсутствовала/не была настроена полноценно, исправлено через Flask-WTF (CSRFProtect).

\- \*\*XSS / пользовательский ввод\*\* — шаблоны Jinja2 по умолчанию экранируют, но присутствуют места с выводом user-controlled данных (проверить и не использовать `|safe`).



\## 3. Перечень реализованных мер защиты

Файлы/строки — \_конкретно где править в проекте\_:

\- `app.py`:

&nbsp; - CSRF: `from flask\_wtf.csrf import CSRFProtect` + `csrf.init\_app(app)` (в `create\_app()`). (строки: где инициализируется Flask)

&nbsp; - Заголовки безопасности: в `@app.after\_request` добавлены `Content-Security-Policy`, `X-Frame-Options: DENY`, `X-Content-Type-Options: nosniff`, `Referrer-Policy`, `Strict-Transport-Security`. (функция `add\_security\_headers`)

&nbsp; - Отключение debug при запуске: `app.run(debug=False)` (в `if \_\_name\_\_ == '\_\_main\_\_'`).

&nbsp; - Скрытие `Server`-заголовка: удаляем/заменяем `Server` в ответе: `if "Server" in response.headers: del response.headers\["Server"]`.

\- `forms.py` + `templates/\*`:

&nbsp; - Все формы используют `FlaskForm` и `{{ form.hidden\_tag() }}` — CSRF-токен включён.

&nbsp; - Валидация формы (WTForms validators) — минимальная проверка длины/наличия данных.

\- Для временной демонстрации и обучения: отдельные уязвимые endpoints (`/vuln\_login`, `/vuln\_register`) находятся в отдельном модуле/ветке — для демонстраций. Они НЕ должны попасть в production.

\- CI/CD: добавлен `security.yml` (GitHub Actions), запускает `bandit` и `pytest` и блокирует merge при `HIGH` проблемах.



\## 4. План регулярного тестирования (DevSecOps)

\- \*\*SAST (статический анализ)\*\*: Bandit запускается на каждом push и PR. Порог: блокировать при наличии `HIGH`/`CRITICAL`.

&nbsp; - Команда: `bandit -r . -f json -o bandit-report.json`

&nbsp; - Проверка: `tools/check\_bandit.py bandit-report.json` (exit non-zero при high).

\- \*\*DAST (динамический анализ)\*\*: Запуск ZAP вручную/на CI (по расписанию или перед релизом). Подготовить baseline report.

\- \*\*Автоматизированные тесты\*\*: `pytest` для unit tests. Запуск в CI.

\- \*\*Пентесты\*\*: периодические ручные pentests (раз в релиз/quarter).

\- \*\*Мониторинг и логирование\*\*: агрегировать логи (при продакшн) и хранить в безопасном месте.

\- \*\*Политики\*\*: установить правило branch protection в GitHub — require status checks (security.yml) и review.



\## 5. Контроль и реагирование

\- Если Bandit/pytest падают — PR не сливать, исправить в ветке.

\- При нахождении уязвимости — создать Issue, пометить severity и назначить ответственное лицо.



---



