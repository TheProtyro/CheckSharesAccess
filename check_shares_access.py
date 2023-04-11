import csv
import smbclient
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--csv', type=str, required=True, help='The CSV file with the format "hostname.domain.local,share"')
parser.add_argument('--username', type=str, required=True, help='The domain username')
parser.add_argument('--password', type=str, required=True, help='The domain password')
parser.add_argument('--domain', type=str, required=True, help='The domain name')

args = parser.parse_args()

# ANSI escape sequence for green text
GREEN = '\033[32m'
# ANSI escape sequence for red text
RED = '\033[31m'
# ANSI escape sequence to reset color to default
RESET = '\033[0m'

with open(args.csv, newline='') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        hostname = row[0]
        share = row[1]

        with smbclient.SambaClient(server=hostname, share=share, username='{}\\{}'.format(args.domain, args.username), password=args.password) as client:
            try:
                file_list = client.listdir('.')
                print('{}Access to share {} on {} : OK{}'.format(GREEN, share, hostname, RESET))
            except smbclient.SambaClientError:
                print('{}Access to share {} on {} : Authentication failure{}'.format(RED, share, hostname, RESET))
