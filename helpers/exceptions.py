
class HandledException(Exception):
    """Обработанное исключение, текст которого выведется в ответе сервера"""
    text = 'Неизвестная ошибка'

    def __str__(self):
        return self.text
