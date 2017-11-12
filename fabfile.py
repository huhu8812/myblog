#coding:utf8
from fabric.api import env, run
from fabric.operations import sudo

GIT_REPO = "https://github.com/huhu8812/myblog.git"

env.user = "huhu"
env.password = 'huhu8812'

env.hosts = ['huhu8812.tech']
env.port = '26582'

def deploy():
        source_folder = '/home/huhu/websites/huhu8812.tech/myblog'
        run('cd %s && git pull' % source_folder)
        run("""
        cd {} &&
        pip install -r requirements.txt &&
        python manage.py collectstatic --noinput &&
        python manage.py migrate
        """.format(source_folder))
        sudo('restart gunicorn-huhu8812.tech')
        sudo('service nginx reload')