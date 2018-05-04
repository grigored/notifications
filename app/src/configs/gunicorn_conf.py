from multiprocessing import cpu_count
import os

# bind = '0.0.0.0:443'
bind = '0.0.0.0:8006'
workers = 1  # cpu_count() * 2 + 1
daemon = False
threads = 10
preload_app = False
proc_name = 'notification-server'
worker_class = 'gthread'
# pidfile = '/application/instacar-back/pid.txt'
# logfile = '/application/instacar-back/services/backend/results.log'
# pythonpath = 'app'
loglevel = 'info'

# ssl config
# keyfile = '/app/example.key'
# certfile = '/app/api_instacarshare_com.crt'
# ca_certs = '/app/bundle.crt'
