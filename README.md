# refactored-waffle


Инструкция:

<strong>1. Запуск стенда:</strong>

- Установить на выделенный компьютер или ВМ Ansible `sudo apt install ansible`;

- Создать или клонировать 4 ВМ (например Ubuntu Server 22.04 LTS);

- Запустить все ВМ, а также ansible-машину под одной сетью;

- С ansible машины выполнить плейбуки из папки playbooks/ командой: 

`ansible-playbook -i hosts.ini -k playbook/path/to_playbook --ask-become-pass` в следующем порядке: 

1. Настройка сети и хоста - network_pb.yml; 
2. Установка и настройка fluentbit - fluentbit.yml;
3. Установка docker и запуск приложения на сервере - install_services.yml (только для ВМ сервера).

- Удостовериться, что сервис fluent.bit запущен: `sudo systemctl status fluent-bit.service`

<strong>2. Проведение экспериментов:</strong>

После запуска настройки всех ВМ и запуска приложения на сервере необходимо донастроить Apache Airflow:

- `ansible-playbook -i hosts.ini -k server/setup_airflow.yml --ask-become-pass`;
- Проверить, что все сервисы на ВМ server работают: `docker ps -a`;
- Проверить, что логи поступают и записываются в папку /home/logs на ВМ log.

Для имитации нормального процесса запустить скрипты normal_activity.sh с ВМ wp1 и wp2. Как пример аномалии, запустить anomaly.sh с ВМ wp1.В дальнейшем создание аномалий можно производить вручную.

<strong>3. Поиск аномалий:</strong>

- Подготовить модели глубокого обучения для анализа логов `git clone https://github.com/w19z/logbert.git`
- Настроить виртуальную среду в соответствии с инструкцией в репозитории;
- После сбора логов, скачать файлы с собранными логами с ВМ logs в папку logbert/preprocessing/logs_out: docker.app, docker.db, docker.jupyter, wp1_sshd, wp2_sshd, sshd;

Подготовить файл comb_structured.csv с помощью блокнота preprocessing.ipynb (logbert/preprocessing).

4. Произвести обучение и тестирование моделей в соответсвии с инструкции logbert.
Пример:
```
cd logbert
. venv/bin/activate
cd logbert/custom
python data_process.py
python loganomaly.py vocab
# set [num_classes] = vocab in loganomaly.py
python loganomaly.py train
python loganomaly.py predict
```




