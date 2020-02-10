import ffmpy
from threading import Thread
import os
from time import sleep

IS_TEST = False

def remove_file(path):
    try:
        os.remove(path)
        return True
    except Exception as e:
        e = "Couldn't remove file, {}".format(str(e))
        print(e)
        return False


class CustomThread(Thread):

    def __init__(self, *args, **kwargs):
        super(CustomThread, self).__init__(*args, **kwargs)
        self.started = False

    def custom_start(self):
        self.started = True
        super(CustomThread, self).start()


class Job:
    def __init__(self, thread, name, src, dest):
        self.thread: CustomThread = thread
        self.id = hash(self.thread)
        self.name = name
        self.dest_path = dest
        self.src_path = src

    def __str__(self):
        return str(self.name)

    def __repr__(self):
        return str(self)

    def is_done(self):
        return not self.thread.is_alive() and self.thread.started

    def get_src_path(self):
        return self.src_path

    def get_dest_path(self):
        return self.dest_path

    def __eq__(self, other):
        return self.id == other.id


class Jobs:
    def __init__(self):
        self.jobs = []
        self.observers = []
        self.stop_poll_for_jobs = False
        self.t = CustomThread(target=self._poll_for_jobs)
        self.t.custom_start()

    def _poll_for_jobs(self):
        while not self.stop_poll_for_jobs:
            for j in self.jobs:
                if j.is_done():
                    for o in self.observers:
                        o.notify(j)
            sleep(.3)

    def stop_polling_for_jobs(self, wait=False):
        self.stop_poll_for_jobs = True
        while wait and self.t.is_alive():
            sleep(.2)

    def add_job(self, thread, name, src_path, dest_path):
        j = Job(thread, name, src_path, dest_path)
        self.jobs.append(j)
        return j

    def remove_job_by_id(self, id):
        for i in self.jobs[:]:
            if i.id == id:
                self.jobs.remove(i)

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

    def __init__(self):
        self.output_paths = {}

    def get_last_output_path(self, source):
        return self.output_paths[source]

    def run(self, runnable, *args):
        thread = CustomThread(target=runnable, args=args)
        thread.custom_start()
        return thread

    def get_output_path(self, input_path, extension):
        if IS_TEST:
            from src.util import naming_utils
            temp_name = naming_utils.get_temp_file_name(extension)
            output_path = os.path.join(os.path.dirname(input_path), temp_name)
        else:
            input_path_no_ext, ext = os.path.splitext(input_path)
            output_path = input_path_no_ext + ('.' if '.' not in extension else '') + extension
        return output_path

    def convert(self, input_path, conversion_extension, check_file_path=True, do_multi_thread=True):

        output_path = self.get_output_path(input_path, conversion_extension)
        if check_file_path is True and os.path.exists(output_path):
            raise FileExistsError
        elif input_path == output_path:
            raise FileExistsError
        else:
            remove_file(output_path)

        ff = ffmpy.FFmpeg(
            inputs={input_path: None},
            outputs={output_path: None})

        self.output_paths[input_path] = output_path
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
