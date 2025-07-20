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
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = False
if 'selected_date' not in st.session_state:
    st.session_state.selected_date = None

# CSS стили для красивого дизайна
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .dark-mode {
        background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%);
        color: #ffffff;
    }
    
    .dark-mode .calendar-container {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .dark-mode .calendar-day {
        background: linear-gradient(145deg, #2a2a3e, #1e1e2e);
        color: #ffffff;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .dark-mode .calendar-day:hover {
        background: linear-gradient(145deg, #667eea, #764ba2);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.6);
    }
    
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        padding: 3rem 2rem;
        border-radius: 25px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
        box-shadow: 0 25px 50px rgba(102, 126, 234, 0.4);
        position: relative;
        overflow: hidden;
        animation: float 6s ease-in-out infinite;
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grain" width="100" height="100" patternUnits="userSpaceOnUse"><circle cx="25" cy="25" r="1" fill="white" opacity="0.1"/><circle cx="75" cy="75" r="1" fill="white" opacity="0.1"/><circle cx="50" cy="10" r="0.5" fill="white" opacity="0.1"/><circle cx="10" cy="50" r="0.8" fill="white" opacity="0.1"/><circle cx="90" cy="30" r="0.3" fill="white" opacity="0.1"/></pattern></defs><rect width="100" height="100" fill="url(%23grain)"/></svg>');
        pointer-events: none;
    }
    
    .main-header::after {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(45deg, transparent, rgba(255,255,255,0.1), transparent);
        transform: rotate(45deg);
        animation: shimmer 4s infinite;
    }
    
    .main-header h1 {
        font-size: 3.5rem;
        font-weight: 800;
        margin: 0;
        text-shadow: 0 8px 16px rgba(0,0,0,0.3);
        animation: fadeInUp 1.5s ease-out;
        background: linear-gradient(45deg, #ffffff, #f0f0f0);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .main-header p {
        font-size: 1.3rem;
        margin: 1rem 0 0 0;
        opacity: 0.95;
        animation: fadeInUp 1.5s ease-out 0.3s both;
        font-weight: 300;
    }
    
    .controls-container {
        background: linear-gradient(145deg, #ffffff, #f8f9fa);
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.1);
        margin-bottom: 2rem;
        border: 1px solid rgba(102, 126, 234, 0.1);
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 1rem;
    }
    
    .dark-mode .controls-container {
        background: linear-gradient(145deg, rgba(255,255,255,0.05), rgba(255,255,255,0.02));
        border: 1px solid rgba(255,255,255,0.1);
    }
    
    .theme-toggle {
        background: linear-gradient(135deg, #667eea, #764ba2);
        border: none;
        padding: 0.75rem 1.5rem;
        border-radius: 25px;
        color: white;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.3);
    }
    
    .theme-toggle:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
    }
    
    .calendar-container {
        background: white;
        border-radius: 25px;
        padding: 2.5rem;
        box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        margin: 2rem 0;
        border: 1px solid rgba(255,255,255,0.2);
        backdrop-filter: blur(15px);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .calendar-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #667eea, #764ba2, #f093fb);
        border-radius: 25px 25px 0 0;
    }
    
    .calendar-container:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 0 30px 60px rgba(0,0,0,0.15);
    }
    
    .month-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        font-weight: 600;
        margin-bottom: 2rem;
        position: relative;
        overflow: hidden;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
    }
    
    .month-header::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(45deg, transparent, rgba(255,255,255,0.1), transparent);
        transform: rotate(45deg);
        animation: shimmer 3s infinite;
    }
    
    .month-header h2 {
        margin: 0;
        font-size: 2rem;
        position: relative;
        z-index: 1;
        text-shadow: 0 4px 8px rgba(0,0,0,0.3);
    }
    
    .calendar-grid {
        display: grid;
        grid-template-columns: repeat(7, 1fr);
        gap: 10px;
        margin-top: 1.5rem;
    }
    
    .calendar-day {
        background: linear-gradient(145deg, #f8f9fa, #e9ecef);
        padding: 1.2rem 0.5rem;
        text-align: center;
        border-radius: 15px;
        border: 2px solid transparent;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        cursor: pointer;
        position: relative;
        overflow: hidden;
        font-weight: 600;
        min-height: 70px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        font-size: 1.1rem;
    }
    
    .calendar-day:hover {
        background: linear-gradient(145deg, #667eea, #764ba2);
        color: white;
        transform: translateY(-5px) scale(1.08);
        box-shadow: 0 15px 35px rgba(102, 126, 234, 0.5);
        border-color: rgba(255,255,255,0.3);
        z-index: 10;
    }
    
    .calendar-day::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
        transition: left 0.6s;
    }
    
    .calendar-day:hover::before {
        left: 100%;
    }
    
    .calendar-day.selected {
        background: linear-gradient(145deg, #ff6b6b, #ee5a24) !important;
        color: white !important;
        transform: scale(1.1);
        box-shadow: 0 15px 35px rgba(255, 107, 107, 0.5) !important;
        animation: bounce 0.6s ease-in-out;
    }
    
    .weekday-header {
        background: linear-gradient(135deg, #495057, #343a40);
        color: white;
        padding: 1.2rem 0.5rem;
        text-align: center;
        border-radius: 15px;
        font-weight: 700;
        font-size: 1rem;
        text-transform: uppercase;
        letter-spacing: 2px;
        box-shadow: 0 8px 20px rgba(0,0,0,0.2);
        position: relative;
        overflow: hidden;
    }
    
    .weekday-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        transition: left 0.5s;
    }
    
    .weekday-header:hover::before {
        left: 100%;
    }
    
    .today {
        background: linear-gradient(145deg, #28a745, #20c997) !important;
        color: white !important;
        font-weight: bold !important;
        box-shadow: 0 15px 35px rgba(40, 167, 69, 0.5) !important;
        animation: pulse 2s infinite;
        position: relative;
    }
    
    .today::after {
        content: '🎯';
        position: absolute;
        top: 5px;
        right: 5px;
        font-size: 0.8rem;
    }
    
    .holiday {
        background: linear-gradient(145deg, #dc3545, #fd7e14) !important;
        color: white !important;
        font-weight: bold !important;
        position: relative;
    }
    
    .holiday::after {
        content: '🎉';
        position: absolute;
        top: 5px;
        right: 5px;
        font-size: 0.8rem;
    }
    
    .weekend {
        background: linear-gradient(145deg, #e3f2fd, #bbdefb);
        color: #1976d2;
        position: relative;
    }
    
    .weekend::after {
        content: '🌅';
        position: absolute;
        top: 5px;
        right: 5px;
        font-size: 0.8rem;
    }
    
    .other-month {
        color: #adb5bd;
        background: #f8f9fa;
        opacity: 0.4;
    }
    
    .lunar-phase {
        font-size: 0.7rem;
        margin-top: 0.2rem;
        opacity: 0.8;
    }
    
    .weather-icon {
        font-size: 0.8rem;
        margin-top: 0.2rem;
    }
    
    .stats-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 3rem;
        border-radius: 25px;
        margin-top: 3rem;
        text-align: center;
        position: relative;
        overflow: hidden;
        box-shadow: 0 20px 40px rgba(102, 126, 234, 0.3);
    }
    
    .stats-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="stats-pattern" width="50" height="50" patternUnits="userSpaceOnUse"><circle cx="25" cy="25" r="1" fill="white" opacity="0.1"/></pattern></defs><rect width="100" height="100" fill="url(%23stats-pattern)"/></svg>');
        pointer-events: none;
    }
    
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 2rem;
        margin-top: 2rem;
        position: relative;
        z-index: 1;
    }
    
    .stat-item {
        background: rgba(255,255,255,0.15);
        padding: 2rem;
        border-radius: 20px;
        backdrop-filter: blur(15px);
        border: 1px solid rgba(255,255,255,0.2);
        transition: all 0.3s ease;
    }
    
    .stat-item:hover {
        transform: translateY(-5px);
        background: rgba(255,255,255,0.25);
    }
    
    .stat-item h4 {
        margin: 0 0 1rem 0;
        font-size: 1.2rem;
        font-weight: 600;
    }
    
    .stat-item p {
        margin: 0;
        font-size: 1.5rem;
        font-weight: 700;
    }
    
    .legend-container {
        background: linear-gradient(145deg, #ffffff, #f8f9fa);
        padding: 2rem;
        border-radius: 20px;
        margin-top: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        border: 1px solid rgba(102, 126, 234, 0.1);
    }
    
    .dark-mode .legend-container {
        background: linear-gradient(145deg, rgba(255,255,255,0.05), rgba(255,255,255,0.02));
        border: 1px solid rgba(255,255,255,0.1);
    }
    
    .legend-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
    }
    
    .legend-item {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.5rem;
        border-radius: 10px;
        background: rgba(102, 126, 234, 0.1);
    }
    
    .legend-color {
        width: 20px;
        height: 20px;
        border-radius: 50%;
        border: 2px solid rgba(255,255,255,0.3);
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(50px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes shimmer {
        0% { transform: translateX(-100%) rotate(45deg); }
        100% { transform: translateX(100%) rotate(45deg); }
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }
    
    @keyframes bounce {
        0%, 20%, 53%, 80%, 100% { transform: scale(1.1); }
        40%, 43% { transform: scale(1.15); }
        70% { transform: scale(1.05); }
        90% { transform: scale(1.1); }
    }
    
    @media (max-width: 768px) {
        .calendar-grid {
            gap: 5px;
        }
        
        .calendar-day {
            padding: 0.8rem 0.3rem;
            min-height: 60px;
            font-size: 1rem;
        }
        
        .main-header h1 {
            font-size: 2.5rem;
        }
        
        .controls-container {
            flex-direction: column;
            text-align: center;
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
    """Возвращает фазу луны для дня (упрощенная версия)"""
    phases = ["🌑", "🌒", "🌓", "🌔", "🌕", "🌖", "🌗", "🌘"]
    return phases[day % 8]

def get_weather_icon(day):
    """Возвращает иконку погоды (упрощенная версия)"""
    weather = ["☀️", "⛅", "🌤️", "🌥️", "☁️", "🌦️", "🌧️", "⛈️"]
    return weather[day % 8]

def create_month_calendar_html(year, month):
    """Создает HTML календарь для месяца"""
    cal = calendar.monthcalendar(year, month)
    month_name = calendar.month_name[month]
    holidays = get_holidays(year, month)
    
    html = f"""
    <div class="calendar-container">
        <div class="month-header">
            <h2>{month_name} {year}</h2>
        </div>
        <div class="calendar-grid">
    """
    
    # Заголовки дней недели
    weekdays = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']
    for day in weekdays:
        html += f'<div class="weekday-header">{day}</div>'
    
    # Дни месяца
    today = datetime.now()
    for week in cal:
        for day in week:
            if day == 0:
                html += '<div class="calendar-day other-month"></div>'
            else:
                day_classes = ["calendar-day"]
                
                # Проверяем, является ли это сегодняшним днем
                if year == today.year and month == today.month and day == today.day:
                    day_classes.append("today")
                
                # Проверяем, является ли это праздником
                if day in holidays:
                    day_classes.append("holiday")
                
                # Проверяем, является ли это выходным (суббота или воскресенье)
                weekday = date(year, month, day).weekday()
                if weekday >= 5:  # 5 = суббота, 6 = воскресенье
                    day_classes.append("weekend")
                
                # Проверяем, выбран ли этот день
                if st.session_state.selected_date and st.session_state.selected_date == (year, month, day):
                    day_classes.append("selected")
                
                class_str = " ".join(day_classes)
                
                # Добавляем иконки
                lunar_phase = get_lunar_phase(day)
                weather_icon = get_weather_icon(day)
                
                html += f'''
                <div class="{class_str}" onclick="selectDate({year}, {month}, {day})">
                    {day}
                    <div class="lunar-phase">{lunar_phase}</div>
                    <div class="weather-icon">{weather_icon}</div>
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

# JavaScript для интерактивности
st.markdown("""
<script>
function selectDate(year, month, day) {
    // Отправляем данные в Streamlit
    fetch('/_stcore/forward', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            'selected_date': [year, month, day]
        })
    });
}
</script>
""", unsafe_allow_html=True)

# Главный заголовок
st.markdown("""
<div class="main-header">
    <h1>📅 Календарь 2025</h1>
    <p>Интерактивный календарь с погодой, фазами луны и праздниками</p>
</div>
""", unsafe_allow_html=True)

# Панель управления
with st.container():
    st.markdown('<div class="controls-container">', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        option = st.radio("Что показать?", ["Весь год", "Один месяц"])
    
    with col2:
        if st.button("🌙 Темная тема" if not st.session_state.dark_mode else "☀️ Светлая тема"):
            st.session_state.dark_mode = not st.session_state.dark_mode
    
    with col3:
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
<div class="stats-container">
    <h3>📊 Статистика 2025 года</h3>
    <div class="stats-grid">
        <div class="stat-item">
            <h4>📅 Всего дней</h4>
            <p>365 дней</p>
        </div>
        <div class="stat-item">
            <h4>🎯 Текущий год</h4>
            <p>2025</p>
        </div>
        <div class="stat-item">
            <h4>🎉 Праздники</h4>
            <p>8 официальных</p>
        </div>
        <div class="stat-item">
            <h4>⭐ Особый год</h4>
            <p>Год технологий</p>
        </div>
        <div class="stat-item">
            <h4>🌙 Фазы луны</h4>
            <p>12 полных</p>
        </div>
        <div class="stat-item">
            <h4>🌤️ Погода</h4>
            <p>365 дней</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Легенда
st.markdown("""
<div class="legend-container">
    <h4>🎨 Легенда календаря</h4>
    <div class="legend-grid">
        <div class="legend-item">
            <div class="legend-color" style="background: linear-gradient(145deg, #28a745, #20c997);"></div>
            <span>🎯 Сегодня - зеленый с пульсацией</span>
        </div>
        <div class="legend-item">
            <div class="legend-color" style="background: linear-gradient(145deg, #dc3545, #fd7e14);"></div>
            <span>🎉 Праздники - красный градиент</span>
        </div>
        <div class="legend-item">
            <div class="legend-color" style="background: linear-gradient(145deg, #e3f2fd, #bbdefb);"></div>
            <span>🌅 Выходные - синий градиент</span>
        </div>
        <div class="legend-item">
            <div class="legend-color" style="background: linear-gradient(145deg, #f8f9fa, #e9ecef);"></div>
            <span>📅 Обычные дни - серый градиент</span>
        </div>
        <div class="legend-item">
            <div class="legend-color" style="background: linear-gradient(145deg, #ff6b6b, #ee5a24);"></div>
            <span>🎯 Выбранный день - оранжевый</span>
        </div>
        <div class="legend-item">
            <div class="legend-color" style="background: transparent; border: 2px solid #667eea;"></div>
            <span>🌙 Фазы луны и погода</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Информация о выбранной дате
if st.session_state.selected_date:
    year, month, day = st.session_state.selected_date
    st.success(f"📅 Выбрана дата: {day} {calendar.month_name[month]} {year}")
    st.info(f"🌙 Фаза луны: {get_lunar_phase(day)} | 🌤️ Погода: {get_weather_icon(day)}")

