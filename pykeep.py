#! /usr/bin/env python

import os, glob, configparser, shlex
import subprocess as subp
from datetime import datetime

def backupMysql(config = None):
    ''' Performs a MySQL backup using mysqldump tool 
        and a specific config file 
    '''

    print('o Performing MySQL Backup...')
    print('\t=> Checking for the mysqldump tool...')

    try:
        with open(os.devnull, 'w') as devnull:
            if subp.call(['which', 'mysqldump'], stdout = devnull, stderr = devnull) == 1:
                print('\t=> mysqldump NOT found. Aborting.')
                return
    except Exception as ex:
        print('\t=> An exception occured. Unable to use "which"')
        print(ex)
        return
    
    print('\t=> mysqldump found. Proceeding with backup...')
    print('\t\t[Backup Path is \'{}\']'.format(config['path']))

    for i, database in enumerate(config['databases'].split(), start = 1):
        print('\t\t* Backing up database {db} ({i}/{total})'.format(db = database, i = i, 
                                                                    total = len(config['databases'].split())), end = ' ')

        filename = '{}_{}.sql'.format(database, datetime.now().strftime('%d-%m-%Y_%H:%M:%S:%f'))

        if not args.dryRun:
            with open(os.path.join(config['path'], filename), 'w') as backupFile:
                command = 'mysqldump -h {host} -u {user} -p{password} --databases {database}'.format(
                    host = config['host'], user = config['usernames'].split()[i - 1],
                    password = config['passwords'].split()[i - 1], database = database)

                subp.call(shlex.split(command), stdout = backupFile)

    print('\t=> MySQL Backup Finished.')

# Available backup routines for different sources: mysql, files, ftp etc
backupRoutines = {
    'mysql': backupMysql,
}

# Finds the path to configuration files
if os.path.isabs(__file__):
    configPath = os.path.join(path, 'configs')
else:
    configPath = os.path.join(os.path.dirname(os.path.join(os.getcwd(), __file__)), 'configs')

if __name__ == '__main__':
    # Sets up the argument parser
    import argparse
    
    parser = argparse.ArgumentParser(description = 'Tool for automating MySQL and FTP backups')
    parser.add_argument('--dry-run', '-d', dest = 'dryRun', nargs = '?', const = True, default = False, \
                        help = 'Runs the script in dry run mode, when no connections, file manipulations etc. are performed')

    args = parser.parse_args()

    for configFile in glob.iglob(configPath +  '/*'):
        config = configparser.ConfigParser()
        config.read(configFile)
        
        for section in config.sections():
            backupRoutines[section](config[section])

