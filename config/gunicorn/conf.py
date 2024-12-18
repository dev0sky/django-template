from dotenv import load_dotenv
load_dotenv()
import os

name = f"{os.getenv('APP_NAME')}"

bind = f"api:{os.getenv('DJANGO_APP_PORT')}"
backlog = 1024 * 4

def get_workers():
    procs = os.sysconf('SC_NPROCESSORS_ONLN')
    if procs > 0:
        return procs * 2 + 1
    else:
        return 3

workers = get_workers()
worker_class = 'gevent'
worker_connections = 1000
timeout = 60 * 30  # 30 minutos

keepalive = 10

loglevel = 'info' 
errorlog = '-'
accesslog = '-'
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

def post_fork(server, worker):
    server.log.info("Worker spawned (pid: %s)", worker.pid)

def pre_fork(server, worker):
    pass

def pre_exec(server):
    server.log.info("Forked child, re-executing.")

def when_ready(server):
    server.log.info("Server is ready. Spawning workers")

def worker_int(worker):
    worker.log.info("worker received INT or QUIT signal")

    ## get traceback info
    import threading, sys, traceback
    id2name = {th.ident: th.name for th in threading.enumerate()}
    code = []
    for threadId, stack in sys._current_frames().items():
        code.append("\n# Thread: %s(%d)" % (id2name.get(threadId,""),
            threadId))
        for filename, lineno, name, line in traceback.extract_stack(stack):
            code.append('File: "%s", line %d, in %s' % (filename,
                lineno, name))
            if line:
                code.append("  %s" % (line.strip()))
    worker.log.debug("\n".join(code))

def worker_abort(worker):
    worker.log.info("worker received SIGABRT signal")