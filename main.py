import threading
from queue import Queue
from spider import Spider
from domain import *
from makeDir import *

# Makes a directory as the name of the project
PROJECT_NAME = 'newboston'

# Web page to crawl
HOMEPAGE = 'https://thenewboston.com'
DOMAIN_NAME = get_domain_name(HOMEPAGE)

# Create queue file
QUEUE_FILE = PROJECT_NAME + '/queue.txt'

# Create crawled file
CRAWLED_FILE = PROJECT_NAME + '/crawled.txt'

# Set number of threads as per computer specification
NUMBER_OF_THREADS = 4

queue = Queue()

# Create spider
Spider(PROJECT_NAME, HOMEPAGE, DOMAIN_NAME)

# Create threads
def create_workers():
    for i in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()


# Next link in queue
def work():
    while True:
        url = queue.get()
        Spider.crawl_page(threading.current_thread().name, url)
        queue.task_done()


# Each queue link new job
def create_jobs():
    for link in file_to_set(QUEUE_FILE):
        queue.put(link)
    queue.join()
    crawl()


# Check queue
def crawl():
    queued_links = file_to_set(QUEUE_FILE)
    if len(queued_links)>0:
        print(str(len(queued_links)) + ' links in queue')
        create_jobs()


create_workers()
crawl()