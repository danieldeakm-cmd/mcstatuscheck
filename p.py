import sys
import argparse
import time

# For popup
import tkinter as tk
from tkinter import messagebox

try:
    from mcstatus import JavaServer
except Exception:
    JavaServer = None


def extract_motd_text(protocol_status):
    try:
        if protocol_status is None:
            return ''
        motd = getattr(protocol_status, 'motd', None)
        if motd is not None:
            raw = getattr(motd, 'raw', None)
            if isinstance(raw, dict) and 'text' in raw:
                return raw.get('text', '')
            return str(motd)
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


def main():

    parser = argparse.ArgumentParser(description="Print the server MOTD (no filtering)")
    parser.add_argument('host', nargs='?', default='fundan1000000.aternos.me' , help='minecraft server host')
    parser.add_argument('--retries', type=int, default=5, help='Number of status attempts (default: 5)')
    parser.add_argument('--delay', type=float, default=0.5, help='Delay between attempts in seconds')
    parser.add_argument('--timeout', type=float, default=3.0, help='Network timeout for status attempts in seconds')
    parser.add_argument('--verbose', '-v', action='store_true', help='Show debug info')
    args = parser.parse_args()

    host = args.host
    #if JavaServer is None:
    #    safe_print('<mcstatus not installed>')
    #    sys.exit(1)

    last_exception = None
    status = None
    server = None
    for i in range(max(1, args.retries)):
        try:
            if args.verbose:
                safe_print(f'[debug] attempt {i+1}/{args.retries}: looking up {host}')
            try:    
                server = JavaServer.lookup(host)
            except ConnectionRefusedError as ce:
                print('connection refused error, probably server loading')
                pass  
            # set timeout on the server object if supported by mcstatus
        
            setattr(server, 'timeout', float(args.timeout))
            
            status = server.status()

            if args.verbose:
                safe_print('[debug] status received')
            break
        except Exception as e:
            last_exception = e
            if args.verbose:
                safe_print(f'[debug] attempt {i+1} failed: {e}')
            if i + 1 < args.retries:
                time.sleep(args.delay)


    if status is None:
        # final fallback: print exception text
        popup_msg = ''
        if last_exception is not None:
            error_msg = f'[error] {type(last_exception).__name__}: {last_exception}'
            safe_print(error_msg)
            popup_msg = error_msg
        else:
            error_msg = 'OSError: Server did not respond with any information!'
            safe_print(error_msg)
        # Only show popup if the message does NOT contain 'Server did not respond with any information!'
        if 'Server did not respond with any information!' not in popup_msg:
            try:
                root = tk.Tk()
                root.withdraw()
                messagebox.showerror('Minecraft Server Error', popup_msg)
                root.destroy()
            except Exception as e:
                safe_print(f'[popup error] {e}')
        sys.exit(1)

    motd_text = extract_motd_text(status)
    safe_print(motd_text or '<none>')

    # Show popup if we got a MOTD and it's not the error message
    if motd_text and 'Server did not respond with any information!' not in motd_text:
        try:
            root = tk.Tk()
            root.withdraw()  # Hide the main window
            messagebox.showinfo('Minecraft Server MOTD', motd_text)
            root.destroy()
        except Exception as e:
            safe_print(f'[popup error] {e}')



if __name__ == '__main__':
    main()
