class Priority:
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4


class Status:
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    CLOSED = "closed"


class Ticket:
    def __init__(self, ticket_id, title, status, priority):
        self.id = ticket_id
        self.title = title
        self.status = status
        self.priority = priority

    def __str__(self):
        return f"[{self.id}] (priority={self.priority}, {self.status}) {self.title}"


def create_ticket(data):
    data = data.strip()

    # Bug формат: BUG-101;Неверный расчёт налога;critical;open
    if data.startswith('BUG-'):
        parts = data.split(';')
        if len(parts) != 4:
            raise ValueError(f"Некорректный формат: {data}")

        priority_map = {
            'critical': Priority.CRITICAL,
            'high': Priority.HIGH,
            'medium': Priority.MEDIUM,
            'low': Priority.LOW
        }
        priority = priority_map.get(parts[2].lower(), Priority.MEDIUM)

        return Ticket(
            ticket_id=parts[0],
            title=parts[1],
            status=parts[3],
            priority=priority
        )

    # Feature формат: F-202;Добавить тёмную тему;5;in_progress
    elif data.startswith('F-'):
        parts = data.split(';')
        if len(parts) != 4:
            raise ValueError(f"Некорректный формат: {data}")

        try:
            story_points = int(parts[2])
            if story_points <= 3:
                priority = Priority.LOW
            elif story_points <= 5:
                priority = Priority.MEDIUM
            elif story_points <= 7:
                priority = Priority.HIGH
            else:
                priority = Priority.CRITICAL
        except:
            priority = Priority.MEDIUM

        return Ticket(
            ticket_id=parts[0],
            title=parts[1],
            status=parts[3],
            priority=priority
        )

    # Support формат: T-303|Проблемы со входом|high|closed
    elif data.startswith('T-'):
        parts = data.split('|')
        if len(parts) != 4:
            raise ValueError(f"Некорректный формат: {data}")

        priority_map = {
            'critical': Priority.CRITICAL,
            'high': Priority.HIGH,
            'medium': Priority.MEDIUM,
            'low': Priority.LOW
        }
        priority = priority_map.get(parts[2].lower(), Priority.MEDIUM)

        # Для длинных описаний обрезаем заголовок
        title = parts[1]
        if len(title) > 50:
            title = title[:50] + "..."

        return Ticket(
            ticket_id=parts[0],
            title=title,
            status=parts[3],
            priority=priority
        )

    else:
        raise ValueError(f"Неизвестный формат задачи: {data}")


def main():

    tickets = []

    # Простые данные (формат: тип-id;заголовок;приоритет/story_points;статус)
    tasks = [
        'BUG-101;Неверный расчёт налога;critical;open',
        'F-202;Добавить тёмную тему;5;in_progress',
        'T-303|Проблемы со входом|high|closed',
        'BUG-102;Ошибка авторизации;high;open',
        'F-203;Добавить поддержку OAuth;8;open'
    ]

    print("Загружаем задачи...")
    for task in tasks:
        try:
            ticket = create_ticket(task)
            tickets.append(ticket)
            print(f"Загружена: {ticket.id}")
        except ValueError as e:
            print(f"Ошибка: {e}")

    print("\n" + "=" * 60)
    print("Все задачи:")
    for ticket in tickets:
        print(ticket)

    print("\n" + "=" * 60)
    print("Задачи со статусом 'open':")
    open_tasks = [t for t in tickets if t.status == 'open']
    for task in open_tasks:
        print(task)

    print("\n" + "=" * 60)
    print("Задачи по приоритету:")
    sorted_tasks = sorted(tickets, key=lambda x: x.priority, reverse=True)
    for task in sorted_tasks:
        print(task)

    print("\n" + "=" * 60)
    print("Поиск задач с 'налог':")
    search_term = "налог"
    found = [t for t in tickets if search_term.lower() in t.title.lower()]
    for task in found:
        print(task)

    print("\n" + "=" * 60)
    print("Top 3 самые важные задачи:")
    top_3 = sorted_tasks[:3]
    for task in top_3:
        print(task)


if __name__ == "__main__":
    main()
