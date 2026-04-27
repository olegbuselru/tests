import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

HOST = "0.0.0.0"
PORT = 8000
BASE_DIR = Path(__file__).parent

CHANNELS = [
    {"name": "Telegram News", "handle": "@telegram", "url": "https://t.me/telegram", "macro": 0, "micro": "Open Source", "subs": 1200000, "desc": "Официальный канал новостей Telegram."},
    {"name": "Pavel Durov", "handle": "@durov", "url": "https://t.me/durov", "macro": 0, "micro": "Backend", "subs": 950000, "desc": "Личный канал Павла Дурова о технологиях и продукте."},
    {"name": "Habr", "handle": "@habr_com", "url": "https://t.me/habr_com", "macro": 0, "micro": "Frontend", "subs": 210000, "desc": "Новости и статьи из мира IT."},
    {"name": "vc.ru", "handle": "@vcnews", "url": "https://t.me/vcnews", "macro": 1, "micro": "Стартапы", "subs": 480000, "desc": "Бизнес, финансы, стартапы и рынок."},
    {"name": "The Bell", "handle": "@thebell_io", "url": "https://t.me/thebell_io", "macro": 1, "micro": "Инвестиции", "subs": 340000, "desc": "Деловые новости, рынки и аналитика."},
    {"name": "Forbes Russia", "handle": "@forbesrussia", "url": "https://t.me/forbesrussia", "macro": 1, "micro": "VC", "subs": 300000, "desc": "Финансы, инвестиции и бизнес-аналитика."},
    {"name": "Meduza", "handle": "@meduzalive", "url": "https://t.me/meduzalive", "macro": 2, "micro": "Россия", "subs": 1300000, "desc": "Оперативные новости и политическая повестка."},
    {"name": "Коммерсантъ", "handle": "@kommersant", "url": "https://t.me/kommersant", "macro": 2, "micro": "Аналитика", "subs": 420000, "desc": "Новости политики и экономики."},
    {"name": "РБК", "handle": "@rbc_news", "url": "https://t.me/rbc_news", "macro": 2, "micro": "Европа", "subs": 900000, "desc": "Лента политических и экономических новостей."},
    {"name": "OpenAI", "handle": "@openai", "url": "https://t.me/openai", "macro": 3, "micro": "LLM", "subs": 250000, "desc": "Официальные анонсы OpenAI."},
    {"name": "Hugging Face", "handle": "@huggingface", "url": "https://t.me/huggingface", "macro": 3, "micro": "NLP", "subs": 90000, "desc": "Новости и релизы экосистемы AI."},
    {"name": "Data Science", "handle": "@data_science", "url": "https://t.me/data_science", "macro": 3, "micro": "Research", "subs": 150000, "desc": "Материалы по ML, DS и исследованиям."},
    {"name": "Cointelegraph", "handle": "@cointelegraph", "url": "https://t.me/cointelegraph", "macro": 4, "micro": "Bitcoin", "subs": 400000, "desc": "Мировые крипто-новости и аналитика."},
    {"name": "ForkLog", "handle": "@forklog", "url": "https://t.me/forklog", "macro": 4, "micro": "Web3", "subs": 300000, "desc": "Крипто и блокчейн-медиа на русском."},
    {"name": "Binance", "handle": "@binance", "url": "https://t.me/binance", "macro": 4, "micro": "DeFi", "subs": 600000, "desc": "Официальный канал Binance."},
    {"name": "BBC News", "handle": "@bbcrussian", "url": "https://t.me/bbcrussian", "macro": 5, "micro": "Новости", "subs": 700000, "desc": "Новости и репортажи BBC на русском."},
    {"name": "Tjournal", "handle": "@tjournal", "url": "https://t.me/tjournal", "macro": 5, "micro": "Журналистика", "subs": 200000, "desc": "Медиа и цифровая повестка."},
    {"name": "Mash", "handle": "@breakingmash", "url": "https://t.me/breakingmash", "macro": 5, "micro": "PR", "subs": 1500000, "desc": "Оперативные медиа-новости."},
    {"name": "Sports.ru", "handle": "@sportsru", "url": "https://t.me/sportsru", "macro": 6, "micro": "Футбол", "subs": 250000, "desc": "Спортивные новости и аналитика."},
    {"name": "Чемпионат", "handle": "@championat", "url": "https://t.me/championat", "macro": 6, "micro": "Баскетбол", "subs": 180000, "desc": "Новости спорта и репортажи."},
    {"name": "UFC", "handle": "@ufc", "url": "https://t.me/ufc", "macro": 6, "micro": "ММА", "subs": 500000, "desc": "Официальный канал UFC."},
    {"name": "Доктор Питер", "handle": "@doctorpiternews", "url": "https://t.me/doctorpiternews", "macro": 7, "micro": "Медицина", "subs": 120000, "desc": "Новости медицины и здоровья."},
    {"name": "Психология", "handle": "@psychologies", "url": "https://t.me/psychologies", "macro": 7, "micro": "Психология", "subs": 95000, "desc": "Практики психологии и ментального здоровья."},
    {"name": "Зожник", "handle": "@zozhnik", "url": "https://t.me/zozhnik", "macro": 7, "micro": "Питание", "subs": 110000, "desc": "ЗОЖ, питание и спортмед."},
    {"name": "Нетология", "handle": "@netologyru", "url": "https://t.me/netologyru", "macro": 8, "micro": "Курсы", "subs": 85000, "desc": "Образовательные материалы и курсы."},
    {"name": "Skillbox", "handle": "@skillboxru", "url": "https://t.me/skillboxru", "macro": 8, "micro": "Программирование", "subs": 130000, "desc": "Курсы, карьера, образование."},
    {"name": "Stepik", "handle": "@stepikorg", "url": "https://t.me/stepikorg", "macro": 8, "micro": "EdTech", "subs": 70000, "desc": "Онлайн-образование и новые программы."},
    {"name": "Кинопоиск", "handle": "@kinopoisk", "url": "https://t.me/kinopoisk", "macro": 9, "micro": "Кино", "subs": 260000, "desc": "Новости кино и сериалов."},
    {"name": "DTF", "handle": "@dtfbest", "url": "https://t.me/dtfbest", "macro": 9, "micro": "Игры", "subs": 210000, "desc": "Игры, развлечения и индустрия."},
    {"name": "2x2", "handle": "@tv2x2", "url": "https://t.me/tv2x2", "macro": 9, "micro": "Аниме", "subs": 90000, "desc": "Поп-культура, юмор и аниме."},
    {"name": "NASA", "handle": "@nasa", "url": "https://t.me/nasa", "macro": 10, "micro": "Космос", "subs": 1800000, "desc": "Официальные новости NASA."},
    {"name": "PostNauka", "handle": "@postnauka", "url": "https://t.me/postnauka", "macro": 10, "micro": "Физика", "subs": 150000, "desc": "Научно-популярные материалы."},
    {"name": "N + 1", "handle": "@nplusone", "url": "https://t.me/nplusone", "macro": 10, "micro": "Биология", "subs": 340000, "desc": "Научные новости и разборы."},
    {"name": "Aviasales", "handle": "@aviasales", "url": "https://t.me/aviasales", "macro": 11, "micro": "Лайфхаки", "subs": 500000, "desc": "Путешествия, билеты, лайфхаки."},
    {"name": "Туту", "handle": "@tutu_travel", "url": "https://t.me/tutu_travel", "macro": 11, "micro": "Визы", "subs": 80000, "desc": "Маршруты, визы и поездки."},
    {"name": "National Geographic", "handle": "@natgeo", "url": "https://t.me/natgeo", "macro": 11, "micro": "Фото", "subs": 400000, "desc": "Путешествия и фото со всего мира."},
]


class AppHandler(BaseHTTPRequestHandler):
    def _send_json(self, payload: dict, status: int = 200):
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_file(self, path: Path, content_type: str):
        if not path.exists():
            self.send_error(404, "Not found")
            return
        data = path.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):  # noqa: N802
        if self.path in ("/", "/index.html"):
            return self._send_file(BASE_DIR / "static" / "index.html", "text/html; charset=utf-8")
        if self.path == "/api/channels":
            return self._send_json({"channels": CHANNELS})
        if self.path.startswith("/static/"):
            file_path = BASE_DIR / self.path.lstrip("/")
            ctype = "text/plain; charset=utf-8"
            if file_path.suffix == ".js":
                ctype = "application/javascript; charset=utf-8"
            elif file_path.suffix == ".css":
                ctype = "text/css; charset=utf-8"
            elif file_path.suffix == ".html":
                ctype = "text/html; charset=utf-8"
            return self._send_file(file_path, ctype)
        self.send_error(404, "Not found")


def run():
    server = HTTPServer((HOST, PORT), AppHandler)
    print(f"Serving on http://{HOST}:{PORT}")
    server.serve_forever()


if __name__ == "__main__":
    run()
