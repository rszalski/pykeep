#! /usr/bin/env python

import os, configparser, config, mysql.backup

# Available backup routines for different sources: mysql, files, ftp etc
backupRoutines = {
    'mysql': mysql.backup.performBackup,
}

if __name__ == '__main__':
    from argparser import parser

    args = parser.parse_args()
    configFiles = [name for name in os.listdir(config.__USER_CONFIG_PATH__) if os.path.isfile(os.path.join(config.__USER_CONFIG_PATH__, name))]

    if not configFiles:
        print('No config files found in {}. Nothing to do! Exiting.'.format(config.__USER_CONFIG_PATH__))
    else:
        for configFile in configFiles:
            userConfig = configparser.ConfigParser()
            userConfig.read(os.path.join(config.__USER_CONFIG_PATH__, configFile))

            for section in userConfig.sections():
                backupRoutines[section](userConfig[section], args)

