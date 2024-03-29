import os
import sqlite3
import subprocess

def read_regex_file(file_path):
    """
    Read regex filters from a file.
    """
    if not os.path.isfile(file_path):
        print(f'Error: File not found: {file_path}')
        return []

    with open(file_path, 'r') as file:
        return [line.strip() for line in file.readlines() if line.strip() and not line.startswith("#")]

def add_regex_filters(regex_filters):
    """
    Add regex filters to Pi-hole.
    """
    path_pihole = '/etc/pihole'
    path_pihole_db = os.path.join(path_pihole, 'gravity.db')
    cmd_restart = ['pihole', 'restartdns', 'reload']

    if not os.path.exists(path_pihole_db):
        print('Error: Pi-hole gravity database not found.')
        return

    try:
        conn = sqlite3.connect(path_pihole_db)
        c = conn.cursor()
    except sqlite3.Error as e:
        print(f'Error: Unable to connect to the Pi-hole database: {e}')
        return

    try:
        # Insert regex filters into the database
        c.executemany("INSERT INTO domainlist (type, domain, enabled) VALUES (3, ?, 1)", [(filter,) for filter in regex_filters])
        conn.commit()
        print(f'Successfully added {len(regex_filters)} regex filters to Pi-hole.')
    except sqlite3.Error as e:
        print(f'Error: Unable to add regex filters to Pi-hole: {e}')

    conn.close()

    # Restart Pi-hole DNS
    print('Restarting Pi-hole DNS...')
    subprocess.run(cmd_restart)

def main():
    # Read regex filters from the regex.list file in the same directory
    regex_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'regex.list')
    regex_filters = read_regex_file(regex_file_path)

    if regex_filters:
        add_regex_filters(regex_filters)
    else:
        print('No regex filters found in the regex.list file.')

if __name__ == "__main__":
    main()
