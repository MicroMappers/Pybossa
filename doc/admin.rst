======================
Administrating PyBossa
======================

PyBossa has three type of users: anonymous, authenticated and administrators.
By default the first created user in a PyBossa server will become an
administrator and manage the site with full privileges.

And admin user will be able to access the admin page by clicking in the user
name and then in the link *Admin site*.

.. image:: http://i.imgur.com/Xm6c42x.png

Administrators can manage three different areas of the server:

 1. Featured projects
 2. Categories, and
 3. Administrators

.. image:: http://i.imgur.com/CIVyRak.png
    :width:100%

.. note::
    Admins can also modify all projects, and also see which projects are marked
    as **Draft**: projects that do not have at least one task and
    a :ref:`task-presenter` to allow other volunteers to participate.

.. note::
    A fourth option is available on the Admin Site menu. Here, admins will be able
    to obtain a list of all registered users in the PyBossa system, in either
    json or csv formats.

.. note::
    In addition, admins can access an extension called `RQ dashboard`_ from where to
    monitor all the background jobs and even cancel them or retry failed ones.

.. _`RQ dashboard`: https://github.com/nvie/rq-dashboard
.. _featured-projects:

Featured Projects
=================

In this section, admins can add/remove projects to the front page of the
site. 

.. image:: http://i.imgur.com/Jpr3bGh.png
    :width:100%

Basically, you will see a green button to add a project to the Featured
selection, or a red one to remove it from the front page.


.. _categories:

Categories
==========

PyBossa provides by default two type of categories:

1. **Thinking**: for projects where the users can use their skills to solve
   a problem (i.e. image or sound pattern recognition).
2. **Sensing**: for projects where the users can help gathering data using
   tools like EpiCollect_ and then analyze the data in the PyBossa server.

Admins can add as many categories as they want, just type then and its
description and click in the green button labeled: Add category.

.. _EpiCollect: http://plus.epicollect.net

.. image:: http://i.imgur.com/otR6wcG.png
    :width: 100%

.. note::
    You cannot delete a category if it has one or more projects associated
    with it. You can however rename the category or delete it when all the
    associated projects are not linked to the given category.


.. _administrators:

Administrators
==============

In this section an administrator will be able to add/remove users to the admin
role. Basically, you can search by user name -nick name- and add them to the
admin group.

.. image:: http://i.imgur.com/IdDKo8P.png
    :width:100%

As with the :ref:`categories` section, a green button will allow you to add the user
to the admin group, while a red button will be shown to remove the user from
the admin group.


Audit log
=========

When a project is created, deleted or updated, the system registers its actions
in the server. Admins will have access to all the logged actions in every
project page, in a section named **Audit log**.

.. image:: http://i.imgur.com/UQeyHPF.png
    :width: 100%

The section will let you know the following information:

- **When**: when the action was taken.
- **Action**: which action was taken: 'created', 'updated', or 'deleted'.
- **Source**: if it was done the action via the API or the WEB interface.
- **Attribute**: which attribute of the project has been changed.
- **Who**: the user who took the action.
- **Old value**: the previous value before the action.
- **New value**: the new value after the action.

.. note::
    Only admins and users marked as *pro* can see the audit log.

Dashboard
=========

The dashboard allows you to see what's going on in your PyBossa server.

.. image:: http://i.imgur.com/CpgclS1.png

.. note::
    This feature requires PostgreSQL >= 9.3. Please upgrade as soon as possible your
    server to have this feature.

The dashboard shows the following information for the last 7 days:

- **Active users**: Number of users that have contributed at least 1 task_run in the last 7 days.
- **Active anonymous users**: Number of anonymous users that have contributed at least 1 task_run in the last 7 days.
- **New projects**: Projects created in the last 7 days.
- **Updated projects**: Updated projects in the last 7 days.
- **Updated projects**: Updated projects in the last 7 days.
- **New users**: Number of new users registered in the last 7 days.
- **Number of returning users**: Number of returning users in the last 7 days classified by number of days coming back.
- **Recent activity feed**: Last events in real time of the server.

The dashboard is updated every 24 hours via the background jobs. These jobs are scheduled in the *low* queue.
