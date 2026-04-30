#from multiprocessing import process
import sys
import argparse
#import multiprocessing
import time
#import schedule

# for mcstatus
from mcstatus import JavaServer

#for notifications
from plyer import notification

#for app
import tkinter as tk
#test

def answer():
    #entry test
    hidden_label.config(text="")

    if entry.get():
     hidden_label.config(text="You entered: " + entry.get())
     entry.delete(0, tk.END)





global switch
switch = False
def switch_text():
    #insert test
    entry.insert(tk.END, "test")
    
    #switch test
    global switch
    switch == False
    if switch == False:
        label.config(text="goodbye world")
        switch = True
    else:
        label.config(text="hello world")
        switch = False

#dhost = 'Skorpion7731-APa5.aternos.me'
dhost = 'ujjocigon.aternos.me:50604'
#dhost = 'fundan1000000.aternos.me'
dretries = 4
ddelay = 0.3
dtimeout = 2.0

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
parser.add_argument('--testapp', type=int, default=0, help='test app')
args = parser.parse_args()

host = args.host    

if args.testapp == 2:
    app2 = tk.Tk()
    #grid test
    app2.title("test grid")
    app2.geometry("500x350")

    frame = tk.Frame(app2)
    frame.pack(pady=20)

    button = tk.Button(frame, text="hello", font=("Arial", 16))
    button.grid(row=1, column=0)
    button = tk.Button(frame, text="answer", font=("Arial", 16))
    button.grid(row=1, column=1, padx=10)
    button = tk.Button(frame, text="switch text", font=("Arial", 16))
    button.grid(row=1, column=2)
    button = tk.Button(frame, text="hello", font=("Arial", 16))
    button.grid(row=2, column=0)
    button = tk.Button(frame, text="answer", font=("Arial", 16))
    button.grid(row=2, column=1)
    button = tk.Button(frame, text="switch text", font=("Arial", 16))
    button.grid(row=2, column=2)
    button = tk.Button(frame, text="aaaaa", font=("Arial", 16))
    button.grid(row=3, column=0, columnspan=3, sticky="ew")

    button = tk.Button(app2,text="Exit",command=app2.destroy)
    button.place(relx=0, rely=0)

    app2.mainloop()

if args.testapp == 1:
    app = tk.Tk()
    #pack test
    app.title("test pack")
    app.geometry("500x350")

    label = tk.Label(app, text="test: hello world", font=("Arial", 20))
    label.pack(pady=20)

    entry = tk.Entry(app, width=30, font=("Arial", 17))
    entry.pack(pady=10)

    button = tk.Button(app, text="switch text", font=("Arial", 16), command=switch_text)
    button.pack(pady=10)
    button = tk.Button(app, text="answer", font=("Arial", 16), command=answer)
    button.pack(pady=10, fill=tk.X, padx=20)

    hidden_label = tk.Label(app, text="", font=("Arial", 20))
    hidden_label.pack(pady=20)

    app.mainloop()
    #test end

def extract_motd_text(protocol_status):
    try:
        motd = getattr(protocol_status, 'motd', None)
        if motd is not None:
            if args.verbose:
                safe_print(f'MOTD object: {motd}, type: {type(motd)}')
            raw = getattr(motd, 'raw', None)
            if isinstance(raw, dict) and 'text' in raw:
                return raw.get('text', '')
            return str(raw)
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
    #query = None
    for i in range(max(1, args.retries)):
        try:
            if args.verbose:
                safe_print(f'[debug] attempt {i+1}/{args.retries}: looking up {host}')
            server = JavaServer.lookup(host)
            # set timeout on the server object if supported by mcstatus
            setattr(server, 'timeout', float(args.timeout))
            connection = server.ping()
            print('ping:', connection)
            status = server.status()
            if args.verbose:
                safe_print(f'[debug] status received on attempt {i+1} for server {server}')
            return status, connection

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

global motd_text
motd_text = None

#stop = False
def main():
    try:
        stop = False
        while stop == False:
            motd_text = None
            if JavaServer is None:
                safe_print('<mcstatus not installed>')
                sys.exit(1)

            status, connection = check_server_status()
            if args.testapp == 3:
                    label2.config(text=f'ping: {connection}')

            if args.verbose:
                print('[debug] final status:', status)
            
            if status is None:
                # check for case when status is none but no error occurred
                error_msg = 'OSError: Server did not respond with any information! loading or offline'
                safe_print(error_msg)
                #motd_text = error_msg
                #global motd_text
                motd_text = 'Server did not respond with any information! loading or offline'
                if args.testapp == 3:
                    label.config(text=motd_text)
            
            if motd_text is None:
                
                motd_text = extract_motd_text(status)
                safe_print(motd_text or 'none')
                if args.testapp == 3:
                    label.config(text=motd_text)
            # Show popup if we got a MOTD and it's not the error message
            if 'Server did not respond with any information!' in motd_text or  'server is offline' in motd_text:
                print('e')
                
            else:
                try:
                    notification.notify(
                    title="Hello!",
                    message=motd_text,
                    timeout=5  # seconds
                    )
                    break
                    #this is the popup code which we are not useing anymore as we have replaced it with notifications
                    ("""
                    root = tk.Tk()
                    root.withdraw()  # Hide the main window
                    messagebox.showinfo('Minecraft Server MOTD', motd_text)
                    root.destroy()
                    """)
                except Exception as e:
                    safe_print(f'[popup error] {e}')
            time.sleep(5)
            print('checking again...')
        print('done')            
    except Exception as e:
        print('ah')            


if __name__ == '__main__':    
    main()

