from notmuch import Database, Query

    db = Database()
    for message in Query(db,'').search_messages()
