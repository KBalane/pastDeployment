bind = 'unix:/tmp/gunicorn-digiinsurance.sock'
backlog = 2048
workers = 5
worker_class = 'sync'
worker_connections = 1000
timeout = 60
keepalive = 2
spew = False
daemon = False
pidfile = None
umask = 0
user = None
group = None
tmp_upload_dir = None
errorlog = '/var/log/gunicorn-digiinsurance.log'
accesslog = '/var/log/gunicorn-digiinsurance.log'
loglevel = 'info'
proc_name = "digiinsurance"

# restart worker after max_requests to limit memory leaks
max_requests = 300


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

    # get traceback info
    import threading, sys, traceback
    id2name = dict([(th.ident, th.name) for th in threading.enumerate()])
    code = []
    for threadId, stack in sys._current_frames().items():
        code.append(
            "\n# Thread: %s(%d)" % (id2name.get(threadId, ""), threadId))
        for filename, lineno, name, line in traceback.extract_stack(stack):
            code.append(
                'File: "%s", line %d, in %s' % (filename, lineno, name))

            if line:
                code.append("  %s" % (line.strip()))
    worker.log.debug("\n".join(code))


def worker_abort(worker):
    worker.log.info("worker received SIGABRT signal")
