from aiogram.utils import executor
from loader import dp
import middlwares, filters, handlers

if __name__ == '__main__':

    executor.start_polling(dp)
