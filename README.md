django-audit-log
===================

Introduction
===================

Important note
----------------------------

This version of `djnago-audit-log` requires a modified version of the [Django Framework](https://github.com/joshblum/django-with-audit.git) to run properly. This can be installed by running

    pip install -e git+https://github.com/joshblum/django-with-audit.git#egg=django

This version of Django has modifications made to the source to signal when objects are retrieved from the database.

What It Does
----------------------------

Lets you keep track of who changed what model instance in you Django application. Full model structure is tracked and kept in a separate table similar in structure to the original model table.

Let's say a user logs in the admin and adds a Product model instance. The audit log will track this in a separate table with the exact structure of you Product table plus a reference to the user, the time of the action and type of action
indicating it was an insert.

Next the user does an update of the same Product instance. The audit log table will keep the previous entry and another one will be added reflecting the change.

When the user deletes the same model instance the audit log table will have an entry indicating this with the state of the model before it was deleted.

What It Doesn't Do
----------------------------

The audit log bootstraps itself on each GET, POST, PUT or DELETE request. So it can only track changes to model instances when they are made via the web interface of your application. Note: issuing a delete in a PUT request will work without a problem (but don't do that). Saving model instances through the Django shell for instance won't reflect anything in the audit log. Neither will direct INSERT, UPDATE or DELETE statements, either within a request lifecycle or directly in your database shell.

Installation
----------------------------

Install with `pip`

    pip install -e https://github.com/joshblum/django-audit-log#egg=audit_log

to hack on the code you can symlink the package in your site-packages from the source tree

    python setup.py develop


Adding the package `'audit_log'` to your `INSTALLED_APPS` tuple will allow admin interface tracking for models with audit logs. 

    
    INSTALLED_APPS = (
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.sites',
        ...
        'audit_log',
        ...
    )

You also need to modify in your `settings.py` by adding  `audit_log.middleware.UserLoggingMiddleware` to the `MIDDLEWARE_CLASSES` tuple

    
    MIDDLEWARE_CLASSES = (
        'django.middleware.common.CommonMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        ...
        'audit_log.middleware.UserLoggingMiddleware',
        ...
    )


Usage
----------------------------

Tracking changes on a model
----------------------------

In order to enable change tracking on a model, the models needs to have a 
property of type `audit_log.models.managers.AuditLog` attached::


    from django.db import models
    from audit_log.models.fields import LastUserField
    from audit_log.models.managers import AuditLog

    
    class ProductCategory(models.Model):
        name = models.CharField(max_length=150, primary_key = True)
        description = models.TextField()
       
        audit_log = AuditLog() 

    class Product(models.Model):
        name = models.CharField(max_length = 150)
        description = models.TextField()
        price = models.DecimalField(max_digits = 10, decimal_places = 2)
        category = models.ForeignKey(ProductCategory)

        audit_log = AuditLog()


Each time you add an instance of AuditLog to any of your models you need to run 
`python manage.py syncdb` so that the database table that keeps the actual 
audit log for the given model gets created.   


Querying the audit log
-------------------------------

An instance of `audit_log.models.managers.AuditLog` will behave much like a 
standard manager in your model. Assuming the above model 
configuration you can go ahead and create/edit/delete instances of Product,  to query all the changes that were made to the products table you would need to retrieve all the entries for the audit log for that particular model class::

    In [2]: Product.audit_log.all()
    Out[2]: [<ProductAuditLogEntry: Product: My widget changed at 2011-02-25 06:04:29.292363>,
            <ProductAuditLogEntry: Product: My widget changed at 2011-02-25 06:04:24.898991>,
            <ProductAuditLogEntry: Product: My Gadget super changed at 2011-02-25 06:04:15.448934>,
            <ProductAuditLogEntry: Product: My Gadget changed at 2011-02-25 06:04:06.566589>,
            <ProductAuditLogEntry: Product: My Gadget created at 2011-02-25 06:03:57.751222>, 
            <ProductAuditLogEntry: Product: My widget created at 2011-02-25 06:03:42.027220>]

Accordingly you can get the changes made to a particular model instance like so::

    In [4]: Product.objects.all()[0].audit_log.all()
    Out[4]: [<ProductAuditLogEntry: Product: My widget changed at 2011-02-25 06:04:29.292363>,
            <ProductAuditLogEntry: Product: My widget changed at 2011-02-25 06:04:24.898991>,
            <ProductAuditLogEntry: Product: My widget created at 2011-02-25 06:03:42.027220>]

Instances of `AuditLog` behave like django model managers and can be queried in the same fashion.

The querysets yielded by `AuditLog` managers are querysets for models  of type `[X]AuditLogEntry`, where X is the tracked model class. An instance of `XAuditLogEntry` represents a log entry for a particular model instance and will have the following fields that are of relevance:

* `action_id` - Primary key for the log entry.
* `action_date` - The point in time when the logged action was performed.
* `action_user` - The user that performed the logged action.
* `action_type` - The type of the action (Created/Changed/Deleted/Read)
* `action_ip` - The IP address of the request perform the logged action.
* `action_referrer` - The HTTP-Referrer of the request perform the logged action.
* `action_user_agent` - The User-Agent of the request perform the logged action.
* `is_new` - Boolean indicating whether the object has been viewed before.
*  `object_state` Any field of the original `X` model that is tracked by the audit log.
