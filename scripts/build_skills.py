#!/usr/bin/env python3
"""Validate every skill in this repo and build one upload-ready ZIP per skill.

A skill is any top-level folder that contains a SKILL.md file.

Each skill is checked against:
  * the Agent Skills specification (https://agentskills.io/specification)
  * the ZIP rules NetSuite's Ask Oracle shows when an upload is rejected

Usage:
  python3 scripts/build_skills.py            # validate, then build dist/<skill>.zip
  python3 scripts/build_skills.py --check    # validate only (used on pull requests)

The script uses only the Python standard library, and exits non-zero if any check fails.
"""

import argparse
import os
import re
import sys
import zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIST = os.path.join(ROOT, "dist")

# Agent Skills spec
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")  # lowercase, digits, single hyphens
MAX_NAME = 64
MAX_DESCRIPTION = 1024
MAX_COMPATIBILITY = 500
MAX_SKILL_LINES = 500  # the spec recommends keeping SKILL.md under 500 lines (warning only)

# Ask Oracle upload rules (as shown in its "File content not valid" message)
MAX_ZIP_BYTES = 10 * 1024 * 1024
MAX_EXTRACTED_BYTES = 50 * 1024 * 1024
MAX_ENTRIES = 100  # files and folders
MAX_SKILL_MD_BYTES = 1 * 1024 * 1024
MAX_DEPTH = 8

# Things that should never be inside a published skill
EXCLUDED_NAMES = {"__MACOSX", "Thumbs.db", "desktop.ini"}

# A references/... (or scripts/, assets/) path mentioned in SKILL.md, e.g. `references/sources.md`
RESOURCE_REF_RE = re.compile(r"`((?:references|scripts|assets)/[^`\s]+)`")


def find_skills():
    return sorted(
        d for d in os.listdir(ROOT)
        if os.path.isdir(os.path.join(ROOT, d))
        and not d.startswith(".")
        and os.path.isfile(os.path.join(ROOT, d, "SKILL.md"))
    )


def read_frontmatter(text):
    """Return the top-level frontmatter keys as a dict of raw string values.

    This deliberately handles only the simple single-line `key: value` form used in
    this repo, so the script needs no YAML library. Nested keys under `metadata:` are skipped.
    """
    if not text.startswith("---\n"):
        return None, "SKILL.md must start with a '---' frontmatter block"
    end = text.find("\n---\n", 4)
    if end == -1:
        return None, "SKILL.md frontmatter is not closed with '---'"
    if not text[end + 5:].strip():
        return None, "SKILL.md has no body after the frontmatter"
    fields = {}
    for line in text[4:end].splitlines():
        if not line.strip() or line.startswith((" ", "\t", "#")):
            continue
        key, sep, value = line.partition(":")
        if not sep:
            return None, f"frontmatter line is not 'key: value': {line!r}"
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        fields[key.strip()] = value
    return fields, None


def collect_files(skill):
    """Return (files, folders) inside the skill, as paths relative to ROOT, excluding junk."""
    files, folders = [], []
    base = os.path.join(ROOT, skill)
    for current, dirs, names in os.walk(base):
        dirs[:] = sorted(d for d in dirs if not d.startswith(".") and d not in EXCLUDED_NAMES)
        rel_dir = os.path.relpath(current, ROOT)
        folders.append(rel_dir)
        for name in sorted(names):
            if name.startswith(".") or name in EXCLUDED_NAMES:
                continue
            files.append(os.path.join(rel_dir, name))
    return files, folders


def validate(skill):
    errors, warnings = [], []
    skill_md = os.path.join(ROOT, skill, "SKILL.md")
    with open(skill_md, encoding="utf-8") as fh:
        text = fh.read()

    fields, problem = read_frontmatter(text)
    if problem:
        return [problem], warnings

    name = fields.get("name", "")
    if not name:
        errors.append("frontmatter is missing 'name'")
    else:
        if len(name) > MAX_NAME or not NAME_RE.match(name):
            errors.append(f"name '{name}' must be 1-{MAX_NAME} lowercase letters, digits and single hyphens")
        if name != skill:
            errors.append(f"name '{name}' must match its folder name '{skill}'")

    description = fields.get("description", "")
    if not description:
        errors.append("frontmatter is missing 'description'")
    elif len(description) > MAX_DESCRIPTION:
        errors.append(f"description is {len(description)} characters (max {MAX_DESCRIPTION})")

    compatibility = fields.get("compatibility")
    if compatibility is not None and not 1 <= len(compatibility) <= MAX_COMPATIBILITY:
        errors.append(f"compatibility must be 1-{MAX_COMPATIBILITY} characters")

    line_count = text.count("\n") + 1
    if line_count > MAX_SKILL_LINES:
        warnings.append(f"SKILL.md is {line_count} lines; the spec recommends under {MAX_SKILL_LINES}")

    if os.path.getsize(skill_md) > MAX_SKILL_MD_BYTES:
        errors.append("SKILL.md is larger than 1 MB")

    files, folders = collect_files(skill)
    skill_mds = [f for f in files if os.path.basename(f) == "SKILL.md"]
    if len(skill_mds) != 1:
        errors.append(f"expected exactly one SKILL.md, found {len(skill_mds)}: {skill_mds}")

    entries = len(files) + len(folders)
    if entries > MAX_ENTRIES:
        errors.append(f"{entries} files and folders (max {MAX_ENTRIES})")

    for f in files:
        depth = f.count(os.sep)  # folders above the file, including the skill folder
        if depth > MAX_DEPTH:
            errors.append(f"{f} is nested {depth} folders deep (max {MAX_DEPTH})")

    extracted = sum(os.path.getsize(os.path.join(ROOT, f)) for f in files)
    if extracted > MAX_EXTRACTED_BYTES:
        errors.append(f"skill is {extracted} bytes uncompressed (max {MAX_EXTRACTED_BYTES})")

    # Every resource SKILL.md points to must actually ship with the skill.
    for ref in sorted(set(RESOURCE_REF_RE.findall(text))):
        if not os.path.isfile(os.path.join(ROOT, skill, ref)):
            errors.append(f"SKILL.md refers to `{ref}`, which doesn't exist in the skill folder")

    return errors, warnings


def build(skill):
    os.makedirs(DIST, exist_ok=True)
    out = os.path.join(DIST, f"{skill}.zip")
    files, _ = collect_files(skill)
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as zf:
        for f in files:
            zf.write(os.path.join(ROOT, f), f.replace(os.sep, "/"))

    size = os.path.getsize(out)
    if size > MAX_ZIP_BYTES:
        raise SystemExit(f"{out} is {size} bytes (max {MAX_ZIP_BYTES})")
    with zipfile.ZipFile(out) as zf:
        bad = zf.testzip()
        if bad:
            raise SystemExit(f"{out} is corrupt at {bad}")
        tops = {n.split("/", 1)[0] for n in zf.namelist()}
        if tops != {skill}:
            raise SystemExit(f"{out} must contain a single top-level folder '{skill}', found {sorted(tops)}")
    return out, size


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--check", action="store_true", help="validate only; don't build zips")
    args = parser.parse_args()

    skills = find_skills()
    if not skills:
        print("No skills found (top-level folders containing SKILL.md).")
        return 1

    failed = False
    for skill in skills:
        errors, warnings = validate(skill)
        for w in warnings:
            print(f"WARN  {skill}: {w}")
        for e in errors:
            print(f"FAIL  {skill}: {e}")
        if errors:
            failed = True
        else:
            print(f"OK    {skill}")

    if failed:
        print("\nValidation failed; no zips were built.")
        return 1
    if args.check:
        return 0

    print()
    for skill in skills:
        out, size = build(skill)
        print(f"Built {os.path.relpath(out, ROOT)} ({size:,} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
