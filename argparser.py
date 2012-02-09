import argparse

parser = argparse.ArgumentParser(description = 'Tool for automating MySQL and FTP backups')

parser.add_argument('--dry-run', '-d', dest = 'dryRun', nargs = '?', const = True, default = False, \
                    help = 'Runs the script in dry run mode, when no connections, file manipulations etc. are performed')
