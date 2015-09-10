# -*- coding: utf8 -*-
# This file is part of PyBossa.
#
# Copyright (C) 2014 SF Isle of Man Limited
#
# PyBossa is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# PyBossa is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with PyBossa.  If not, see <http://www.gnu.org/licenses/>.
# Cache global variables for timeouts
"""
CSV Exporter module for exporting tasks and tasks results out of PyBossa
"""

from pybossa.exporter import Exporter
import tempfile
from pybossa.core import uploader, task_repo
from pybossa.model.task import Task
from pybossa.model.task_run import TaskRun
from flask.ext.babel import gettext
from pybossa.util import UnicodeWriter
import pybossa.model as model
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
from flask import abort


class CsvExporter(Exporter):

    def _format_csv_properly(self, row, ty=None):
        tmp = row.keys()
        task_keys = []
        for k in tmp:
            k = "%s__%s" % (ty, k)
            task_keys.append(k)
        if (type(row['info']) == dict):
            task_info_keys = []
            tmp = row['info'].keys()
            for k in tmp:
                k = "%sinfo__%s" % (ty, k)
                task_info_keys.append(k)
        else:
            task_info_keys = []

        keys = sorted(task_keys + task_info_keys)
        values = []
        _prefix = "%sinfo" % ty
        for k in keys:
            prefix, k = k.split("__")
            if prefix == _prefix:
                if row['info'].get(k) is not None:
                    values.append(row['info'][k])
                else:
                    values.append(None)
            else:
                if row.get(k) is not None:
                    values.append(row[k])
                else:
                    values.append(None)

        return values

    def _handle_task(self, writer, t):
        writer.writerow(self._format_csv_properly(t.dictize(), ty='task'))

    def _handle_task_run(self, writer, t):
        writer.writerow(self._format_csv_properly(t.dictize(), ty='taskrun'))

    def _get_csv(self, out, writer, table, handle_row, id):
        for tr in getattr(task_repo, 'filter_%ss_by' % table)(project_id=id,
                                                              yielded=True):
            handle_row(writer, tr)
        out.seek(0)
        yield out.read()

    def _respond_csv(self, ty, id):
        try:
            # Export Task(/Runs) to CSV
            types = {
                "task": (
                    model.task.Task, self._handle_task,
                    (lambda x: True),
                    gettext(
                        "Oops, the project does not have tasks to \
                        export, if you are the owner add some tasks")),
                "task_run": (
                    model.task_run.TaskRun, self._handle_task_run,
                    (lambda x: True),
                    gettext(
                        "Oops, there are no Task Runs yet to export, invite \
                         some users to participate"))}
            try:
                table, handle_row, test, msg = types[ty]
            except KeyError:
                return abort(404)  # TODO!

            out = tempfile.TemporaryFile()
            writer = UnicodeWriter(out)
            t = getattr(task_repo, 'get_%s_by' % ty)(project_id=id)
            if t is not None:
                if test(t):
                    tmp = t.dictize().keys()
                    task_keys = []
                    for k in tmp:
                        k = "%s__%s" % (ty, k)
                        task_keys.append(k)
                    if (type(t.info) == dict):
                        task_info_keys = []
                        tmp = t.info.keys()
                        for k in tmp:
                            k = "%sinfo__%s" % (ty, k)
                            task_info_keys.append(k)
                    else:
                        task_info_keys = []
                    keys = task_keys + task_info_keys
                    writer.writerow(sorted(keys))

                return self._get_csv(out, writer, ty, handle_row, id)
            else:
                pass  # TODO
        except:  # pragma: no cover
            raise

    def _make_zip(self, project, ty):
        name = self._project_name_latin_encoded(project)
        csv_task_generator = self._respond_csv(ty, project.id)
        if csv_task_generator is not None:
            # TODO: use temp file from csv generation directly
            datafile = tempfile.NamedTemporaryFile()
            try:
                for line in csv_task_generator:
                    datafile.write(str(line))
                datafile.flush()
                csv_task_generator.close()  # delete temp csv file
                zipped_datafile = tempfile.NamedTemporaryFile()
                try:
                    zip = self._zip_factory(zipped_datafile.name)
                    zip.write(
                        datafile.name, secure_filename('%s_%s.csv' % (name, ty)))
                    zip.close()
                    container = "user_%d" % project.owner_id
                    file = FileStorage(
                        filename=self.download_name(project, ty), stream=zipped_datafile)
                    uploader.upload_file(file, container=container)
                finally:
                    zipped_datafile.close()
            finally:
                datafile.close()

    def download_name(self, project, ty):
        return super(CsvExporter, self).download_name(project, ty, 'csv')

    def pregenerate_zip_files(self, project):
        print "%d (csv)" % project.id
        self._make_zip(project, "task")
        self._make_zip(project, "task_run")
