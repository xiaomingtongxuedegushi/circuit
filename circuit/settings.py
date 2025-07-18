"""
Django settings for circuit project.

Generated by 'django-admin startproject' using Django 3.1.6.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '!@#nm_!_n(_&)3)algnqq2gjj^nso5hw8a3@%124+5)+oh-ako'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'simpleui',
    'import_export',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'django_filters',
    'corsheaders',
    'data',
    'question',
    'usermanage',
    'examination',
    'curriculum',
    'contest',
    'electron'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'circuit.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'circuit.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        # 'NAME': BASE_DIR / 'db.sqlite3',
        'NAME': str(os.path.join(BASE_DIR, "db.sqlite3"))
    },

    # 'default': {
    #     'ENGINE': 'django.db.backends.mysql', # 数据库引擎
    #     'NAME': 'circuit', # 数据库名
    #     'USER': 'lys', # 账号
    #     'PASSWORD': '0807liu..', # 密码
    #     'HOST': '43.248.186.198', # HOST
    #     'POST': 3306, # 端口

    # }
}

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

REST_FRAMEWORK = {
    # 'DEFAULT_RENDERER_CLASSES': ('rest_framework.renderers.JSONRenderer',),
    'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend',)
}

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
MEDIA_URL = '/upload/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'upload').replace('\\', '/')
# MEDIA_ROOT = os.path.join(BASE_DIR, 'upload')
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_WHITELIST = (
    'http://192.168.10.101',
    'http://localhost:8081',
    'http://192.168.31.144',
    'http://pdf.car.com',
    'http://stu.car.com',
    'http://quick.car.com',
    'http://quicktable.car.com',
    'http://quconchoice.car.com',
    'http://127.0.0.1:8091',
    'http://127.0.0.1:8082',
    # 'http://192.168.1.103:9000/',
    'http://127.0.0.1',
    # "http://192.168.1.103:9000",

    # '*.*.*.*'

)
CORS_ALLOW_METHODS = (
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
    'VIEW',
)
CORS_ALLOW_HEADERS = (
    'XMLHttpRequest',
    'X_FILENAME',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
    'Pragma',
)
SIMPLEUI_DEFAULT_THEME = 'simpleui.css'
SIMPLEUI_HOME_INFO = False
SIMPLEUI_ANALYSIS = False
SIMPLEUI_STATIC_OFFLINE = True
SIMPLEUI_CONFIG = {
    'system_keep': False,
    # 'menu_display': ['故障管理', '课程系统', '考试系统', '题库管理', '用户管理','auth'],
    'dynamic': True,
    'menus': [
        # {
        #     'name': '故障管理',
        #     'codename': 'data',
        #     'icon': 'el-icon-warning',
        #     'models': [{
        #         'name': '故障设置',
        #         'codename': 'add_fault',
        #         'url': 'data/fault'
        #     },{
        #         'name': '串口设置',
        #         'codename': 'add_serial',
        #         'icon': 'el-icon-setting',
        #         'url': 'data/serial'
        #     }]
        # },
        {
            'name': '课程系统',
            'codename': 'curriculum',
            'icon': 'el-icon-data-analysis',
            'models': [{
                'name': '课程管理',
                'codename': 'add_course',
                'url': 'curriculum/course/'
            }, {
                'name': '资源管理',
                'codename': 'add_resources',
                'url': 'curriculum/resources/'
            }]
        }, {
            'name': '考试系统',
            'codename': 'examination',
            'icon': 'el-icon-s-claim',
            'models': [{
                'name': '考试管理',
                'codename': 'add_examinations',
                'url': 'examination/examinations/'
            },
                {
                    'name': '快速添加',
                    'url': 'http://quick.car.com/',
                },
                {
                    'name': '选择题目',
                    'codename': 'add_choice_topic',
                    'url': 'examination/choice_topic'
                }, {
                    'name': '多选题目',
                    'codename': 'add_multiple_choice_topic',
                    'icon': 'fa fa-check-square',
                    'url': 'examination/multiple_choice_topic'
                }, {
                    'name': '判断题目',
                    'codename': 'add_judge_topic',
                    'icon': 'fa fa-check',
                    'url': 'examination/judge_topic'
                }, {
                    'name': '学生成绩',
                    'codename': 'add_results',
                    'icon': 'el-icon-s-data',
                    'url': 'examination/results'
                }]
        }, {
            'name': '题库管理',
            'codename': 'question',
            'icon': 'el-icon-tickets',
            'models': [{
                'name': '选择题',
                'codename': 'add_choice',
                # 'icon':'fa fa-circle',
                'url': 'question/choice',
            }, {
                'name': '多选题',
                'codename': 'add_multiple_choice',
                'icon': 'fa fa-check-square',
                'url': 'question/multiple_choice'
            }, {
                'name': '判断题',
                'codename': 'add_judge',
                'icon': 'fa fa-check',
                'url': 'question/judge'
            }, {
                'name': '题目类型',
                'codename': 'add_questiontype',
                'icon': 'el-icon-reading',
                'url': 'question/questiontype'
            }, {
                'name': '车型管理',
                'codename': 'add_classification',
                'icon': 'fa fa-car',
                'url': 'data/classification'
            }, ]
        }, {
            'name': '竞赛系统',
            'codename': 'contest',
            'models': [
                {
                    'name': '竞赛',
                    'codename': 'add_contestlist',
                    'models': [{
                        'name': '竞赛管理',
                        'codename': 'add_contestlist',
                        'url': 'contest/contestlist'
                    }, {
                        'name': '工位管理',
                        'codename': 'add_station',
                        'url': 'contest/station'
                    }, {
                        'name': '作业项目',
                        'codename': 'add_job',
                        'url': 'contest/job'
                    }]
                },
                {
                    'name': '作业评分',
                    'codename': 'add_job_item',
                    'models': [{
                        'name': '作业小项',
                        'codename': 'add_job_item',
                        'url': 'contest/job_item'
                    }, {
                        'name': '作业分数',
                        'codename': 'add_jobscore',
                        'url': 'contest/jobscore'
                    }, {
                        'name': '作业总分',
                        'codename': 'add_jobtotal',
                        'url': 'contest/jobtotal'
                    }]
                },
                {
                    'name': '作业表',
                    'codename': 'add_record',
                    'models': [{
                        'name': '记录表',
                        'codename': 'add_record',
                        'url': 'contest/record'
                    }, {
                        'name': '行管理',
                        'codename': 'add_row',
                        'url': 'contest/row'
                    }, {
                        'name': '列管理',
                        'codename': 'add_column',
                        'url': 'contest/column'
                    }, {
                        'name': '作答标准',
                        'codename': 'add_criteria',
                        'url': 'contest/criteria'
                    }, {
                        'name': '作答记录',
                        'codename': 'add_tablerecord',
                        'url': 'contest/tablerecord'
                    }, {
                        'name': '表格成绩',
                        'codename': 'add_tablejobscore',
                        'url': 'contest/tablejobscore'
                    }]
                }, {
                    'name': '理论考核',
                    'codename': 'add_choice_job',
                    'models': [{
                        'name': '选择题目',
                        'codename': 'add_choice_job',
                        'url': 'contest/choice_job'
                    }, {
                        'name': '多选题目',
                        'codename': 'add_multiple_job',
                        'url': 'contest/multiple_job'
                    }, {
                        'name': '判断题目',
                        'codename': 'add_judge_job',
                        'url': 'contest/judge_job'
                    }, {
                        'name': '成绩',
                        'codename': 'add__results_job',
                        'url': 'contest/results_job'
                    }, {
                        'name': '答题记录',
                        'codename': 'add_jilu',
                        'models': [{
                            'name': '选择记录',
                            'codename': 'add_choice_res',
                            'url': 'contest/choice_res'
                        }, {
                            'name': '多选记录',
                            'codename': 'add_multiple_res',
                            'url': 'contest/multiple_res'
                        }, {
                            'name': '判断记录',
                            'codename': 'add_judge_res',
                            'url': 'contest/judge_res'
                        }]
                    }]
                }, {
                    'name': '总成绩',
                    'codename': 'add_merge',
                    'url': 'contest/merge'
                }, {
                    'name': '快速添加理论',
                    'codename': 'add_choice_res',
                    'url': 'http://quconchoice.car.com'
                }, {
                    'name': '快速添加表格',
                    'codename': 'add_criteria',
                    'url': 'http://quicktable.car.com'
                }]
        },
        {
            'name': 'APP点位图',
            'codename': 'contest',
            'models': [{
                'name': '设置APP点位图',
                'codename': 'add_app_point_image',
                'url': '/set_point_image'
            }, {
                'name': '设置APP点位数据',
                'codename': 'add_app_point_data',
                'url': '/set_point_data'
            }]
        },
        {
            'name': '用户管理',
            'codename': 'usermanage',
            'models': [{
                'name': '学生管理',
                'codename': 'add_students',
                'icon': 'fa fa-address-card',
                'url': 'usermanage/students'
            }, {
                'name': '教师管理',
                'codename': 'add_teachers',
                'url': 'usermanage/teachers'
            }, {
                'name': '班级管理',
                'codename': 'add_classes',
                'icon': 'fa fa-graduation-cap',
                'url': 'usermanage/classes'
            }, {
                'name': '院系管理',
                'codename': 'add_department',
                'icon': 'el-icon-school',
                'url': 'usermanage/department'
            }]
        }, {
            'name': '电子竞赛',
            'codename': 'electron',
            'models': [{
                'name': '竞赛管理',
                'codename': 'add_elecontest',
                'url': 'electron/elecontest'
            }, {
                'name':'工位管理',
                'codename': 'add_station_ele',
                'url': 'electron/station_ele'
            } ,{
                    'name':'文件记录',
                    'codename': 'add_elerecord',
                    'url': 'electron/elerecord'
                },{
                    'name':'快速添加理论',
                    'codename': 'add_choice_ele',
                    'url': 'http://quickele.car.com'
                },{
                'name': '理论题目',
                'codename': 'add_choice_ele',
                'models': [{
                    'name': '选择题目',
                    'codename': 'add_choice_ele',
                    'url': 'electron/choice_ele'
                }, {
                    'name': '多选题目',
                    'codename': 'add_multiple_ele',
                    'url': 'electron/multiple_ele'
                }, {
                    'name': '判断题目',
                    'codename': 'add_judge_ele',
                    'url': 'electron/judge_ele'
                }]
            }, {
                'name': '答题记录',
                'coedname': 'add_choice_res_ele',
                'models': [{
                    'name': '选择记录',
                    'codename': 'add_chocie_res_ele',
                    'url': 'electron/choice_res_ele'
                }, {
                    'name': '多选记录',
                    'codename': 'add_multiple_res_ele',
                    'url': 'electron/multiple_res_ele'
                }, {
                    'name': '判断记录',
                    'codename': 'add_judge_res_ele',
                    'url': 'electron/judge_res_ele'
                },{
                    'name': '理论成绩',
                    'codename': 'add_results_ele',
                    'url': 'electron/results_ele'
                }]
            }]
        }, {
            'app': 'auth',
            'codename': 'auth',
            'name': '权限认证',
            'icon': 'fas fa-user-shield',
            'models': [{
                'name': '用户',
                'codename': 'add_user',
                'icon': 'fa fa-user',
                'url': 'auth/user/'
            }, {
                'name': '群组',
                'url': 'auth/group/'
            }]
        }
    ]
}
# 设置默认主键字段类型
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# 解决数据库初始化警告
SILENCED_SYSTEM_CHECKS = ['models.W042']

#
# {
#                 'name': '作业小项',
#                 'url': 'contest/job_item'
#             },{
#                 'name': '作业分数',
#                 'url': 'contest/jobscore'
#             },{
#                 'name': '作业总分',
#                 'url': 'contest/jobtotal'
#             },
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/
