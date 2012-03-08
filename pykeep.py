#! /usr/bin/env python

import os, configparser, config, mysql.backup

# Available backup routines for different sources: mysql, files, ftp etc
backupRoutines = {
    'mysql': mysql.backup.performBackup,
}

if __name__ == '__main__':
    from argparser import parser

    args = parser.parse_args()
    path = config.__USER_CONFIG_PATH__
    configFiles = [os.path.join(path, name) for name in os.listdir(path)
                   if (os.path.isfile(os.path.join(path, name)) and name.endswith('.conf'))]

    if not configFiles:
        print('No config files found in {}. Nothing to do! Exiting.'.format(config.__USER_CONFIG_PATH__))
    else:
        for configFile in configFiles:
            userConfig = configparser.ConfigParser()
            userConfig.read(configFile)

            for section in userConfig.sections():
                try:
                    backupRoutines[section](userConfig[section], args)
                except KeyError:
                    print('Config file contains a section that is not \
                          supported. Ignoring [{}]'.format(section))
