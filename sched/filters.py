from jinja2 import Markup, evalcontextfilter, escape


def init_app(app):
    app.jinja_env.filters['date'] = do_date
    app.jinja_env.filters['datetime'] = do_datetime
    app.jinja_env.filters['duration'] = do_duration

    # The nl2br filter uses the Jinja environment's context to determine
    # whether to autoescape
    app.jinja_env.filters['nl2br'] = evalcontextfilter(do_nl2br)


def do_datetime(dt, format=None):
    if dt is None:
        # By default, render an empty string.
        return ''
    if format is None:
        # No format is given in the template call. Use a default format.
        #
        # Format time in its own strftime call in order to:
        # 1. Left-strip leading 0 in hour display.
        # 2. Use 'am' and 'pm' (lower case) instead of 'AM' and 'PM'.
        formatted_date = dt.strftime('%Y-%m-%d - %A')
        formatted_time = dt.strftime('%I:%M%p').lstrip('0').lower()
        formatted = '%s at %s' % (formatted_date, formatted_time)
    else:
        formatted = dt.strftime(format)
    return formatted


def do_date(dt, format='%Y-%m-%d - %A'):
    if dt is None:
        return ''
    # Only difference with do_datetime is the default format, but that is
    # convenient enough to warrant its own template filter.
    return dt.strftime(format)


def do_duration(seconds):
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    d, h = divmod(h, 24)
    tokens = []
    tokens.append(one_many(d, '{d} day'))
    tokens.append(one_many(h, '{h} hour'))
    tokens.append(one_many(m, '{d} minute'))
    tokens.append(one_many(s, '{d} second'))
    template = ', '.join(tokens)

    return template.format(d=d, h=h, m=m, s=s)


def one_many(number, str_duration):
    return str_duration if number > 1 else str_duration + 's'


def do_nl2br(context, value):
    formatted = u'<br />'.join(escape(value).split('\n'))
    if context.autoescape:
        formatted = Markup(formatted)
    return formatted
