DjangoCMS on OpenShift Express
==============================

This git repository helps you get up and running quickly w/ a Django CMS installation
on OpenShift Express.  The Django project name used in this repo is 'mycms'
but you can feel free to change it.  Right now the backend is mysql. 

When you push this application up for the first time, the mysql database is
created, synced and migrated. It will then check to see if you have a django admin
user, if not it will create one and give it a default password. You should immediately
login to the django admin and change the password.

This repo was inspired by https://github.com/openshift/django-example and http://blog.ianweller.org/2011/05/12/openshift-express-first-thoughts/ Check them out, they were very helpful to me.

For more details, I have written a full blog post covering all of these steps in more detail at http://kencochrane.net/blog/2012/01/installing-django-application-on-openshift/

Running on OpenShift
----------------------------

Create an account at http://openshift.redhat.com/

install the client  (You need git installed first.) https://openshift.redhat.com/app/express#mac
Here are my steps for Mac OSX

    sudo gem install json_pure
    sudo gem install rhc

Create a domain. replace $mydoman and $loginemail with your own domain and the login email you used when creating an account.

    rhc-create-domain -n $mydomain -l $loginemail

Create a wsgi-3.2 application

    rhc-create-app -a blog -t wsgi-3.2

Add mysql to your app.

    rhc-ctl-app -a blog -e add-mysql-5.1
    
Add phpmyadmin to help you manage your database.

    rhc-ctl-app -a blog -e add-phpmyadmin-3.4

Add this upstream repo from github

    cd blog
    git remote add upstream -m master git://github.com/kencochrane/django-cms-openshift.git
    git pull -s recursive -X theirs upstream master

Then push the repo upstream

    git push

That's it, you can now checkout your application at (default admin account is admin/<password given at deploy time>):

    http://blog-$yournamespace.rhcloud.com

