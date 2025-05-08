# НОМЕРА РЕГИСТРОВ

CURRENT_FRAME_REG = 1               # РЕГИСТР ТЕКУЩЕГО ЭКРАНА

START_AUTOMAT_N3_MANUAL_REG = 2     # КНОПКА СТАРТА НАСОСА Н3 РУЧНОГО РЕЖИМА
START_MODE_MANUAL_REG = 3           # КНОПКА СТАРТА РУЧНОГО РЕЖИМА
START_AUTOMAT_N3_STAT_REG = 4       # КНОПКА СТАРТА НАСОСА Н3 СТАТИЧЕСКОГО РЕЖИМА
START_MODE_STAT_REG = 5             # КНОПКА СТАРТА СТАТИЧЕСКОГО РЕЖИМА
START_AUTOMAT_N3_CYCLE_REG = 6      # КНОПКА СТАРТА НАСОСА Н3 ЦИКЛИЧЕСКОГО РЕЖИМА
START_MODE_CYCLE_REG = 7            # КНОПКА СТАРТА ЦИКЛИЧЕСКОГО РЕЖИМА

PRESSURE_MN1 = 8                    # ДАВЛЕНИЕ МОНОМЕТРА 1 (FLOAT)
PRESSURE_MN2 = 10                   # ДАВЛЕНИЕ МОНОМЕТРА 2 (FLOAT)
SPEED = 12                          # СКОРОСТЬ НАБОРА ДАВЛЕНИЯ (FLOAT)

FREQ_MANUAL = 14                    # ЧАСТОТА ДЛЯ РУЧНОГО РЕЖИМА

PRESSURE_END_STAT = 15              # ДАВЛЕНИЕ КОНЕЧНОЕ ДЛЯ НАСТРОЕК СТАТИЧЕСКОГО РЕЖИМА (FLOAT)
PRESSURE_MID_STAT = 17              # ДАВЛЕНИЕ ПРОМЕЖУТОЧНОЕ ДЛЯ НАСТРОЕК СТАТИЧЕСКОГО РЕЖИМА (FLOAT)
PRESSURE_SPEED_STAT = 19            # СКОРОСТЬ НАБОРА ДАВЛЕНИЯ ДЛЯ НАСТРОЕК СТАТИЧЕСКОГО РЕЖИМА (FLOAT)
TIME_WAIT_1_STAT = 21               # ВРЕМЯ ОЖИДАНИЯ 1 ДЛЯ НАСТРОЕК СТАТИЧЕСКОГО РЕЖИМА
TIME_WAIT_2_STAT = 22               # ВРЕМЯ ОЖИДАНИЯ 2 ДЛЯ НАСТРОЕК СТАТИЧЕСКОГО РЕЖИМА

PRESSURE_END_CYCLE = 23             # ДАВЛЕНИЕ КОНЕЧНОЕ ДЛЯ НАСТРОЕК ЦИКЛИЧЕСКОГО РЕЖИМА (FLOAT)
PRESSURE_SPEED_CYCLE = 25           # СКОРОСТЬ ДАВЛЕНИЯ ДЛЯ НАСТРОЕК ЦИКЛИЧЕСКОГО РЕЖИМА (FLOAT)
TIME_PAUSE_CYCLE = 27               # ВРЕМЯ ПАУЗЫ ДЛЯ НАСТРОЕК ЦИКЛИЧЕСКОГО РЕЖИМА

NUMBER_OF_CYCLES = 28               # КОЛИЧЕСТВО ЦИКЛОВ
DROP_NUMBER_OF_CYCLES = 29          # СБРОС КОЛИЧЕСТВА ЦИКЛОВ
WARNING_SCREENS = 30                # ВСПЛЫВАЮЩИЕ ЭКРАНЫ
WARNING_BUTTON_BLOCK = 31           # КНОПКУ СТАРТ БЛОКИРУЕТ
WORK = 32                           # СТАТУС РАБОТЫ


# ОГРАНИЧЕНИЯ ДЛЯ ВВОДА ДАННЫХ

FREQ_MANUAL_MIN_MAX = [25, 100]
PRESSURE_END_MIN_MAX = [0, 38]
TIME_WAIT_MIN_MAX = [0, 999]
PRESSURE_SPEED_MIN_MAX = [0, 5]