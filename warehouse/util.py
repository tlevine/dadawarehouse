import datetime, os

def i_should_copy(local_filename):
    if not os.path.exists(local_filename):
        return True

    mtime = datetime.datetime.fromtimestamp(os.stat(local_filename).st_mtime)
    a_day_ago = datetime.datetime.now() - datetime.timedelta(days = 1)
    return mtime < a_day_ago
