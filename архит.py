from graphviz import Digraph

def generate_enterprise_architecture_diagram():
    # Инициализация графа с настройками высокого разрешения
    dot = Digraph(comment='Архитектура сервиса транскрибации', format='png')
    dot.attr(rankdir='LR', size='14,10', dpi='300', fontname='Helvetica')
    dot.attr('node', shape='box', style='rounded,filled', fontname='Helvetica', fontsize='12')
    dot.attr('edge', fontname='Helvetica', fontsize='10', color='#555555')

    # Группа: Клиентский уровень
    with dot.subgraph(name='cluster_client') as c:
        c.attr(label='Пользовательский слой', style='dashed', color='#BDC3C7')
        c.node('App', 'Мобильное АРМ инспектора\n(Запись и загрузка аудио)', fillcolor='#D1E8E2')
        c.node('Web', 'Веб-портал\n(Аналитика протоколов)', fillcolor='#D1E8E2')

    # Группа: Уровень маршрутизации и бизнес-логики (CPU Pool)
    with dot.subgraph(name='cluster_api') as c:
        c.attr(label='Слой маршрутизации (CPU Kubernetes Pool)', style='solid', color='#7F8C8D')
        c.node('Ingress', 'API Gateway / WAF\n(NGINX)', fillcolor='#F9E79F')
        c.node('API', 'Backend Service\n(FastAPI / Uvicorn)', fillcolor='#FAD7A1')

    # Группа: Уровень хранения данных (Stateful Pool)
    with dot.subgraph(name='cluster_storage') as c:
        c.attr(label='Слой персистентного хранения', style='solid', color='#2980B9')
        c.node('S3', 'Объектное хранилище S3\n(MinIO) - Аудиоархив', fillcolor='#AED6F1')
        c.node('DB', 'Реляционная СУБД\n(PostgreSQL) - Метаданные', fillcolor='#AED6F1')
        c.node('MQ', 'Брокер сообщений\n(RabbitMQ) - Очереди', fillcolor='#F5B041')

    # Группа: Уровень ИИ вычислений (GPU Pool)
    with dot.subgraph(name='cluster_gpu') as c:
        c.attr(label='Слой инференса нейросетей (GPU Kubernetes Pool)', style='solid', color='#8E44AD')
        c.node('Worker1', 'Inference Worker 1\n(faster-whisper INT8)', fillcolor='#D7BDE2')
        c.node('Worker2', 'Inference Worker N\n(faster-whisper INT8)', fillcolor='#D7BDE2')

    # Группа: Уровень мониторинга
    with dot.subgraph(name='cluster_mon') as c:
        c.attr(label='Слой обсервабилити', style='dotted', color='#7F8C8D')
        c.node('Prometheus', 'Prometheus + NVIDIA DCGM\nСбор телеметрии', fillcolor='#A9DFBF')
        c.node('Grafana', 'Grafana\nДашборды', fillcolor='#A9DFBF')

    # Построение связей (маршруты данных)
    dot.edge('App', 'Ingress', label=' HTTP/TLS (Аудио)')
    dot.edge('Web', 'Ingress', label=' HTTP/TLS (Запросы)')
    dot.edge('Ingress', 'API', label=' Маршрутизация')
    
    # Логика сохранения задачи
    dot.edge('API', 'S3', label=' 1. Сохранение файла (Stream)')
    dot.edge('API', 'DB', label=' 2. Создание записи')
    dot.edge('API', 'MQ', label=' 3. Публикация Task ID')
    
    # Логика обработки задачи
    dot.edge('MQ', 'Worker1', label=' 4. Асинхронное чтение')
    dot.edge('MQ', 'Worker2', label=' 4. Асинхронное чтение')
    
    dot.edge('Worker1', 'S3', label=' 5. Загрузка аудио в RAM')
    dot.edge('Worker2', 'S3', label=' 5. Загрузка аудио в RAM')
    
    dot.edge('Worker1', 'API', label=' 6. Возврат JSON протокола')
    dot.edge('Worker2', 'API', label=' 6. Возврат JSON протокола')
    
    # Мониторинг
    dot.edge('Prometheus', 'Worker1', style='dashed', dir='back')
    dot.edge('Prometheus', 'API', style='dashed', dir='back')
    dot.edge('Grafana', 'Prometheus', label=' PromQL')

    # Генерация файла
    dot.render('enterprise_architecture_diagram', view=True)
    print("Генерация завершена. Файл 'enterprise_architecture_diagram.png' сохранен.")

if __name__ == '__main__':
    generate_enterprise_architecture_diagram()