import matplotlib.pyplot as plt
import numpy as np

def calculate_hardware_requirements(n_users, r_day=2, t_active=8, k_peak=0.25, t_inf=100, u_gpu=0.7, k_reserve=1.5):
    """
    Расчет необходимого количества GPU на основе входящих параметров системы.
    """
    # Расчет пикового RPS (запросов/файлов в секунду)
    rps = (n_users * r_day) / (t_active * 3600 * k_peak)
    # Вычисление количества логических процессов с округлением вверх
    raw_gpu_processes = rps * t_inf / u_gpu
    # Применение коэффициента резервирования
    n_gpu = np.ceil(raw_gpu_processes) * k_reserve
    return n_gpu

# Генерация массива данных от 100 до 10000 пользователей
users_range = np.linspace(100, 10000, 100)
gpus_needed = [calculate_hardware_requirements(u) for u in users_range]

# Построение графика
plt.figure(figsize=(12, 7))
plt.plot(users_range, gpus_needed, color='#8E44AD', linewidth=3, label='Требуемое количество GPU')
plt.fill_between(users_range, gpus_needed, color='#D7BDE2', alpha=0.3)

plt.title('Моделирование зависимости GPU-ресурсов от масштаба системы (67)', fontsize=16, pad=15)
plt.xlabel('Количество активных инспекторов в системе', fontsize=12)
plt.ylabel('Необходимое количество GPU-инстансов (с учетом резерва)', fontsize=12)
plt.grid(True, linestyle='-.', alpha=0.6)

# Аннотация целевых масштабов
scales = [(100, 'Малый\n(Регион)'), (1000, 'Средний\n(Округ)'), (10000, 'Большой\n(Федерация)')]
for users, label in scales:
    gpus = calculate_hardware_requirements(users)
    plt.scatter(users, gpus, color='#C0392B', s=80, zorder=5)
    plt.annotate(f'{label}\n{users} чел.\n~{int(gpus)} GPU', 
                 (users, gpus), textcoords="offset points", xytext=(-35,15), ha='center', 
                 fontsize=10, bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="gray", lw=1))

plt.legend(loc='upper left', fontsize=12)
plt.tight_layout()
plt.show()
