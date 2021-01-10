import multiprocessing

bind = '0.0.0.0:8000'

# The number of running workers is calculated as two
# times the number of cores on the machine plus one.
workers = multiprocessing.cpu_count() * 2 + 1
