#! /usr/bin/env python

import os, glob, configparser, shlex
import subprocess as subp

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
    
    with open(os.path.join(config['path'], config['backup_name']), 'w') as backupFile:
        subp.call(shlex.split('mysqldump -h {host} -u {username} -p{password} --databases {databases}'.format(**config)), stdout = backupFile)
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

