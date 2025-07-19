import streamlit as st
import calendar

def print_year_calendar(year):
    result = ""
    for month in range(1, 13):
        result += calendar.month(year, month) + "\n"
        result += "-" * 20 + "\n"
    return result

def print_month_calendar(year, month):
    return calendar.month(year, month)

# --- UI ---
st.title("📅 Календарь на 2025 год")

option = st.radio("Что показать?", ["Весь год", "Один месяц"])

year = 2025

if option == "Весь год":
    st.text(print_year_calendar(year))

elif option == "Один месяц":
    month = st.selectbox("Выберите месяц", list(range(1, 13)))
    st.text(print_month_calendar(year, month))
