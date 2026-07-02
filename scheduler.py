from apscheduler.schedulers.blocking import BlockingScheduler
from main import main as run_monitor


def job():
    print("\n⏰ Авто-запуск мониторинга...")
    run_monitor()


def start_scheduler():
    scheduler = BlockingScheduler()

    # каждые 40 минут
    scheduler.add_job(job, "interval", minutes=40)

    print("🚀 Мониторинг запущен (каждые 40 минут)")

    scheduler.start()