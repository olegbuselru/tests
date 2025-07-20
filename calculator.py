import streamlit as st
import calendar
from datetime import datetime, date

# Настройка страницы
st.set_page_config(
    page_title="Календарь 2025",
    page_icon="📅",
    layout="wide"
)

# CSS стили для красивого дизайна
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        padding: 3rem 2rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
        box-shadow: 0 20px 40px rgba(102, 126, 234, 0.3);
        position: relative;
        overflow: hidden;
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grain" width="100" height="100" patternUnits="userSpaceOnUse"><circle cx="25" cy="25" r="1" fill="white" opacity="0.1"/><circle cx="75" cy="75" r="1" fill="white" opacity="0.1"/><circle cx="50" cy="10" r="0.5" fill="white" opacity="0.1"/></pattern></defs><rect width="100" height="100" fill="url(%23grain)"/></svg>');
        pointer-events: none;
    }
    
    .main-header h1 {
        font-size: 3rem;
        font-weight: 700;
        margin: 0;
        text-shadow: 0 4px 8px rgba(0,0,0,0.3);
        animation: fadeInUp 1s ease-out;
    }
    
    .main-header p {
        font-size: 1.2rem;
        margin: 1rem 0 0 0;
        opacity: 0.9;
        animation: fadeInUp 1s ease-out 0.2s both;
    }
    
    .calendar-container {
        background: white;
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        margin: 1.5rem 0;
        border: 1px solid rgba(255,255,255,0.2);
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
    }
    
    .calendar-container:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 40px rgba(0,0,0,0.15);
    }
    
    .month-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        font-weight: 600;
        margin-bottom: 1.5rem;
        position: relative;
        overflow: hidden;
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
        font-size: 1.8rem;
        position: relative;
        z-index: 1;
    }
    
    .calendar-grid {
        display: grid;
        grid-template-columns: repeat(7, 1fr);
        gap: 8px;
        margin-top: 1rem;
    }
    
    .calendar-day {
        background: linear-gradient(145deg, #f8f9fa, #e9ecef);
        padding: 1rem 0.5rem;
        text-align: center;
        border-radius: 12px;
        border: 2px solid transparent;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        cursor: pointer;
        position: relative;
        overflow: hidden;
        font-weight: 500;
        min-height: 60px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    .calendar-day:hover {
        background: linear-gradient(145deg, #667eea, #764ba2);
        color: white;
        transform: translateY(-3px) scale(1.05);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
        border-color: rgba(255,255,255,0.3);
    }
    
    .calendar-day::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        transition: left 0.5s;
    }
    
    .calendar-day:hover::before {
        left: 100%;
    }
    
    .weekday-header {
        background: linear-gradient(135deg, #495057, #343a40);
        color: white;
        padding: 1rem 0.5rem;
        text-align: center;
        border-radius: 12px;
        font-weight: 600;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    .today {
        background: linear-gradient(145deg, #28a745, #20c997) !important;
        color: white !important;
        font-weight: bold !important;
        box-shadow: 0 8px 25px rgba(40, 167, 69, 0.4) !important;
        animation: pulse 2s infinite;
    }
    
    .holiday {
        background: linear-gradient(145deg, #dc3545, #fd7e14) !important;
        color: white !important;
        font-weight: bold !important;
    }
    
    .weekend {
        background: linear-gradient(145deg, #e3f2fd, #bbdefb);
        color: #1976d2;
    }
    
    .other-month {
        color: #adb5bd;
        background: #f8f9fa;
        opacity: 0.5;
    }
    
    .radio-container, .select-container {
        background: linear-gradient(145deg, #ffffff, #f8f9fa);
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        margin-bottom: 2rem;
        border: 1px solid rgba(102, 126, 234, 0.1);
    }
    
    .stats-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        margin-top: 2rem;
        text-align: center;
    }
    
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
        margin-top: 1rem;
    }
    
    .stat-item {
        background: rgba(255,255,255,0.1);
        padding: 1rem;
        border-radius: 10px;
        backdrop-filter: blur(10px);
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
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
    
    @media (max-width: 768px) {
        .calendar-grid {
            gap: 4px;
        }
        
        .calendar-day {
            padding: 0.5rem 0.25rem;
            min-height: 50px;
            font-size: 0.9rem;
        }
        
        .main-header h1 {
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
                
                class_str = " ".join(day_classes)
                html += f'<div class="{class_str}">{day}</div>'
    
    html += "</div></div>"
    return html

def create_year_calendar_html(year):
    """Создает HTML календарь для всего года"""
    html = ""
    for month in range(1, 13):
        html += create_month_calendar_html(year, month)
    return html

# Главный заголовок
st.markdown("""
<div class="main-header">
    <h1>📅 Календарь 2025</h1>
    <p>Красивый и функциональный календарь с праздниками и событиями</p>
</div>
""", unsafe_allow_html=True)

# Контейнер для выбора опции
with st.container():
    st.markdown('<div class="radio-container">', unsafe_allow_html=True)
    option = st.radio("Что показать?", ["Весь год", "Один месяц"])
    st.markdown('</div>', unsafe_allow_html=True)

year = 2025

if option == "Весь год":
    st.markdown(create_year_calendar_html(year), unsafe_allow_html=True)

elif option == "Один месяц":
    with st.container():
        st.markdown('<div class="select-container">', unsafe_allow_html=True)
        month = st.selectbox("Выберите месяц", 
                           list(range(1, 13)), 
                           format_func=lambda x: calendar.month_name[x])
        st.markdown('</div>', unsafe_allow_html=True)
    
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
    </div>
</div>
""", unsafe_allow_html=True)

# Легенда
st.markdown("---")
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown("🎯 **Сегодня** - выделен зеленым")
with col2:
    st.markdown("🎉 **Праздники** - выделены красным")
with col3:
    st.markdown("🌅 **Выходные** - выделены синим")
with col4:
    st.markdown("📅 **Обычные дни** - серый фон")

