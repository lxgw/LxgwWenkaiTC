import plistlib
import argparse
import os
import re
import datetime
from zoneinfo import ZoneInfo

argparser = argparse.ArgumentParser()
argparser.add_argument("file", type=str, help="fontinfo.plist file path")
argparser.add_argument("--version", "-v", type=str, help="version number, in vX.XXX format")
argparser.add_argument("--date", "-d", type=str, help="date, default to current date in GMT+8", default=datetime.datetime.now(ZoneInfo("Asia/Shanghai")).strftime("%B %d, %Y"))

args = argparser.parse_args()

parser = re.compile(r"v?((?P<major>\d+)\.(?P<minor>\d+).*)")
match = parser.match(args.version)
major_version_num = int(match.group("major"))
minor_version_num = int(match.group("minor"))
version_num_string = f"Version {match.group(1)}"

if args.date.strip() == "":
    args.date = datetime.datetime.now(ZoneInfo("Asia/Shanghai")).strftime("%B %d, %Y")
version_string = f"{version_num_string}; {args.date}"

assert os.path.isfile(args.file), "File not found"

fontinfo = plistlib.load(open(args.file, "rb"))

fontinfo["openTypeNameUniqueID"] = (
    fontinfo["openTypeNameUniqueID"].split(":")[0] + ":" + version_num_string
)
fontinfo["openTypeNameVersion"] = version_string
fontinfo["versionMajor"] = major_version_num
fontinfo["versionMinor"] = minor_version_num

plistlib.dump(fontinfo, open(args.file, "wb"))

print("SUCCESS: Updated version in %s" % args.file)