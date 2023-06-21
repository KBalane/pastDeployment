# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'digiinsurance',
        'USER': 'doadmin',
        'PASSWORD': 'qkzmyludhmr5s2k8',
        'HOST': 'db-mysql-sgp1-52145-do-user-6523329-0.b.db.ondigitalocean.com',
        'PORT': '25060',
    }
    # 'default': {
    #     'ENGINE': 'django.db.backends.mysql',
    #     'NAME': 'coco',
    #     'USER': 'root',
    #     'PASSWORD': 'pogiako69_',
    #     'HOST': 'localhost',
    #     'PORT': '3306',
    # }
}
