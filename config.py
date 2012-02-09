import os

'''
    Contains module-wide configuration settings
'''

# This is the place that every user will store configuration files at
__USER_CONFIG_PATH__ =  os.path.join(os.path.expanduser('~'), '.pykeep')
