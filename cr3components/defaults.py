from cr3components import GlobalSettings
gs = GlobalSettings()

for k,v in gs.items():
    globals()[k] = v

import os
import socket

BASE_DIR = apply(os.path.join, os.path.split(ROOT_PATH)[0:-1]) #cd ..

host = socket.gethostbyaddr(socket.gethostname())
hostname = host[0].split(".")[0]

HOME = os.environ['HOME']
USER = os.environ['USER']


INTERNAL_IPS = ('127.0.0.1',)

ADMINS = (
     ('Support', 'support+%s@cr3studio.com' % PROJECT),
)

MANAGERS = ADMINS

# lighttpd fix
FORCE_SCRIPT_NAME = ""

HOSTCONFIG = {
    'ichi' : {
        'DATABASES' : {
            'default': {
                'ENGINE': 'django.db.backends.postgresql_psycopg2',
                'NAME':USER,
                'USER':USER,
                'PASSWORD':DBPASS,
            }
        },
        'DEBUG' : False,
    },
    'alf' : {
        'DATABASES' : {
            'default': {
                'ENGINE': 'django.db.backends.postgresql_psycopg2',
                'NAME':USER,
                'USER':USER,
                'PASSWORD':DBPASS,
            }
        },
        'DEBUG' : True,
    },
    'delta' : {
        'DATABASES' : {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': '%s.db' % PROJECT
            }
        },
        'DEBUG' : True,
    }
}

DATABASES = HOSTCONFIG[hostname]['DATABASES']
DEBUG = HOSTCONFIG[hostname]['DEBUG']


TIME_ZONE = 'Europe/Warsaw'

LANGUAGE_CODE = 'pl'

USE_I18N = True
USE_L10N = True

_ = lambda s: s
LANGUAGES = (
  ('pl', _('Polish')),
  ('en', _('English')),
)

LANGUAGES_FALLBACK = {
    'en':'pl',
}

SITE_ID = 1

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

STATICFILES_DIRS = (
    os.path.join(ROOT_PATH, "static"),
)

MEDIA_URL = '/media/'
MEDIA_SECURE_URL = MEDIA_URL


STATIC_URL = '/static/'

ADMIN_MEDIA_PREFIX = '/static/admin/'


MIDDLEWARE_CLASSES = (
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.doc.XViewMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'pandora.middleware.UserMiddleware',
    'pandora.middleware.RequestMiddleware',
    'cr3components.cms.middleware.CmsMiddleware',
)
if DEBUG:
    MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware',)

ROOT_URLCONF = '%s.urls' % PROJECT


INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.databrowse',
    'django.contrib.sitemaps',
    'django.contrib.messages',
    'mptt',
    'cr3components.cms',
    'cr3components.banners',
    'cr3components.templateasoption',
    'convert',
    'markitup',
    'convert',
    'uni_form',
    'compressor',
)
INSTALLED_APPS += ('gunicorn',) #add to cms template & bt3 template
INSTALLED_APPS += ('haystack',) #add to cms template & bt3 template

if DEBUG:
    INSTALLED_APPS += ('debug_toolbar',)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.eggs.Loader',
)

TEMPLATE_DIRS = (
    os.path.join(ROOT_PATH, "templates"),
)


TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.request',
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
    'cr3components.cms.context_processors.cms',
)

STATICFILES_DIRS = (
    os.path.join(ROOT_PATH, "static"),
)

DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS':False
}

DEBUG_TOOLBAR_PANELS = (
    'debug_toolbar.panels.version.VersionDebugPanel',
    'debug_toolbar.panels.timer.TimerDebugPanel',
    'debug_toolbar.panels.settings_vars.SettingsVarsDebugPanel',
    'debug_toolbar.panels.headers.HeaderDebugPanel',
    'debug_toolbar.panels.request_vars.RequestVarsDebugPanel',
    'debug_toolbar.panels.template.TemplateDebugPanel',
    'debug_toolbar.panels.sql.SQLDebugPanel',
    'debug_toolbar.panels.signals.SignalDebugPanel',
    'debug_toolbar.panels.logger.LoggingPanel',
)

TEMPLATESADMIN_EDITHOOKS = (    
    'templatesadmin.edithooks.gitcommit.GitCommitHook',
)


EMAIL_HOST = 'localhost'
DEFAULT_FROM_EMAIL = 'webmaster@localhost'
LOGIN_REDIRECT_URL = '/'


#module: MarkitUp
MARKITUP_MEDIA_URL = "%s" % STATIC_URL
#MARKITUP_FILTER = ('django.contrib.markup.templatetags.markup.textile', {})
MARKITUP_FILTER = ('markdown.markdown', {'safe_mode': False})
MARKITUP_SET = 'markitup/sets/markdown'
MARKITUP_SKIN = 'markitup/skins/simple'
#actual recommendation is markdown. In some future multimarkdown will be introduced

#module: Compress
COMPRESS_STORAGE = "staticfiles.storage.StaticFileStorage"
COMPRESS_URL = STATIC_URL
COMPRESS_ROOT = STATIC_ROOT
COMPRESS = True

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': PROJECT,
        'KEY_PREFIX': PROJECT,
    }
}

COMPILER_FORMATS = {
    '.less': {
        'binary_path': 'lessc',
        'arguments': '*.less *.css',
    },
}

COMPRESS_CSS_FILTERS = ['compressor.filters.css_default.CssAbsoluteFilter']
#COMPRESS_CSS_FILTERS = ['compressor.filters.yui.YUICompressorFilter']
COMPRESS_JS_FILTERS = ['compressor.filters.jsmin.JSMinFilter']
COMPRESS_YUI_BINARY = 'java -jar yuicompressor-2.4.2.jar'


# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request':{
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

CR3SETTINGS = {}

CR3CMS_PAGE_SUFFIX = ".html" #not yet supported
