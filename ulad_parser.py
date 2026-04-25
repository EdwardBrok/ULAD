"""
ULAD Parser (Unified Logical Aggregation of Data)
Full Russian format configuration parser
"""

import re
from typing import Any, Dict, List, Union


class UladParser:
    """Parser for .улад configuration files"""

    def __init__(self):
        self.data = {}
        self.current_section = None

        # Russian number words
        self.number_words = {
            'ноль': 0, 'один': 1, 'два': 2, 'три': 3, 'четыре': 4,
            'пять': 5, 'шесть': 6, 'семь': 7, 'восемь': 8, 'девять': 9,
            'десять': 10, 'одиннадцать': 11, 'двенадцать': 12, 'тринадцать': 13,
            'четырнадцать': 14, 'пятнадцать': 15, 'шестнадцать': 16,
            'семнадцать': 17, 'восемнадцать': 18, 'девятнадцать': 19,
            'двадцать': 20, 'тридцать': 30, 'сорок': 40, 'пятьдесят': 50,
            'шестьдесят': 60, 'семьдесят': 70, 'восемьдесят': 80, 'девяносто': 90,
            'сто': 100, 'двести': 200, 'триста': 300, 'четыреста': 400,
            'пятьсот': 500, 'шестьсот': 600, 'семьсот': 700, 'восемьсот': 800,
            'девятьсот': 900, 'тысяча': 1000
        }

    def parse(self, content: str) -> Dict[str, Any]:
        """Parse ULAD format string into dictionary"""
        lines = content.split('\n')

        # Validate header
        if not lines or not lines[0].strip().startswith('УЛАД-СХЕМА:3.0'):
            raise UladError('File must start with "УЛАД-СХЕМА:3.0"')

        for line in lines[1:]:
            stripped = line.strip()

            if not stripped:
                continue

            # Skip comments
            if stripped.startswith('ЗАМЕТКА:') and stripped.endswith(':ЗАМЕТКА'):
                continue

            # Section start
            if stripped.startswith('[НАЧАЛО:'):
                self._start_section(stripped)
                continue

            # Section end
            if stripped.startswith('[КОНЕЦ:'):
                self._end_section(stripped)
                continue

            # Key-value pair
            if 'ЭТО =>' in stripped:
                self._parse_pair(stripped)

        return self.data

    def load_file(self, filepath: str) -> Dict[str, Any]:
        """Load and parse .улад file from disk"""
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        return self.parse(content)

    def _start_section(self, line: str):
        """Handle section start: [НАЧАЛО:ИМЯ]"""
        name = line[8:-1]
        self.current_section = name
        if name not in self.data:
            self.data[name] = {}

    def _end_section(self, line: str):
        """Handle section end: [КОНЕЦ:ИМЯ]"""
        name = line[7:-1]
        if self.current_section == name:
            self.current_section = None
        else:
            raise UladError(f'Section mismatch: started {self.current_section}, ended {name}')

    def _parse_pair(self, line: str):
        """Parse key-value pair: КЛЮЧ ЭТО => значение"""
        parts = line.split('ЭТО =>', 1)
        key = parts[0].strip()
        raw_value = parts[1].strip()

        parsed_value = self._parse_value(raw_value)

        if self.current_section:
            self.data[self.current_section][key] = parsed_value
        else:
            self.data[key] = parsed_value

    def _parse_value(self, value: str) -> Any:
        """Parse value with type inference"""

        # Quoted string with Russian quotes
        if value.startswith('«') and value.endswith('»'):
            return value[1:-1]

        # Boolean values
        if value == 'ИСТИНА':
            return True
        if value == 'ЛОЖЬ':
            return False

        # Array with (И) ... (И) and ПОТОМ separator
        if value.startswith('(И)') and value.endswith('(И)'):
            inner = value[3:-3]
            if not inner.strip():
                return []
            items = [item.strip() for item in inner.split('ПОТОМ')]
            return [self._parse_value(item) for item in items]

        # Dictionary {А В НЁМ ... }
        if value.startswith('{А В НЁМ'):
            return self._parse_dict(value)

        # Number (digits or words)
        num = self._to_number(value)
        if num is not None:
            return num

        # Fallback to string
        return value

    def _parse_dict(self, value: str) -> Dict[str, Any]:
        """Parse nested dictionary"""
        result = {}
        inner = value[9:-1].strip()

        if '\n' not in inner:
            pairs = self._split_dict_pairs(inner)
            for pair in pairs:
                if 'ЭТО =>' in pair:
                    k, v = pair.split('ЭТО =>', 1)
                    result[k.strip()] = self._parse_value(v.strip())
        else:
            lines = inner.split('\n')
            for line in lines:
                stripped = line.strip()
                if 'ЭТО =>' in stripped:
                    k, v = stripped.split('ЭТО =>', 1)
                    result[k.strip()] = self._parse_value(v.strip())

        return result

    def _split_dict_pairs(self, text: str) -> List[str]:
        """Split dictionary pairs"""
        pairs = []
        current = []
        depth = 0

        for char in text:
            if char in '{(':
                depth += 1
            elif char in ')}':
                depth -= 1
            elif char == ',' and depth == 0:
                pairs.append(''.join(current))
                current = []
                continue
            current.append(char)

        if current:
            pairs.append(''.join(current))

        return [p for p in pairs if p.strip()]

    def _to_number(self, text: str) -> Union[int, float, None]:
        """Convert Russian number words or digits to number"""
        # Try digits first
        if any(d in text for d in '0123456789'):
            try:
                return int(text)
            except ValueError:
                try:
                    return float(text)
                except ValueError:
                    pass

        # Try simple word lookup
        lower_text = text.lower()
        if lower_text in self.number_words:
            return self.number_words[lower_text]

        # Try compound numbers
        words = lower_text.split()
        if len(words) > 1:
            total = 0
            for word in words:
                if word in self.number_words:
                    total += self.number_words[word]
            if total > 0:
                return total

        return None


class UladError(Exception):
    """Exception for ULAD parsing errors"""
    pass