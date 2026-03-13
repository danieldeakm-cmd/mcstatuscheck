import sys
import argparse
import time

# For popup
import tkinter as tk
from tkinter import messagebox
from mcstatus import JavaServer

test = messagebox.askyesnocancel('arguments set','here')
print(test)

dhost = 'fundan1000000.aternos.me'
dretries = 5
ddelay = 0.5
dtimeout = 3.0

#dparser = argparse.ArgumentParser(description="defaults set")
#dparser.add_argument('dhost', nargs='?', default='fundan1000000.aternos.me' , help='default minecraft server host')
#dparser.add_argument('--dretries', type=int, default=5, help='default Number of status attempts (default: 5)')
#dparser.add_argument('--ddelay', type=float, default=0.5, help='default Delay between attempts in seconds')
#dparser.add_argument('--dtimeout', type=float, default=3.0, help='default Network timeout for status attempts in seconds')
#dargs = dparser.parse_args()



parser = argparse.ArgumentParser(description="Print the server MOTD (no filtering)")
parser.add_argument('host', nargs='?', default=dhost , help='minecraft server host')
parser.add_argument('--retries', type=int, default=dretries, help='Number of status attempts (default: 5)')
parser.add_argument('--delay', type=float, default=ddelay, help='Delay between attempts in seconds')
parser.add_argument('--timeout', type=float, default=dtimeout, help='Network timeout for status attempts in seconds')
parser.add_argument('--verbose', '-v', action='store_true', help='Show debug info')
args = parser.parse_args()

host = args.host    


def extract_motd_text(protocol_status):
    try:
        motd = getattr(protocol_status, 'motd', None)
        if motd is not None:
            if args.verbose:
                safe_print(f'MOTD object: {motd}, type: {type(motd)}')
                safe_print(f'MOTD object: {motd.json}, type: {type(motd)}')
            raw = getattr(motd, 'raw', None)
            if isinstance(raw, dict) and 'text' in raw:
                return raw.get('text', '')
            return str(motd)
        else:
             if args.verbose:
                safe_print(f'[debug] motd NONE!!!???: {getattr(motd, "raw", None)}')

        raw_all = getattr(protocol_status, 'raw', None)
        if isinstance(raw_all, dict):
            desc = raw_all.get('description', {})
            if isinstance(desc, dict) and 'text' in desc:
                return desc.get('text', '')
    except Exception:
        return ''
    return ''


def safe_print(s):
    try:
        print(s)
    except Exception:
        enc = getattr(sys.stdout, 'encoding', None) or 'utf-8'
        try:
            print(s.encode(enc, errors='replace').decode(enc, errors='replace'))
        except Exception:
            print(s.encode('utf-8', errors='replace').decode('utf-8', errors='replace'))


def check_server_status():
    status = None
    server = None
    query = None
    for i in range(max(1, args.retries)):
        try:
            if args.verbose:
                safe_print(f'[debug] attempt {i+1}/{args.retries}: looking up {host}')
            server = JavaServer.lookup(host)
            # set timeout on the server object if supported by mcstatus
            setattr(server, 'timeout', float(args.timeout))
            status = server.status()
            if args.verbose:
                safe_print(f'[debug] status received on attempt {i+1} for server {server}')
            return status

        except ConnectionRefusedError as ce:
            print('connection refused error, probably server loading')
            pass
        except Exception as e:
            last_exception = e
            if args.verbose:
                    safe_print(f'[debug] attempt {i+1} failed: {e}')
            if i + 1 < args.retries:
                time.sleep(args.delay) 
            else:
                error_msg = f'[error] {type(last_exception).__name__}: {last_exception}'
                safe_print(error_msg)                                              

def main():
    if JavaServer is None:
        safe_print('<mcstatus not installed>')
        sys.exit(1)

    status = check_server_status()
    if args.verbose:
        print('[debug] final status:', status)

    if status is None:
        # check for case when status is none but no error occurred
        error_msg = 'OSError: Server did not respond with any information! loading or offline'
        safe_print(error_msg)
        sys.exit(0)
       

    motd_text = extract_motd_text(status)
    safe_print(motd_text or '<none>')

    # Show popup if we got a MOTD and it's not the error message
    if motd_text and 'Server did not respond with any information!' in motd_text or  'server is offline' in motd_text:
        sys.exit(0)
    else:
        try:
            root = tk.Tk()
            root.withdraw()  # Hide the main window
            messagebox.showinfo('Minecraft Server MOTD', motd_text)
            root.destroy()
        except Exception as e:
            safe_print(f'[popup error] {e}')

if __name__ == '__main__':
    main()
