# DailyKindle

DailyKindle is a Python scripts which, given a set of RSS/Atom feeds URLs,
creates a MOBI file that you can directly use on you Amazon Kindle (or any other
device that supports MOBI documents).

## Requirements

* A working Python 3 environment (tested on OS X + Python 3.2 + Virtualenv).
* [Amazon's KindleGen](http://www.amazon.com/gp/feature.html?docId=1000234621)
  binary.

## Installation

1. Grab the script code. Choose one of the following:
   * [https://bitbucket.org/pelletier/dailykindle/get/tip.zip](https://bitbucket.org/pelletier/dailykindle/get/tip.zip)
   * [https://github.com/pelletier/dailykindle/zipball/master](https://github.com/pelletier/dailykindle/zipball/master)
   * `hg clone https://bitbucket.org/pelletier/dailykindle`
   * `git clone git://github.com/pelletier/dailykindle.git`
2. (optional) Source your virtualenv.
3. `pip install -r requirements.txt`

## Usage

    DailyKindle usage:
    python dailykindle.py <output dir> <day|week> <kindle_gen> <feed_url_1>
    [<feed_url_2> ...]

Passing `day` will only keep posts younger than one day; `week` for one week.

This will create a `daily.mobi` in `<output dir>`. You can now transfer this
file to your device.

## Example

    python dailykindle.py ~/Desktop/temp/ day \
    "~/Downloads/KindleGen_Mac_i386_v1.2/kindleGen" \
    "http://feeds.feedburner.com/b-list-entries" \
    "http://lucumr.pocoo.org/feed.atom"

## License

Have fun.
