import matplotlib.pyplot as plt
import numpy as np

# Задание временного горизонта: 36 месяцев (3 года)
months = np.arange(1, 37)

# Финансовые показатели Варианта А (On-Premise)
capex_onprem = 23.86  # Капитальные затраты (млн руб.)
opex_onprem_monthly = 5.0 / 12  # Ежемесячные операционные затраты (млн руб/мес)
tco_onprem = capex_onprem + (opex_onprem_monthly * months)

# Финансовые показатели Варианта В (Cloud Selectel)
opex_cloud_monthly = 45.88 / 12  # Ежемесячные арендные платежи (млн руб/мес)
tco_cloud = opex_cloud_monthly * months

# Визуализация данных
plt.figure(figsize=(10, 6))
plt.plot(months, tco_onprem, label='Вариант А: Собственная инфраструктура (CAPEX + OPEX)', color='#27AE60', linewidth=3)
plt.plot(months, tco_cloud, label='Вариант В: Облачные мощности (OPEX)', color='#E67E22', linewidth=3)

# Алгоритм поиска точки безубыточности (Cross-over point)
crossover_idx = np.argmin(np.abs(tco_onprem - tco_cloud))
crossover_month = months[crossover_idx]
crossover_cost = tco_onprem[crossover_idx]

plt.scatter(crossover_month, crossover_cost, color='#C0392B', s=120, zorder=5)
plt.annotate(f'Точка окупаемости\n(Месяц {crossover_month})', 
             (crossover_month, crossover_cost), textcoords="offset points", xytext=(-40, 20), ha='center',
             fontsize=11, fontweight='bold')

plt.title('Анализ экономической эффективности: TCO на горизонте 3 лет', fontsize=15, pad=15)
plt.xlabel('Время эксплуатации (Месяцы)', fontsize=12)
plt.ylabel('Накопленные затраты (Млн. руб.)', fontsize=12)
plt.legend(loc='upper left', fontsize=11)
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.show()
