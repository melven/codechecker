#!/usr/bin/env python3
# read the fortitude doc/rules directory and generate checker labels

import argparse
import json
import os
import re


def _get_severity(code: str) -> str:
    """Assign a severity to every code"""

    if code.startswith("S"):
        return "STYLE"
    if code.startswith("E"):
        return "UNSPECIFIED"
    if code.startswith("C"):
        return "MEDIUM"
    if code.startswith("OB"):
        return "HIGH"
    if code.startswith("MOD"):
        return "LOW"
    if code.startswith("PORT"):
        return "MEDIUM"
    return "UNSPECIFIED"


def main():
    """main function, small converter for fortitude doc to checker labels"""
    parser = argparse.ArgumentParser(
            prog="fortitude_checker_labels",
            description="generate config/labels/ruff.json from fortitude/docs/rules")
    parser.add_argument("fortitude_directory")

    args = parser.parse_args()
    rules_path = os.path.join(args.fortitude_directory, "docs", "rules")

    rules_dict = _scan_doc_rules_dir(rules_path)

    print(json.dumps(rules_dict, sort_keys=True, indent=2))
    

def _scan_doc_rules_dir(doc_rules_path: str) -> dict:
    """scan the contents of the fortitide/docs/rules dir and return a dictionary with all rules"""

    title_match = re.compile(".*\((.*)\)")

    labels = dict()
    files = os.listdir(doc_rules_path)
    for file in files:
        name = file.replace(".md", "")
        if file != name + ".md":
            raise RuntimeError("Unexpected filename '%s' in directory '%s'!" %(file, doc_rules_path))

        file_path = os.path.join(doc_rules_path, file)
        with open(file_path, mode="r") as markdown_description:
            first_line = markdown_description.readline().strip("\n")
            code = title_match.match(first_line).group(1)

        severity = _get_severity(code)

        labels[code] = [
                "doc_url:https://fortitude.readthedocs.io/en/stable/rules/"+name,
                "severity:"+_get_severity(code)
                ]

    result = {
            "analyzer": "ruff",
            "labels": labels
            }

    return result


if __name__ == '__main__':
    main()
