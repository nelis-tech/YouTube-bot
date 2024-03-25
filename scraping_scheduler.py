import schedule
import time

class ScrapingScheduler:
    def __init__(self, manager):
        self.manager = manager
        self.interval = manager.scraping_interval
        self.is_running = False

    def start(self):
        schedule.every(self.interval).minutes.do(self.manager.search_videos, self.manager.bot.chat_id)
        self.is_running = True
        while self.is_running:
            schedule.run_pending()
            time.sleep(1)

    def stop(self):
        schedule.clear()
        self.is_running = False

    def set_interval(self, interval):
        self.interval = interval