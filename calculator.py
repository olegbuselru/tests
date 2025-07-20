import streamlit as st
from datetime import datetime
import json

# Настройка страницы
st.set_page_config(
    page_title="📝 Список задач",
    page_icon="✅",
    layout="wide"
)

# Инициализация состояния
if 'tasks' not in st.session_state:
    st.session_state.tasks = []
if 'completed_tasks' not in st.session_state:
    st.session_state.completed_tasks = []

# CSS стили для красивого дизайна
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
    }
    
    .main-header h1 {
        margin: 0;
        font-size: 2.5rem;
        font-weight: 700;
    }
    
    .main-header p {
        margin: 1rem 0 0 0;
        opacity: 0.9;
        font-size: 1.1rem;
    }
    
    .task-input-container {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        margin-bottom: 2rem;
        border: 2px solid #f0f0f0;
    }
    
    .task-item {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        box-shadow: 0 3px 10px rgba(0,0,0,0.1);
        border-left: 4px solid #667eea;
        transition: all 0.3s ease;
    }
    
    .task-item:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 20px rgba(0,0,0,0.15);
    }
    
    .task-item.completed {
        border-left-color: #28a745;
        opacity: 0.7;
        background: #f8f9fa;
    }
    
    .task-item.completed .task-text {
        text-decoration: line-through;
        color: #6c757d;
    }
    
    .task-text {
        font-size: 1.1rem;
        font-weight: 500;
        margin: 0;
        color: #2c3e50;
    }
    
    .task-meta {
        font-size: 0.9rem;
        color: #6c757d;
        margin-top: 0.5rem;
    }
    
    .stats-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        text-align: center;
    }
    
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1.5rem;
        margin-top: 1.5rem;
    }
    
    .stat-item {
        background: rgba(255,255,255,0.2);
        padding: 1.5rem;
        border-radius: 10px;
        backdrop-filter: blur(10px);
    }
    
    .stat-item h3 {
        margin: 0 0 0.5rem 0;
        font-size: 1.2rem;
    }
    
    .stat-item p {
        margin: 0;
        font-size: 2rem;
        font-weight: 700;
    }
    
    .priority-high {
        border-left-color: #dc3545 !important;
    }
    
    .priority-medium {
        border-left-color: #ffc107 !important;
    }
    
    .priority-low {
        border-left-color: #28a745 !important;
    }
    
    .delete-btn {
        background: #dc3545;
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        cursor: pointer;
        font-size: 0.9rem;
        transition: all 0.3s ease;
    }
    
    .delete-btn:hover {
        background: #c82333;
        transform: scale(1.05);
    }
    
    .add-btn {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 25px;
        cursor: pointer;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.3);
    }
    
    .add-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
    }
    
    .clear-btn {
        background: #6c757d;
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        cursor: pointer;
        font-size: 0.9rem;
        transition: all 0.3s ease;
    }
    
    .clear-btn:hover {
        background: #5a6268;
    }
    
    .section-header {
        background: #f8f9fa;
        padding: 1rem 1.5rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        border-left: 4px solid #667eea;
    }
    
    .section-header h2 {
        margin: 0;
        color: #2c3e50;
        font-size: 1.3rem;
    }
    
    @media (max-width: 768px) {
        .main-header h1 {
            font-size: 2rem;
        }
        
        .stats-grid {
            grid-template-columns: 1fr;
        }
    }
</style>
""", unsafe_allow_html=True)

def add_task(task_text, priority="medium"):
    """Добавляет новую задачу"""
    if task_text.strip():
        task = {
            'id': len(st.session_state.tasks) + len(st.session_state.completed_tasks) + 1,
            'text': task_text.strip(),
            'priority': priority,
            'created_at': datetime.now().strftime("%d.%m.%Y %H:%M"),
            'completed_at': None
        }
        st.session_state.tasks.append(task)
        return True
    return False

def complete_task(task_id):
    """Отмечает задачу как выполненную"""
    for task in st.session_state.tasks:
        if task['id'] == task_id:
            task['completed_at'] = datetime.now().strftime("%d.%m.%Y %H:%M")
            st.session_state.completed_tasks.append(task)
            st.session_state.tasks.remove(task)
            break

def delete_task(task_id, from_completed=False):
    """Удаляет задачу"""
    if from_completed:
        st.session_state.completed_tasks = [t for t in st.session_state.completed_tasks if t['id'] != task_id]
    else:
        st.session_state.tasks = [t for t in st.session_state.tasks if t['id'] != task_id]

def clear_completed_tasks():
    """Очищает все выполненные задачи"""
    st.session_state.completed_tasks = []

# Главный заголовок
st.markdown("""
<div class="main-header">
    <h1>📝 Список задач</h1>
    <p>Организуйте свои дела и отслеживайте прогресс</p>
</div>
""", unsafe_allow_html=True)

# Статистика
total_tasks = len(st.session_state.tasks) + len(st.session_state.completed_tasks)
completed_count = len(st.session_state.completed_tasks)
pending_count = len(st.session_state.tasks)
completion_rate = (completed_count / total_tasks * 100) if total_tasks > 0 else 0

st.markdown("""
<div class="stats-container">
    <h2>📊 Статистика</h2>
    <div class="stats-grid">
        <div class="stat-item">
            <h3>Всего задач</h3>
            <p>{}</p>
        </div>
        <div class="stat-item">
            <h3>Выполнено</h3>
            <p>{}</p>
        </div>
        <div class="stat-item">
            <h3>В процессе</h3>
            <p>{}</p>
        </div>
        <div class="stat-item">
            <h3>Прогресс</h3>
            <p>{:.1f}%</p>
        </div>
    </div>
</div>
""".format(total_tasks, completed_count, pending_count, completion_rate), unsafe_allow_html=True)

# Добавление новой задачи
st.markdown('<div class="task-input-container">', unsafe_allow_html=True)
st.markdown("### ➕ Добавить новую задачу")

col1, col2, col3 = st.columns([3, 1, 1])

with col1:
    new_task = st.text_input("Введите задачу:", placeholder="Например: Сделать покупки", key="new_task_input")

with col2:
    priority = st.selectbox("Приоритет:", ["Низкий", "Средний", "Высокий"], key="priority_select")

with col3:
    if st.button("➕ Добавить", key="add_task_btn", use_container_width=True):
        priority_map = {"Низкий": "low", "Средний": "medium", "Высокий": "high"}
        if add_task(new_task, priority_map[priority]):
            st.success("✅ Задача добавлена!")
            st.rerun()

st.markdown('</div>', unsafe_allow_html=True)

# Текущие задачи
if st.session_state.tasks:
    st.markdown('<div class="section-header">', unsafe_allow_html=True)
    st.markdown("### 🔄 Текущие задачи")
    st.markdown('</div>', unsafe_allow_html=True)
    
    for task in st.session_state.tasks:
        col1, col2, col3 = st.columns([4, 1, 1])
        
        with col1:
            priority_class = f"priority-{task['priority']}"
            st.markdown(f"""
            <div class="task-item {priority_class}">
                <p class="task-text">{task['text']}</p>
                <p class="task-meta">📅 Создано: {task['created_at']} | 🎯 Приоритет: {task['priority'].title()}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            if st.button("✅", key=f"complete_{task['id']}", help="Отметить как выполненную"):
                complete_task(task['id'])
                st.success("🎉 Задача выполнена!")
                st.rerun()
        
        with col3:
            if st.button("🗑️", key=f"delete_{task['id']}", help="Удалить задачу"):
                delete_task(task['id'])
                st.success("🗑️ Задача удалена!")
                st.rerun()
else:
    st.info("📝 У вас пока нет активных задач. Добавьте первую задачу выше!")

# Выполненные задачи
if st.session_state.completed_tasks:
    st.markdown('<div class="section-header">', unsafe_allow_html=True)
    st.markdown("### ✅ Выполненные задачи")
    st.markdown('</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([5, 1])
    
    with col1:
        for task in st.session_state.completed_tasks:
            st.markdown(f"""
            <div class="task-item completed">
                <p class="task-text">{task['text']}</p>
                <p class="task-meta">📅 Создано: {task['created_at']} | ✅ Выполнено: {task['completed_at']}</p>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        if st.button("🗑️ Очистить все", key="clear_completed", help="Удалить все выполненные задачи"):
            clear_completed_tasks()
            st.success("🗑️ Все выполненные задачи удалены!")
            st.rerun()

# Дополнительные функции
st.markdown("---")
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🔄 Обновить", key="refresh_btn"):
        st.rerun()

with col2:
    if st.button("📊 Экспорт", key="export_btn"):
        tasks_data = {
            'active_tasks': st.session_state.tasks,
            'completed_tasks': st.session_state.completed_tasks,
            'export_date': datetime.now().strftime("%d.%m.%Y %H:%M")
        }
        st.download_button(
            label="📥 Скачать JSON",
            data=json.dumps(tasks_data, ensure_ascii=False, indent=2),
            file_name=f"tasks_{datetime.now().strftime('%Y%m%d_%H%M')}.json",
            mime="application/json"
        )

with col3:
    if st.button("🗑️ Очистить все", key="clear_all_btn"):
        st.session_state.tasks = []
        st.session_state.completed_tasks = []
        st.success("🗑️ Все задачи удалены!")
        st.rerun()

# Подсказки
st.markdown("---")
st.markdown("### 💡 Подсказки:")
st.markdown("""
- **Приоритеты**: Высокий (красный), Средний (желтый), Низкий (зеленый)
- **Статистика**: Отслеживайте свой прогресс в реальном времени
- **Экспорт**: Сохраните свои задачи в JSON файл
- **Очистка**: Удалите выполненные задачи одним кликом
""")
