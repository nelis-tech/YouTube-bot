from youtube_api import YouTubeAPI
from aiogram import types

class BotManager:
    def __init__(self):
        self.bot = None
        self.api = YouTubeAPI()
        self.keywords = []
        self.filters = {}
        self.scraping_interval = 60
        self.setup_step = None

    async def start(self, message: types.Message):
        await message.answer('Bot started. Use /setup to configure the bot.')

    async def setup(self, message: types.Message):
        self.setup_step = 'keywords'
        await message.answer('Welcome to the YouTube Bot setup! Start by specifying your search keywords, separated by commas.')

    async def help(self, message: types.Message):
        await message.answer('Use /start to start the bot, /setup to configure the bot.')

    async def handle_message(self, message: types.Message):
        chat_id = message.chat.id
        message_text = message.text
        if self.setup_step == 'keywords':
            self.keywords = message.split(',')
            self.setup_step = 'videoDefinition'
            await self.bot.send_message(chat_id=chat_id, text='Keywords set to: ' + ', '.join(self.keywords) + '. Now, please specify the video definition: HD or SD?')
        elif self.setup_step == 'videoDefinition':
            self.filters['videoDefinition'] = message
            self.setup_step = 'videoDimension'
            await self.bot.send_message(chat_id=chat_id, text='Video definition set to: ' + self.filters['videoDefinition'] + '. Now, please specify the video dimension: 2D or 3D?')
        elif self.setup_step == 'videoDimension':
            self.filters['videoDimension'] = message
            self.setup_step = 'videoDuration'
            await self.bot.send_message(chat_id=chat_id, text='Video dimension set to: ' + self.filters['videoDimension'] + '. Now, please specify the video duration: short, medium, or long?')
        elif self.setup_step == 'videoDuration':
            self.filters['videoDuration'] = message
            self.setup_step = 'videoEmbeddable'
            await self.bot.send_message(chat_id=chat_id, text='Video duration set to: ' + self.filters['videoDuration'] + '. Now, please specify if the video should be embeddable: yes or no?')
        elif self.setup_step == 'videoEmbeddable':
            self.filters['videoEmbeddable'] = message.lower() == 'yes'
            self.setup_step = 'videoLicense'
            await self.bot.send_message(chat_id=chat_id, text='Video embeddability set to: ' + str(self.filters['videoEmbeddable']) + '. Now, please specify the video license type: Creative Commons or Standard YouTube?')
        elif self.setup_step == 'videoLicense':
            self.filters['videoLicense'] = message
            self.setup_step = 'videoType'
            await self.bot.send_message(chat_id=chat_id, text='Video license type set to: ' + self.filters['videoLicense'] + '. Now, please specify the video type: episode, movie, or any?')
        elif self.setup_step == 'videoType':
            self.filters['videoType'] = message
            self.setup_step = 'location'
            await self.bot.send_message(chat_id=chat_id, text='Video type set to: ' + self.filters['videoType'] + '. Now, please specify the location for search (if any):')
        elif self.setup_step == 'location':
            self.filters['location'] = message
            self.setup_step = 'maxResults'
            await self.bot.send_message(chat_id=chat_id, text='Location set to: ' + self.filters['location'] + '. Now, please specify the maximum number of results to return:')
        elif self.setup_step == 'maxResults':
            self.filters['maxResults'] = int(message)
            self.setup_step = 'order'
            await self.bot.send_message(chat_id=chat_id, text='Max results set to: ' + str(self.filters['maxResults']) + '. Now, please specify the order of results: date, rating, relevance, title, video count, or view count?')
        elif self.setup_step == 'order':
            self.filters['order'] = message
            self.setup_step = 'publishedAfter'
            await self.bot.send_message(chat_id=chat_id, text='Order set to: ' + self.filters['order'] + '. Now, please specify the publication time to search videos before (provide date in YYYY-MM-DD format):')
        elif self.setup_step == 'publishedAfter':
            self.filters['publishedAfter'] = message
            self.setup_step = 'interval'
            await self.bot.send_message(chat_id=chat_id, text='Publication time set to: ' + self.filters['publishedAfter'] + '. Now, please specify the scraping interval in minutes (e.g., 60 for an hour):')
        elif self.setup_step == 'interval':
            self.scraping_interval = int(message)
            self.setup_step = None
            await self.bot.send_message(chat_id=chat_id, text='Scraping interval set to: ' + str(self.scraping_interval) + ' minutes. Setup complete! Your bot is now configured per your preferences. Use /start to begin the search or /help for more commands.')
