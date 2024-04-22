#!/usr/bin/python3
import argparse
from idstools import rule
from datetime import date
import tldextract
from os import makedirs
from pprint import pprint

description = (
    "Given a file containing a list of Suricata rules, extract any blocked domains."
)

parser = argparse.ArgumentParser(description=description)

parser.add_argument(
    "--rules",
    required=True,
    help="The name of the file containing a list of Suricata rules, one rule per line.",
)
args = parser.parse_args()

rules_in_file = open(args.rules, "r")

categories = {
    "MALICIOUS": {
        "description": "Blocks malware, phishing, coin miners, PUPs, exploits, etc.",
        "utility": "High - useful at home and in corporate environments",
        "count": 0,
        "tags": [
            "ET TROJAN",
            "ET MALWARE",
            "ET MOBILE_MALWARE",
            "ET CURRENT_EVENTS",
            "ET PHISHING",
            "ET ATTACK_RESPONSE",
            "ET ADWARE_PUP",
            "ET EXPLOIT_KIT",
            "ET WEB_CLIENT",
            "ET WEB_SERVER",
            "ET COINMINER",
        ],
    },
    "SUSPICIOUS": {
        "description": "Blocks link shorteners, pastebin services, games, etc.",
        "utility": "Moderate - useful in strict corporate environments, maybe not at home",
        "count": 0,
        "tags": [
            "ET INFO DYNAMIC_DNS",
            "ET POLICY",
            "ET GAMES",
            "ET DNS",
        ],
    },
    "INFORMATIONAL": {
        "description": "Blocks more link shorteners, benign callbacks, and some potentially unwanted sites (ex. file sharing), etc.",
        "utility": "Low - may be useful in certain strict corporate environments",
        "count": 0,
        "tags": ["ET INFO", "ET HUNTING"],
    },
}

makedirs("output/", exist_ok=True)
malicious_file = open("output/malicious.txt", "w")
suspicious_file = open("output/suspicious.txt", "w")
informational_file = open("output/informational.txt", "w")


def write_by_category(category, write_this):
    if category == "MALICIOUS":
        malicious_file.write(f"{write_this}\n")
    if category == "SUSPICIOUS":
        suspicious_file.write(f"{write_this}\n")
    if category == "INFORMATIONAL":
        informational_file.write(f"{write_this}\n")


header = """# (Unofficial) Emerging Threats PiHole blocklist
#
# Category: {}
# Description: {}
# Utility: {}
# Status: Beta / in development
# Last modified: {}
# Blocklist generated 
"""

for category_name, category_content in categories.items():
    write_by_category(
        category_name,
        header.format(
            category_name,
            category_content["description"],
            category_content["utility"],
            date.today(),
        ),
    )

for line in rules_in_file:
    input_rule = line.strip()

    # skip empty lines
    if input_rule == "":
        continue

    # skip commented lines
    if input_rule[0] == "#":
        continue

    # parse each rule individually
    parsed_rule = rule.parse(input_rule)

    # skip non-DNS rules
    if not "dns.query" in parsed_rule.keys() and not "dns_query" in parsed_rule.keys():
        continue

    # domain components are not suitable for DNSBL
    may_be_component_of_domain = True
    if "endswith" in parsed_rule.keys():
        may_be_component_of_domain = False
    if "isdataat" in parsed_rule.keys():
        if parsed_rule["isdataat"] == "!1,relative":
            may_be_component_of_domain = False

    if may_be_component_of_domain:
        continue

    # regex may not be possible in DNSBL
    if "pcre" in parsed_rule.keys():
        continue

    # skip rules which except some subdomains
    # TODO: do something to handle rules which have exceptions
    mixed_allow_and_deny = False
    for option in parsed_rule.options:
        if option["name"] == "content":
            if option["value"].startswith('!"'):
                mixed_allow_and_deny = True

    if mixed_allow_and_deny:
        continue

    clean_domain = parsed_rule.content.strip('."')
    parsed_domain = tldextract.extract(clean_domain)

    # skip any suspicious TLDs as those are unsuitable for DNSBL
    if parsed_domain.domain == "" or parsed_domain.suffix == "":
        continue

    message = parsed_rule.msg

    category = ""
    for category_name, category_content in categories.items():
        for category_tag in category_content["tags"]:
            if category_tag in message and not category:
                category = category_name
                categories[category_name]["count"] += 1

    if not category:
        print(f"Couldn't categorize message: {message}")

    write_by_category(category, f"0.0.0.0\t{clean_domain}")

if categories["MALICIOUS"]["count"] < 1500:
    print("There are too few MALICIOUS domains -- is the input file correct?")
    exit(1)
