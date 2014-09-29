import os
from concurrent.futures import ThreadPoolExecutor

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .pal.load import update as pal
from .history.load import update as history
from .gnucash.load import update as gnucash
from .facebookchat.load import update as fb
from .notmuch.load import update as notmuch
from .twitter.load import update as twitter
from .branchable.load import update as branchable
from .piwik.load import update as piwik
from .muttalias.load import update as mutt

def load(engine):
    sm = sessionmaker(bind=engine)

    notmuch(sm()) # This one crashes on `notmuch new`.

    # Import separate data marts in parallel.
    with ThreadPoolExecutor(max_workers = 8) as e:
        # Minutely updates
        e.submit(history, sm())
        e.submit(notmuch, sm()) # This one crashes on `notmuch new`.
        e.submit(piwik, sm())

        # Daily updates
        e.submit(fb, sm())

        # This involves downloading a biggish file.
    #   e.submit(branchable, sm())

        # These delete existing state and thus take a while.
        # Also, the data aren't updated that often.
        # So we put them last.
        e.submit(twitter, sm())
        e.submit(pal, sm())
        e.submit(gnucash, sm())
        e.submit(mutt, sm())
