from os import environ
SESSION_CONFIG_DEFAULTS = dict(real_world_currency_per_point=1.0, participation_fee=0.0)
SESSION_CONFIGS = [dict(name='hiring_funnel_demo', num_demo_participants=1, app_sequence=['hiring_funnel'])]
LANGUAGE_CODE = 'en'
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = False
DEMO_PAGE_INTRO_HTML = ''
PARTICIPANT_FIELDS = ['condition', 'practice_data_json', 'main_data_json', 'history_json', 'selected_round', 'selected_candidate', 'selected_true_quality', 'selected_reward_string', 'weight_resume', 'weight_zoom', 'weight_inperson', 'gender', 'age', 'education']
SESSION_FIELDS = []
THOUSAND_SEPARATOR = ''
ROOMS = []

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

SECRET_KEY = 'blahblah'

# if an app is included in SESSION_CONFIGS, you don't need to list it here
INSTALLED_APPS = ['otree']


