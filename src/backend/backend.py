import ffmpy
from threading import Thread
import os
from time import sleep


def remove_file(path):
    try:
        os.remove(path)
    except Exception as e:
        pass


class Job:
    def __init__(self, thread, name, src, dest):
        self.thread = thread
        self.id = hash(self.thread)
        self.name = name
        self.dest_path = dest
        self.src_path = src

    def __str__(self):
        return str(self.name)

    def __repr__(self):
        return str(self)

    def is_done(self):
        return not self.thread.is_alive()

    def get_src_path(self):
        return self.src_path

    def get_dest_path(self):
        return self.dest_path


class Jobs:
    def __init__(self):
        self.jobs = []
        self.observers = []
        self.stop_poll_for_jobs = False
        self.t = Thread(target=self._poll_for_jobs)
        self.t.start()

    def _poll_for_jobs(self):
        while not self.stop_poll_for_jobs:
            for j in self.jobs:
                if j.is_done():
                    for o in self.observers:
                        o.notify(j)
            sleep(.5)

    def stop_polling_for_jobs(self, wait=False):
        self.stop_poll_for_jobs = True
        while wait and self.t.is_alive():
            sleep(.2)

    def add_job(self, thread, name, src_path, dest_path):
        j = Job(thread, name, src_path, dest_path)
        self.jobs.append(j)
        return j

    def remove_job(self, thread):
        for i in self.jobs[:]:
            if i.thread is thread:
                self.jobs.remove(i)

    def remove_job_by_id(self, id):
        for i in self.jobs[:]:
            if i.id == id:
                self.jobs.remove(i)

    def index_of(self, thread=None, name=None):
        for i, j in enumerate(self.jobs):
            if j.thread == thread:
                return i

    def index_of_id(self, id):
        for i, j in enumerate(self.jobs):
            if j.id == id:
                return i

    def get_job(self, id):
        for i in self.jobs:
            if i.id == id:
                return i

    def __iter__(self):
        return iter(self.jobs)

    def __getitem__(self, item):
        return self.jobs[item]


class Conversion:

    def run(self, runnable, *args):
        thread = Thread(target=runnable, args=args)
        thread.start()
        return thread

    def convert(self, input_path, conversion_extension, check_file_path=True, app_window=None):
        output_path, ext = os.path.splitext(input_path)
        output_path += ('.' if '.' not in conversion_extension else '') + conversion_extension
        if check_file_path is True and os.path.exists(output_path):
            raise FileExistsError
        elif input_path == output_path:
            raise FileExistsError
        else:
            remove_file(output_path)

        ff = ffmpy.FFmpeg(
            inputs={input_path: None},
            outputs={output_path: None})

        do_multi_thread = app_window is not None
        if do_multi_thread:
            return self.run(ff.run)
        else:
            ff.run()
        pass

    def get_supported_types(self):
        return sorted([
            'AIFF',
            'ASF',
            'AVI',
            'BFI',
            'CAF',
            'FLV',
            'GIF',
            'MP4',
            'MP3',
            'WAV',
            'MOV',
            'MPG4',
        ])
