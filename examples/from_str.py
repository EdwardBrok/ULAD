#!/usr/bin/env python3
"""
Example: Parse ULAD config from string literal
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ulad_parser import UladParser
import json


def main():
    # Config as string (no file needed)
    config_str = '''
УЛАД-СХЕМА:3.0
ЗАМЕТКА: пример конфига прямо в коде :ЗАМЕТКА

[НАЧАЛО:СОЕДИНЕНИЕ]
    ХОЗЯИН ЭТО => «локальный-узел»
    ПРОХОД ЭТО => 437
    ИМЯ_ПОЛЬЗОВАТЕЛЯ ЭТО => «администратор»
    ПАРОЛЬ ЭТО => «секретненько»
    БЕЗОПАСНОСТЬ ЭТО => ИСТИНА
[КОНЕЦ:СОЕДИНЕНИЕ]

[НАЧАЛО:СЛУЖБА]
    ОТЛАДКА ЭТО => ЛОЖЬ
    ОТКУДА_МОЖНО ЭТО => (И) «местный-узел» ПОТОМ «соседний-узел» ПОТОМ «удалённый-узел» (И)
    ТАЙМАУТ ЭТО => тридцать
    ПОВТОРЫ ЭТО => пять
[КОНЕЦ:СЛУЖБА]

[НАЧАЛО:ХРАНИЛИЩЕ]
    ТИП ЭТО => «внутреннее»
    ПУТЬ ЭТО => «/данные/приложение/хранилище»
    РАЗМЕР ЭТО => сто двадцать четыре
    ЕДИНИЦА_РАЗМЕРА ЭТО => «мегабайты»
[КОНЕЦ:ХРАНИЛИЩЕ]
'''

    parser = UladParser()

    try:
        config = parser.parse(config_str)

        print("=== ULAD CONFIGURATION FROM STRING ===\n")
        print(json.dumps(config, indent=2, ensure_ascii=False))

        # Demonstrate type conversion
        print("\n=== TYPE DEMONSTRATION ===")
        timeout = config['СЛУЖБА']['ТАЙМАУТ']
        print(f"Timeout value: {timeout} (type: {type(timeout).__name__})")

        origins = config['СЛУЖБА']['ОТКУДА_МОЖНО']
        print(f"Allowed origins: {origins} (type: {type(origins).__name__})")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == '__main__':
    main()