import feedparser
from os import path

OUTPUT_DIR = "~/Desktop/temp/"

def grab_feeds(feeds):
    """Array of feeds URLs -> Array of feedparser objects."""
    return [feedparser.parse(feed) for feed in feeds]


def generate_toc(feeds):
    """Array of feedparser objects -> NCX file content."""
    xml = """
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE ncx PUBLIC "-//NISO//DTD ncx 2005-1//EN" "http://www.daisy.org/z3986/2005/ncx-2005-1.dtd">
<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1" xml:lang="en-US">
<head>
<meta name="dtb:uid" content="BookId"/>
<meta name="dtb:depth" content="2"/>
<meta name="dtb:totalPageCount" content="0"/>
<meta name="dtb:maxPageNumber" content="0"/>
</head>
<docTitle><text>DailyKindle</text></docTitle>
<docAuthor><text>Thomas Pelletier</text></docAuthor>
  <navMap>"""
    footer = """
  </navMap>
</ncx>"""

    xml += '<navPoint class="toc" id="toc" playOrder="1">'
    xml += '<navLabel><text>Table of Contents</text></navLabel>'
    xml += '<content src="toc.html"/></navPoint>'


    play_order = 1
    chapter = 1

    for feed in feeds:
        chapter += 1
        play_order += 1

        xml += '<navPoint class="chapter" id="chapter_%s" playOrder="%s">' % (chapter, play_order)
        xml += '<navLabel><text>%s</text></navLabel>' % feed.feed.title
        xml += '<content src="%s.html"/>' % chapter

        section = 0

        for entry in feed.entries:
            play_order += 1
            section += 1
            xml += '<navPoint class="section" id="_%s.%s" playOrder="%s">' % (chapter, section, play_order)
            xml += '<navLabel><text>%s</text></navLabel>' % entry.title
            xml += '<content src="%s.html#id_%s.%s"/>' % (chapter, chapter, section)
            xml += '</navPoint>'

        xml += '</navPoint>'

    return xml + footer

def generate_toc_html(feeds):
    html = """
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head><title>Table of Contents</title></head>
<body>

<div>
 <h1><b>TABLE OF CONTENTS</b></h1>
 <br />"""
    html_footer = """
</body>
</html>"""

    chapter = 1

    for feed in feeds:
        chapter += 1

        html += '<h3><b>%s</b></h3>' % feed.feed.title
        html += '<ul>'

        section = 0

        for entry in feed.entries:
            section += 1

            html += '<li><a href="%s.html#id_%s.%s">%s</a></li>' % (chapter, chapter, section, entry.title)

        html += '</ul>'

    return html + html_footer

def generate_html(feed, chapter):
    html = """
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<title>%s</title>
<link rel="stylesheet" href="KUG.css" type="text/css" />
</head>
<body>
""" % feed.feed.title
    foot = """
</body>
</html>
"""

    html += "<h1>%s</h1>" % feed.feed.title

    section = 0

    for entry in feed.entries:
        section += 1
        html += '<div id="id_%s.%s"><h2>%s</h2>' % (chapter, section, entry.title)
        html += entry.description
        html += '</div>'
        html += '<p class="pagebreak">&nbsp;</p>'

    return html + foot

def generate_opf(feeds):
    opf = """
<?xml version="1.0" encoding="utf-8"?>
<package xmlns="http://www.idpf.org/2007/opf" version="2.0" unique-identifier="BookId">
    <metadata xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:opf="http://www.idpf.org/2007/opf">
        <dc:title>DailyKindle</dc:title>
        <dc:language>en-us</dc:language>
        <dc:creator>DailyKindle</dc:creator>
    </metadata>
    <manifest>
"""

    opf += '<item id="item1" media-type="application/xhtml+xml" href="toc.html"/>'

    item = 1
    for feed in feeds:
        item += 1
        opf += '<item id="item%s" media-type="application/xhtml+xml" href="%s.html"/>"' % (item, item)

    opf += '<item id="toc" media-type="application/x-dtbncx+xml" href="toc.ncx"></item>'

    opf += '</manifest>'

    opf += '<spine toc="toc">'
    item = 1
    for feed in feeds:
        item += 1
        opf += '<itemref idref="item%s"/>' % item
    opf += '</spine>'

    opf += """
<guide>
    <reference type="toc" title="Table of Contents" href="toc.html"></reference>
    <reference type="text" title="Table of Contents" href="toc.html"></reference>
</guide>
"""
    opf += "</package>"
    return opf

def write(filepath, content, relative=True):
    if relative:
        filepath = path.join(OUTPUT_DIR, filepath)
    filepath = path.expanduser(filepath)
    f = open(filepath, "w+")
    f.write(content)
    f.close()

def build(feeds):
    feedso = grab_feeds(feeds)
    write("daily.opf", generate_opf(feedso))
    write("toc.ncx", generate_toc(feedso))
    write("toc.html", generate_toc_html(feedso))

    chapter = 1

    for feed in feedso:
        chapter += 1
        write("%s.html" % chapter, generate_html(feed, chapter))

if __name__ == "__main__":
    f = [
        "http://feeds.feedburner.com/b-list-entries",
        "http://lucumr.pocoo.org/feed.atom",
    ]
    build(f)
