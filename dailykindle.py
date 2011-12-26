from datetime import date, timedelta
from shutil import copy
from os import path, listdir
import feedparser
from jinja2 import Environment, PackageLoader

templates_env = Environment(loader=PackageLoader('dailykindle', 'templates'))
ROOT = path.dirname(path.abspath(__file__))


def build(feeds_urls, output_dir, max_old=None):
    """
    Given a list of feeds URLs and the path of a directory, writes the necessary
    for building a MOBI document.

    max_old must be either None or a timedelta. It defines the maximum age of
    posts which should be considered.
    """

    # Convert max_old if needed.
    if max_old == None:
        max_old = timedelta.max

    # Give the feeds URLs to Feedparser to have nicely usable feed objects.
    feeds = [feedparser.parse(feed_url) for feed_url in feeds_urls]

    # Parse the feeds and grave useful information to build a structure
    # which will be passed to the templates.
    data = []

    ## Initialize some counters for the TOC IDs.
    ## We start counting at 2 because 1 is the TOC itself.
    feed_number = 1
    play_order = 1

    for feed in feeds:
        feed_number += 1
        play_order += 1
        local = {
            'number': feed_number,
            'play_order': play_order,
            'entries': [],
            'title': feed.feed.title,
        }

        entry_number = 0
        for entry in feed.entries:

            # We don't want old posts, just fresh news.
            if date.today() - date(*entry.date_parsed[0:3]) > max_old:
                continue

            play_order += 1
            entry_number += 1

            local_entry = {
                'number': entry_number,
                'play_order': play_order,
                'title': entry.title,
                'description': entry.description,
            }

            local['entries'].append(local_entry)

        data.append(local)

    # Wrap data and today's date in a dict to use the magic of **.
    wrap = {
        'date': date.today().isoformat(),
        'feeds': data,
    }

    # Render and output templates

    ## TOC (NCX)
    render_and_write('toc.xml', wrap, 'toc.ncx', output_dir)
    ## TOC (HTML)
    render_and_write('toc.html', wrap, 'toc.html', output_dir)
    ## OPF
    render_and_write('opf.xml', wrap, 'daily.opf', output_dir)
    ## Content
    for feed in data:
        render_and_write('feed.html', feed, '%s.html' % feed['number'], output_dir)

    # Copy the assets
    for name in listdir(path.join(ROOT, 'assets')):
        copy(path.join(ROOT, 'assets', name), path.join(output_dir, name))
    # copytree(path.join(ROOT, 'assets'), output_dir)


def render_and_write(template_name, context, output_name, output_dir):
    """Render `template_name` with `context` and write the result in the file
    `output_dir`/`output_name`."""

    template = templates_env.get_template(template_name)
    f = open(path.join(output_dir, output_name), "w")
    f.write(template.render(**context))
    f.close()


if __name__ == "__main__":
    from sys import argv, exit

    def usage():
        print("""DailyKindle usage:
python dailykindle.py <output dir> <day|week> <feed_url_1> [<feed_url_2> ...]""")

    if not len(argv) > 3:
        usage()
        exit(64)

    length = None
    if argv[2] == 'day':
        length = timedelta(1)
    elif argv[2] == 'week':
        length = timedelta(7)

    print("Running DailyKindle...")
    build(argv[3:], argv[1], length)
    print("Done")
