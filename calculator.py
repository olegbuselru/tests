import streamlit as st
import calendar
from datetime import datetime, date
import random

# Настройка страницы
st.set_page_config(
    page_title="Календарь 2025",
    page_icon="📅",
    layout="wide"
)

# Инициализация состояния
if 'selected_date' not in st.session_state:
    st.session_state.selected_date = None

# Минималистичные CSS стили
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600&display=swap');
    
    * {
        font-family: 'JetBrains Mono', monospace;
    }
    
    .pixel-header {
        background: #1a1a1a;
        color: #00ff00;
        padding: 2rem;
        text-align: center;
        border: 3px solid #00ff00;
        margin-bottom: 2rem;
        box-shadow: 5px 5px 0px #00ff00;
    }
    
    .pixel-header h1 {
        font-size: 2.5rem;
        margin: 0;
        text-shadow: 2px 2px 0px #000;
    }
    
    .pixel-header p {
        font-size: 1rem;
        margin: 1rem 0 0 0;
        opacity: 0.8;
    }
    
    .pixel-container {
        background: #000;
        border: 2px solid #00ff00;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 3px 3px 0px #00ff00;
    }
    
    .pixel-month-header {
        background: #00ff00;
        color: #000;
        padding: 1rem;
        text-align: center;
        font-weight: bold;
        font-size: 1.2rem;
        border: 2px solid #000;
        margin-bottom: 1rem;
    }
    
    .pixel-grid {
        display: grid;
        grid-template-columns: repeat(7, 1fr);
        gap: 2px;
        margin-top: 1rem;
    }
    
    .pixel-day {
        background: #1a1a1a;
        color: #00ff00;
        padding: 0.8rem 0.5rem;
        text-align: center;
        border: 1px solid #00ff00;
        cursor: pointer;
        font-weight: 500;
        min-height: 60px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        transition: all 0.2s ease;
    }
    
    .pixel-day:hover {
        background: #00ff00;
        color: #000;
        transform: scale(1.05);
    }
    
    .pixel-day.selected {
        background: #ff0000;
        color: #fff;
        border: 2px solid #fff;
    }
    
    .pixel-weekday {
        background: #333;
        color: #00ff00;
        padding: 0.8rem 0.5rem;
        text-align: center;
        font-weight: bold;
        border: 1px solid #00ff00;
        font-size: 0.9rem;
    }
    
    .pixel-today {
        background: #00ff00;
        color: #000;
        font-weight: bold;
        border: 2px solid #fff;
    }
    
    .pixel-holiday {
        background: #ff0000;
        color: #fff;
        font-weight: bold;
    }
    
    .pixel-weekend {
        background: #1a1a1a;
        color: #0080ff;
        border: 1px solid #0080ff;
    }
    
    .pixel-other-month {
        color: #666;
        background: #0a0a0a;
        border: 1px solid #333;
    }
    
    .pixel-controls {
        background: #1a1a1a;
        border: 2px solid #00ff00;
        padding: 1.5rem;
        margin-bottom: 2rem;
        box-shadow: 3px 3px 0px #00ff00;
    }
    
    .pixel-stats {
        background: #1a1a1a;
        border: 2px solid #00ff00;
        padding: 2rem;
        margin-top: 2rem;
        box-shadow: 3px 3px 0px #00ff00;
    }
    
    .pixel-stats h3 {
        color: #00ff00;
        text-align: center;
        margin-bottom: 1.5rem;
        font-size: 1.5rem;
    }
    
    .pixel-stats-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
    }
    
    .pixel-stat-item {
        background: #000;
        border: 1px solid #00ff00;
        padding: 1rem;
        text-align: center;
    }
    
    .pixel-stat-item h4 {
        color: #00ff00;
        margin: 0 0 0.5rem 0;
        font-size: 1rem;
    }
    
    .pixel-stat-item p {
        color: #fff;
        margin: 0;
        font-size: 1.2rem;
        font-weight: bold;
    }
    
    .pixel-legend {
        background: #1a1a1a;
        border: 2px solid #00ff00;
        padding: 1.5rem;
        margin-top: 2rem;
        box-shadow: 3px 3px 0px #00ff00;
    }
    
    .pixel-legend h4 {
        color: #00ff00;
        margin-bottom: 1rem;
        font-size: 1.2rem;
    }
    
    .pixel-legend-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 0.5rem;
    }
    
    .pixel-legend-item {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.5rem;
        background: #000;
        border: 1px solid #00ff00;
    }
    
    .pixel-legend-color {
        width: 20px;
        height: 20px;
        border: 1px solid #00ff00;
    }
    
    .pixel-legend-color.today { background: #00ff00; }
    .pixel-legend-color.holiday { background: #ff0000; }
    .pixel-legend-color.weekend { background: #0080ff; }
    .pixel-legend-color.normal { background: #1a1a1a; }
    .pixel-legend-color.selected { background: #ff0000; }
    
    .pixel-legend-item span {
        color: #00ff00;
        font-size: 0.9rem;
    }
    
    .pixel-info {
        background: #1a1a1a;
        border: 2px solid #00ff00;
        padding: 1rem;
        margin-top: 1rem;
        box-shadow: 3px 3px 0px #00ff00;
    }
    
    .pixel-info h4 {
        color: #00ff00;
        margin: 0 0 0.5rem 0;
    }
    
    .pixel-info p {
        color: #fff;
        margin: 0;
        font-size: 0.9rem;
    }
    
    @media (max-width: 768px) {
        .pixel-grid {
            gap: 1px;
        }
        
        .pixel-day {
            padding: 0.5rem 0.25rem;
            min-height: 50px;
            font-size: 0.9rem;
        }
        
        .pixel-header h1 {
            font-size: 2rem;
        }
    }
</style>
""", unsafe_allow_html=True)

def get_holidays(year, month):
    """Возвращает список праздников для месяца"""
    holidays = {
        1: [1, 7],  # Новый год, Рождество
        2: [23],    # День защитника Отечества
        3: [8],     # Международный женский день
        5: [1, 9],  # День труда, День Победы
        6: [12],    # День России
        11: [4],    # День народного единства
        12: [31]    # Новый год
    }
    return holidays.get(month, [])

def get_lunar_phase(day):
    """Возвращает фазу луны для дня"""
    phases = ["🌑", "🌒", "🌓", "🌔", "🌕", "🌖", "🌗", "🌘"]
    return phases[day % 8]

def get_weather_icon(day):
    """Возвращает иконку погоды"""
    weather = ["☀️", "⛅", "🌤️", "🌥️", "☁️", "🌦️", "🌧️", "⛈️"]
    return weather[day % len(weather)]

def get_zodiac_sign(month, day):
    """Возвращает знак зодиака"""
    zodiac_signs = [
        (1, 20, "♒"), (2, 19, "♓"), (3, 21, "♈"),
        (4, 20, "♉"), (5, 21, "♊"), (6, 21, "♋"),
        (7, 23, "♌"), (8, 23, "♍"), (9, 23, "♎"),
        (10, 23, "♏"), (11, 22, "♐"), (12, 22, "♑")
    ]
    
    for i, (start_month, start_day, sign) in enumerate(zodiac_signs):
        next_month, next_day, _ = zodiac_signs[(i + 1) % 12]
        if (month == start_month and day >= start_day) or (month == next_month and day < next_day):
            return sign
    return "♑"

def create_month_calendar_html(year, month):
    """Создает HTML календарь для месяца"""
    cal = calendar.monthcalendar(year, month)
    month_name = calendar.month_name[month]
    holidays = get_holidays(year, month)
    
    html = f"""
    <div class="pixel-container">
        <div class="pixel-month-header">
            {month_name} {year}
        </div>
        <div class="pixel-grid">
    """
    
    # Заголовки дней недели
    weekdays = ['ПН', 'ВТ', 'СР', 'ЧТ', 'ПТ', 'СБ', 'ВС']
    for day in weekdays:
        html += f'<div class="pixel-weekday">{day}</div>'
    
    # Дни месяца
    today = datetime.now()
    for week in cal:
        for day in week:
            if day == 0:
                html += '<div class="pixel-day pixel-other-month"></div>'
            else:
                day_classes = ["pixel-day"]
                
                # Проверяем, является ли это сегодняшним днем
                if year == today.year and month == today.month and day == today.day:
                    day_classes.append("pixel-today")
                
                # Проверяем, является ли это праздником
                if day in holidays:
                    day_classes.append("pixel-holiday")
                
                # Проверяем, является ли это выходным
                weekday = date(year, month, day).weekday()
                if weekday >= 5:
                    day_classes.append("pixel-weekend")
                
                # Проверяем, выбран ли этот день
                if st.session_state.selected_date and st.session_state.selected_date == (year, month, day):
                    day_classes.append("selected")
                
                class_str = " ".join(day_classes)
                
                # Добавляем иконки
                lunar_phase = get_lunar_phase(day)
                weather_icon = get_weather_icon(day)
                zodiac_sign = get_zodiac_sign(month, day)
                
                html += f'''
                <div class="{class_str}" onclick="selectDate({year}, {month}, {day})">
                    <div style="font-size: 1.1rem; font-weight: bold;">{day}</div>
                    <div style="font-size: 0.7rem; margin-top: 2px;">{lunar_phase}</div>
                    <div style="font-size: 0.7rem;">{weather_icon}</div>
                    <div style="font-size: 0.6rem; margin-top: 2px;">{zodiac_sign}</div>
                </div>
                '''
    
    html += "</div></div>"
    return html

def create_year_calendar_html(year):
    """Создает HTML календарь для всего года"""
    html = ""
    for month in range(1, 13):
        html += create_month_calendar_html(year, month)
    return html

# Простой JavaScript
st.markdown("""
<script>
function selectDate(year, month, day) {
    console.log('Selected:', year, month, day);
    // Простой визуальный эффект
    event.target.style.transform = 'scale(1.1)';
    setTimeout(() => {
        event.target.style.transform = 'scale(1)';
    }, 200);
}
</script>
""", unsafe_allow_html=True)

# Главный заголовок
st.markdown("""
<div class="pixel-header">
    <h1>📅 КАЛЕНДАРЬ 2025</h1>
    <p>PIXEL EDITION - Минималистичный календарь в стиле ретро</p>
</div>
""", unsafe_allow_html=True)

# Панель управления
with st.container():
    st.markdown('<div class="pixel-controls">', unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        option = st.radio("Что показать?", ["Весь год", "Один месяц"])
    
    with col2:
        if st.button("🎲 Случайный месяц"):
            random_month = random.randint(1, 12)
            st.session_state.random_month = random_month
    
    st.markdown('</div>', unsafe_allow_html=True)

year = 2025

if option == "Весь год":
    st.markdown(create_year_calendar_html(year), unsafe_allow_html=True)

elif option == "Один месяц":
    month = st.selectbox("Выберите месяц", 
                        list(range(1, 13)), 
                        format_func=lambda x: calendar.month_name[x],
                        index=getattr(st.session_state, 'random_month', 0) - 1)
    
    st.markdown(create_month_calendar_html(year, month), unsafe_allow_html=True)

# Статистика года
st.markdown("""
<div class="pixel-stats">
    <h3>📊 СТАТИСТИКА 2025</h3>
    <div class="pixel-stats-grid">
        <div class="pixel-stat-item">
            <h4>📅 Дней</h4>
            <p>365</p>
        </div>
        <div class="pixel-stat-item">
            <h4>🎯 Год</h4>
            <p>2025</p>
        </div>
        <div class="pixel-stat-item">
            <h4>🎉 Праздники</h4>
            <p>8</p>
        </div>
        <div class="pixel-stat-item">
            <h4>🌙 Фазы луны</h4>
            <p>12</p>
        </div>
        <div class="pixel-stat-item">
            <h4>🌤️ Погода</h4>
            <p>365</p>
        </div>
        <div class="pixel-stat-item">
            <h4>♈ Знаки зодиака</h4>
            <p>12</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Легенда
st.markdown("""
<div class="pixel-legend">
    <h4>🎨 ЛЕГЕНДА</h4>
    <div class="pixel-legend-grid">
        <div class="pixel-legend-item">
            <div class="pixel-legend-color today"></div>
            <span>🎯 Сегодня</span>
        </div>
        <div class="pixel-legend-item">
            <div class="pixel-legend-color holiday"></div>
            <span>🎉 Праздники</span>
        </div>
        <div class="pixel-legend-item">
            <div class="pixel-legend-color weekend"></div>
            <span>🌅 Выходные</span>
        </div>
        <div class="pixel-legend-item">
            <div class="pixel-legend-color normal"></div>
            <span>📅 Обычные дни</span>
        </div>
        <div class="pixel-legend-item">
            <div class="pixel-legend-color selected"></div>
            <span>🎯 Выбранный</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Информация о выбранной дате
if st.session_state.selected_date:
    year, month, day = st.session_state.selected_date
    zodiac_sign = get_zodiac_sign(month, day)
    
    st.markdown(f"""
    <div class="pixel-info">
        <h4>📅 Выбрана дата: {day} {calendar.month_name[month]} {year}</h4>
        <p>🌙 Фаза луны: {get_lunar_phase(day)} | 🌤️ Погода: {get_weather_icon(day)} | {zodiac_sign}</p>
    </div>
    """, unsafe_allow_html=True)

# Тестовое сообщение
st.success("✅ Календарь загружен!")
st.info("🎮 Пиксельный стиль готов к работе")

