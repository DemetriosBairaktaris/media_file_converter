import pytest
from threading import Thread
from time import sleep
from tempfile import NamedTemporaryFile
import os

from test.files import file_utils
from src.backend import backend
from src.gui import widgets


def test_():
    pass


class Contexts:
    class JobsContext:
        def __init__(self):
            self.jobs = None

        def __enter__(self):
            self.jobs = backend.Jobs()
            return self.jobs

        def __exit__(self, exc_type, exc_val, exc_tb):
            self.jobs.stop_polling_for_jobs()


class Fixtures:
    seconds = 30

    @staticmethod
    def create_job():
        name = 'name'
        src = 'src'
        dest = 'dest'
        t = Thread(target=lambda *args: [sleep(1) for x in range(Fixtures.seconds)])
        return backend.Job(t, name, src, dest)

    @staticmethod
    @pytest.fixture()
    def job():
        return Fixtures.create_job()

    @staticmethod
    @pytest.fixture()
    def list_of_jobs():
        return [Fixtures.create_job() for i in range(10)]


# Fixtures
job = Fixtures.job
list_of_jobs = Fixtures.list_of_jobs


class TestJob:

    def test_str_representation(self, job):
        assert str(job) == 'name'
        assert repr(job) == 'name'

    def test_create_job(self, job):
        """
        Create a job with thread and assert thread is running
        :return:
        """
        Fixtures.seconds = 30
        job.thread.start()
        assert 'dest' == job.get_dest_path()
        assert 'src' == job.get_src_path()
        assert not job.is_done()

    def test_job_is_done(self, job):
        """
        Creat Job and assure the thread is done
        :return:
        """
        Fixtures.seconds = 5
        job.thread.start()
        assert not job.is_done()
        sleep(6)
        assert job.is_done()

    def test_implicit_job_id(self, job):
        t = job.thread
        id = hash(t)
        assert id == job.id


class TestJobs:

    def test_index(self, job):
        with Contexts.JobsContext() as jobs:
            jobs.add_job(job.thread, job.name, job.src_path, job.dest_path)
            assert job == jobs[0]

    def test_get_job_by_id(self, job):
        with Contexts.JobsContext() as jobs:
            jobs.add_job(job.thread, job.name, job.src_path, job.dest_path)
            assert job == jobs.get_job(job.id)

    def test_add_job(self, job):
        """
        add a simple job
        :param job:
        :return:
        """
        with Contexts.JobsContext() as jobs:
            jobs.add_job(job.thread, job.name, job.src_path, job.dest_path)
            assert jobs.jobs[0]

    def test_add_jobs(self, list_of_jobs):
        """
        Add many jobs and make sure they are running
        :param list_of_jobs:
        :return:
        """
        Fixtures.seconds = 30
        with Contexts.JobsContext() as jobs:
            for job in list_of_jobs:
                jobs.add_job(job.thread, job.name, job.src_path, job.dest_path)
                job.thread.start()

            for job in jobs:
                assert not job.is_done()

    def test_remove_job_by_id(self, job):
        """
        add a job and remove it by id assert it is gone
        :param job:
        :return:
        """
        with Contexts.JobsContext() as jobs:
            jobs.add_job(job.thread, job.name, job.src_path, job.dest_path)
            jobs.remove_job_by_id(hash(job.thread))

            assert len(jobs.jobs) == 0

    def test_add_observer_and_observe(self, job):
        with Contexts.JobsContext() as jobs:
            Fixtures.seconds = 1

            class Observer:
                def __init__(self):
                    self.notified = False

                def notify(self, *args):
                    self.notified = True

            o = Observer()

            jobs.observers.append(o)
            jobs.add_job(job.thread, job.name, job.src_path, job.dest_path)
            job.thread.start()
            sleep(6)
            assert o.notified

    def test_index_of_job_id(self, job):
        Fixtures.seconds = 5
        with Contexts.JobsContext() as jobs:
            jobs.add_job(job.thread, job.name, job.src_path, job.dest_path)
            job.thread.start()
            assert 0 == jobs.index_of_id(job.id)


class TestConversion:

    def test_run(self):
        assert backend.Conversion().run(lambda: sleep(3)).is_alive()

    def test_same_dest_path_as_src_path(self):
        """
            Test that the conversion backend throws a FileExistsError if the conversion would yield same file type.
            Should be agnostic to whether the extension has a . or not.
        :return:
        """
        with pytest.raises(FileExistsError):
            assert backend.Conversion().convert('/path/path/path.mp3', 'mp3')
            assert backend.Conversion().convert('/path/path/d.mp3', '.mp3')

    def test_file_path_(self):
        with pytest.raises(FileExistsError):
            assert backend.Conversion().convert(file_utils.get_file_by_type('mp3'), 'wav')

    def test_convert_with_multi_thread(self):
        c = backend.Conversion()
        c.convert(file_utils.get_file_by_type('wav', prefix='real_'), 'mp3', check_file_path=False).join()
        assert os.path.exists(file_utils.get_file_by_type('mp3', prefix='real_'))
        os.remove(file_utils.get_file_by_type('mp3', prefix='real_'))

    def test_convert_no_multi_thread(self):
        c = backend.Conversion()
        c.convert(file_utils.get_file_by_type('wav', prefix='real_'), 'mp3', check_file_path=False, do_multi_thread=False)
        assert os.path.exists(file_utils.get_file_by_type('mp3', prefix='real_'))
        os.remove(file_utils.get_file_by_type('mp3', prefix='real_'))


def test_remove_file():
    t = NamedTemporaryFile('w', delete=False)
    t.close()
    assert os.path.exists(t.name)
    assert backend.remove_file(t.name)
    assert not os.path.exists(t.name)


def test_remove_file_not_exists():
    """try to remove a file that does not exist, and it should not throw a exception"""
    assert not os.path.exists('/c/d/e/r/f/d/d/e/3')
    assert not backend.remove_file('/c/d/e/r/f/d/d/e/3')


def test_extended_widget_list_item():
    """Tests how the widget list item's state should be"""
    assert widgets.ExtendedQListWidgetItem('id').id == 'id'


def test_extended_widget_list_item_original_text():
    assert widgets.ExtendedQListWidgetItem('id', 'text').original_text == 'text'


def test_extended_widget_list_item_original_text_changed():
    e = widgets.ExtendedQListWidgetItem('id', 'text')
    e.set_done(True)
    assert e.text().lower().endswith('done')


def test_extended_widget_list_item_original_text_changed_x_times():
    e = widgets.ExtendedQListWidgetItem('id', 'text')
    e.set_done(True)
    e.set_done(True)
    e.set_done(True)
    assert e.text().lower().endswith('done')
    assert e.text().lower().count('done') == 1
