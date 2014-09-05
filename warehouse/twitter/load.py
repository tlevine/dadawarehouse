NOTMUCH = ['notmuch', 'show', '--format=json', 'from:twitter.com']
TMP = '/tmp/twitter'

def emails():
    if os.path.isfile(TMP):
        fp = open(TMP)
    else:
        raise NotImplementedError
        notmuch = subprocess.Popen(RSYNC)
        notmuch.wait()

    result = json.load(fp)
    fp.close()
    return result

def update(session):
    emails()
