import streamlit as st
import calendar
from datetime import datetime

# Настройка страницы
st.set_page_config(
    page_title="Календарь 2025",
    page_icon="📅",
    layout="wide"
)

# CSS стили для красивого дизайна
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
    }
    
    .calendar-container {
        background: white;
        border-radius: 15px;
        padding: 2rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
    
    .month-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    
    .calendar-grid {
        display: grid;
        grid-template-columns: repeat(7, 1fr);
        gap: 5px;
        margin-top: 1rem;
    }
    
    .calendar-day {
        background: #f8f9fa;
        padding: 0.5rem;
        text-align: center;
        border-radius: 8px;
        border: 1px solid #e9ecef;
        transition: all 0.3s ease;
    }
    
    .calendar-day:hover {
        background: #667eea;
        color: white;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
    }
    
    .weekday-header {
        background: #495057;
        color: white;
        padding: 0.5rem;
        text-align: center;
        border-radius: 8px;
        font-weight: bold;
    }
    
    .today {
        background: #28a745 !important;
        color: white !important;
        font-weight: bold;
    }
    
    .other-month {
        color: #adb5bd;
        background: #f1f3f4;
    }
    
    .radio-container {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin-bottom: 2rem;
    }
    
    .select-container {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

def display_month_calendar(year, month):
    """Отображает календарь месяца используя Streamlit компоненты"""
    month_name = calendar.month_name[month]
    
    # Заголовок месяца
    st.markdown(f"""
    <div class="month-header">
        <h2>{month_name} {year}</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Получаем календарь
    cal = calendar.monthcalendar(year, month)
    today = datetime.now()
    
    # Создаем таблицу календаря
    weekdays = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']
    
    # Создаем данные для таблицы
    table_data = []
    for week in cal:
        row = []
        for day in week:
            if day == 0:
                row.append("")
            else:
                # Проверяем, является ли это сегодняшним днем
                if year == today.year and month == today.month and day == today.day:
                    row.append(f"**{day}** 🎯")
                else:
                    row.append(str(day))
        table_data.append(row)
    
    # Отображаем таблицу
    st.table(table_data)

def display_year_calendar(year):
    """Отображает календарь всего года"""
    months = list(range(1, 13))
    
    # Создаем 3 колонки для месяцев
    for i in range(0, len(months), 3):
        cols = st.columns(3)
        for j, col in enumerate(cols):
            if i + j < len(months):
                month = months[i + j]
                with col:
                    st.markdown(f"### {calendar.month_name[month]}")
                    st.text(calendar.month(year, month))

# Главный заголовок
st.markdown("""
<div class="main-header">
    <h1>📅 Календарь 2025</h1>
    <p>Выберите, что хотите посмотреть</p>
</div>
""", unsafe_allow_html=True)

# Простой заголовок на случай, если HTML не работает
st.title("📅 Календарь 2025")

# Выбор опции
option = st.radio("Что показать?", ["Весь год", "Один месяц"])

year = 2025

if option == "Весь год":
    st.subheader("Календарь на весь 2025 год")
    display_year_calendar(year)

elif option == "Один месяц":
    month = st.selectbox("Выберите месяц", 
                        list(range(1, 13)), 
                        format_func=lambda x: calendar.month_name[x])
    
    display_month_calendar(year, month)

# Дополнительная информация
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    st.info("📅 Всего дней в году: 365")
with col2:
    st.info("🎯 Текущий год: 2025")
with col3:
    st.info("⭐ Особый год!")

# Простой тест
st.success("✅ Приложение работает!")
st.write("Если вы видите это сообщение, значит приложение загрузилось успешно.")

