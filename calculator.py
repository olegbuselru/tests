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

# Простые CSS стили
st.markdown("""
<style>
    .calendar-header {
        background-color: #1a1a1a;
        color: #00ff00;
        padding: 1rem;
        text-align: center;
        border: 2px solid #00ff00;
        margin-bottom: 1rem;
        font-family: monospace;
    }
    
    .calendar-container {
        background-color: #000;
        border: 2px solid #00ff00;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    .month-title {
        background-color: #00ff00;
        color: #000;
        padding: 0.5rem;
        text-align: center;
        font-weight: bold;
        margin-bottom: 1rem;
        font-family: monospace;
    }
    
    .weekday-header {
        background-color: #333;
        color: #00ff00;
        padding: 0.5rem;
        text-align: center;
        font-weight: bold;
        border: 1px solid #00ff00;
        font-family: monospace;
    }
    
    .calendar-day {
        background-color: #1a1a1a;
        color: #00ff00;
        padding: 0.5rem;
        text-align: center;
        border: 1px solid #00ff00;
        font-family: monospace;
        min-height: 60px;
    }
    
    .calendar-day:hover {
        background-color: #00ff00;
        color: #000;
    }
    
    .today {
        background-color: #00ff00 !important;
        color: #000 !important;
        font-weight: bold;
    }
    
    .holiday {
        background-color: #ff0000 !important;
        color: #fff !important;
        font-weight: bold;
    }
    
    .weekend {
        color: #0080ff !important;
    }
    
    .other-month {
        color: #666;
        background-color: #0a0a0a;
        border: 1px solid #333;
    }
    
    .stats-container {
        background-color: #1a1a1a;
        border: 2px solid #00ff00;
        padding: 1rem;
        margin-top: 1rem;
    }
    
    .stat-item {
        background-color: #000;
        border: 1px solid #00ff00;
        padding: 0.5rem;
        text-align: center;
        margin: 0.5rem;
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

def display_month_calendar(year, month):
    """Отображает календарь месяца используя Streamlit компоненты"""
    cal = calendar.monthcalendar(year, month)
    month_name = calendar.month_name[month]
    holidays = get_holidays(year, month)
    today = datetime.now()
    
    # Заголовок месяца
    st.markdown(f"""
    <div class="month-title">
        {month_name} {year}
    </div>
    """, unsafe_allow_html=True)
    
    # Дни недели
    weekdays = ['ПН', 'ВТ', 'СР', 'ЧТ', 'ПТ', 'СБ', 'ВС']
    cols = st.columns(7)
    
    for i, day in enumerate(weekdays):
        with cols[i]:
            st.markdown(f"""
            <div class="weekday-header">
                {day}
            </div>
            """, unsafe_allow_html=True)
    
    # Дни месяца
    for week in cal:
        cols = st.columns(7)
        for i, day in enumerate(week):
            with cols[i]:
                if day == 0:
                    st.markdown('<div class="calendar-day other-month"></div>', unsafe_allow_html=True)
                else:
                    # Определяем классы для дня
                    day_classes = ["calendar-day"]
                    
                    if year == today.year and month == today.month and day == today.day:
                        day_classes.append("today")
                    
                    if day in holidays:
                        day_classes.append("holiday")
                    
                    weekday = date(year, month, day).weekday()
                    if weekday >= 5:
                        day_classes.append("weekend")
                    
                    class_str = " ".join(day_classes)
                    
                    # Иконки
                    lunar_phase = get_lunar_phase(day)
                    weather_icon = get_weather_icon(day)
                    zodiac_sign = get_zodiac_sign(month, day)
                    
                    st.markdown(f"""
                    <div class="{class_str}">
                        <div style="font-size: 1.2rem; font-weight: bold;">{day}</div>
                        <div style="font-size: 0.8rem;">{lunar_phase}</div>
                        <div style="font-size: 0.8rem;">{weather_icon}</div>
                        <div style="font-size: 0.7rem;">{zodiac_sign}</div>
                    </div>
                    """, unsafe_allow_html=True)

# Главный заголовок
st.markdown("""
<div class="calendar-header">
    <h1>📅 КАЛЕНДАРЬ 2025 - PIXEL EDITION</h1>
    <p>Минималистичный календарь в стиле ретро</p>
</div>
""", unsafe_allow_html=True)

# Панель управления
col1, col2 = st.columns([3, 1])

with col1:
    option = st.radio("Что показать?", ["Весь год", "Один месяц"])

with col2:
    if st.button("🎲 Случайный месяц"):
        random_month = random.randint(1, 12)
        st.session_state.random_month = random_month

year = 2025

# Отображение календаря
if option == "Весь год":
    for month in range(1, 13):
        st.markdown('<div class="calendar-container">', unsafe_allow_html=True)
        display_month_calendar(year, month)
        st.markdown('</div>', unsafe_allow_html=True)

elif option == "Один месяц":
    month = st.selectbox("Выберите месяц", 
                        list(range(1, 13)), 
                        format_func=lambda x: calendar.month_name[x],
                        index=getattr(st.session_state, 'random_month', 0) - 1)
    
    st.markdown('<div class="calendar-container">', unsafe_allow_html=True)
    display_month_calendar(year, month)
    st.markdown('</div>', unsafe_allow_html=True)

# Статистика
st.markdown("""
<div class="stats-container">
    <h3 style="color: #00ff00; text-align: center;">📊 СТАТИСТИКА 2025</h3>
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="stat-item">
        <h4 style="color: #00ff00;">📅 Дней</h4>
        <p style="color: #fff; font-size: 1.5rem; font-weight: bold;">365</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="stat-item">
        <h4 style="color: #00ff00;">🎯 Год</h4>
        <p style="color: #fff; font-size: 1.5rem; font-weight: bold;">2025</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="stat-item">
        <h4 style="color: #00ff00;">🎉 Праздники</h4>
        <p style="color: #fff; font-size: 1.5rem; font-weight: bold;">8</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="stat-item">
        <h4 style="color: #00ff00;">🌙 Фазы луны</h4>
        <p style="color: #fff; font-size: 1.5rem; font-weight: bold;">12</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="stat-item">
        <h4 style="color: #00ff00;">🌤️ Погода</h4>
        <p style="color: #fff; font-size: 1.5rem; font-weight: bold;">365</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="stat-item">
        <h4 style="color: #00ff00;">♈ Знаки зодиака</h4>
        <p style="color: #fff; font-size: 1.5rem; font-weight: bold;">12</p>
    </div>
    """, unsafe_allow_html=True)

# Легенда
st.markdown("""
<div class="stats-container">
    <h4 style="color: #00ff00;">🎨 ЛЕГЕНДА</h4>
</div>
""", unsafe_allow_html=True)

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.markdown("""
    <div class="stat-item">
        <div style="background: #00ff00; width: 20px; height: 20px; margin: 0 auto;"></div>
        <p style="color: #00ff00; text-align: center;">🎯 Сегодня</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="stat-item">
        <div style="background: #ff0000; width: 20px; height: 20px; margin: 0 auto;"></div>
        <p style="color: #00ff00; text-align: center;">🎉 Праздники</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="stat-item">
        <div style="background: #0080ff; width: 20px; height: 20px; margin: 0 auto;"></div>
        <p style="color: #00ff00; text-align: center;">🌅 Выходные</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="stat-item">
        <div style="background: #1a1a1a; width: 20px; height: 20px; margin: 0 auto; border: 1px solid #00ff00;"></div>
        <p style="color: #00ff00; text-align: center;">📅 Обычные дни</p>
    </div>
    """, unsafe_allow_html=True)

with col5:
    st.markdown("""
    <div class="stat-item">
        <div style="background: #ff0000; width: 20px; height: 20px; margin: 0 auto;"></div>
        <p style="color: #00ff00; text-align: center;">🎯 Выбранный</p>
    </div>
    """, unsafe_allow_html=True)

# Информация
st.success("✅ Календарь загружен!")
st.info("🎮 Пиксельный стиль готов к работе")

