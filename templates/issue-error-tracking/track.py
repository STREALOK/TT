# SPDX-License-Identifier: AGPL-3.0-only
"""Bounded, offline issue ledger. Approval attestations are evidence, not authority."""
import argparse
import copy
import datetime as dt
import hashlib
import json
import math
import re
import sys
from pathlib import Path

MAX_BYTES = 1024 * 1024
MAX_RECORDS = 1000
MAX_TEXT = 4096
WEIGHTS = {"impact": 3, "reach": 2, "recurrence": 2,
           "persistence": 1, "reversibility": 2}
COMMON = {"type", "id", "revision", "provenance", "screening"}
FIELDS = {
    "issue": COMMON | {"title", "owner", "kind", "system_side", "status",
        "classification", "fix_state", "created_at", "updated_at", "first_observed",
        "earliest_located", "origin", "fixed_at", "closed_reason", "supersedes",
        "observed", "expected", "steps", "reproduction", "cause", "hoped_fix",
        "acceptance_scope", "confidence", "verification_cost", "weights", "public_summary"},
    "error": COMMON | {"issue_id", "observed_at", "recorded_at", "signature",
        "dedupe_key", "grouping_version", "expectation", "transience", "evidence",
        "occurrence_count", "count_basis", "count_source", "window_start", "window_end"},
    "trial": COMMON | {"issue_id", "observed_at", "recorded_at", "method",
        "environment", "duration_seconds", "outcome", "result_scope", "use_mode",
        "events_observed", "event_kind", "exposures", "count_basis", "count_source",
        "window_start", "window_end", "issue_revision", "artifact", "scenario"},
    "transition": COMMON | {"issue_id", "recorded_at", "field", "before", "after", "reason"},
}
PREFIX = {"issue": "ISS", "error": "ERR", "trial": "TRY", "transition": "CHG"}


class LedgerError(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise LedgerError(message)


def shape(obj, keys, where):
    require(type(obj) is dict and set(obj) == set(keys), where + ": incorrect fields")


def string(value, where, nullable=False, empty=False):
    if value is None and nullable:
        return
    require(type(value) is str and len(value) <= MAX_TEXT and (empty or value.strip()),
            where + ": expected bounded text")
    require(not any(ord(c) < 32 and c not in "\n\r\t" for c in value),
            where + ": control character")


def integer(value, where, minimum=0, maximum=10**9, nullable=False):
    if value is None and nullable:
        return
    require(type(value) is int and minimum <= value <= maximum,
            where + ": expected integer in range")


def number(value, where, minimum=0, maximum=10**9, nullable=False):
    if value is None and nullable:
        return
    require(type(value) in (int, float) and minimum <= value <= maximum
            and math.isfinite(value), where + ": expected finite number in range")


def enum(value, choices, where):
    require(type(value) is str and value in choices.split("|"), where + ": invalid enum")


def utc(value, where, nullable=False):
    if value is None and nullable:
        return None
    require(type(value) is str and re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", value),
            where + ": expected UTC YYYY-MM-DDTHH:MM:SSZ")
    try:
        return dt.datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=dt.timezone.utc)
    except ValueError:
        raise LedgerError(where + ": invalid calendar time") from None


def identifier(value, kind, where, nullable=False):
    if value is None and nullable:
        return
    require(type(value) is str and re.fullmatch(PREFIX[kind] + r"-[A-Za-z0-9][A-Za-z0-9_-]{0,63}", value),
            where + ": invalid id")


def texts(value, where, maximum=64):
    require(type(value) is list and len(value) <= maximum, where + ": expected bounded list")
    for text in value:
        string(text, where)


def hex_digest(value, where, nullable=False):
    if value is None and nullable:
        return
    require(type(value) is str and re.fullmatch(r"[a-f0-9]{64}", value), where + ": invalid SHA-256")


def validate_common(r):
    k = r["type"]
    identifier(r["id"], k, "id")
    integer(r["revision"], "revision", 1)
    require(type(r["provenance"]) is list and len(r["provenance"]) <= 64,
            "provenance: expected bounded list")
    for p in r["provenance"]:
        shape(p, {"ref", "sha256", "rights", "redaction", "public_excerpt", "privacy_flags"}, "provenance")
        string(p["ref"], "provenance.ref")
        hex_digest(p["sha256"], "provenance.sha256", True)
        enum(p["rights"], "owned|licensed|permission|restricted|unknown", "provenance.rights")
        enum(p["redaction"], "none|partial|complete|unknown", "provenance.redaction")
        string(p["public_excerpt"], "provenance.public_excerpt", True)
        texts(p["privacy_flags"], "provenance.privacy_flags", 16)
    s = r["screening"]
    shape(s, {"status", "reviewer", "date", "revision", "text_digest"}, "screening")
    enum(s["status"], "pending|approved|rejected", "screening.status")
    string(s["reviewer"], "screening.reviewer", True)
    integer(s["revision"], "screening.revision", 1, nullable=True)
    hex_digest(s["text_digest"], "screening.text_digest", True)
    if s["date"] is not None:
        require(type(s["date"]) is str and re.fullmatch(r"\d{4}-\d{2}-\d{2}", s["date"]), "screening.date: invalid date")
        try:
            dt.date.fromisoformat(s["date"])
        except ValueError:
            raise LedgerError("screening.date: invalid calendar date") from None
    if s["status"] == "approved":
        require(all(s[x] is not None for x in ("reviewer", "date", "revision", "text_digest")),
                "approved screening requires reviewer, date, revision and digest")


def validate_issue(r):
    for key in ("title", "owner", "observed", "expected", "hoped_fix"):
        string(r[key], key)
    for key in ("closed_reason", "public_summary"):
        string(r[key], key, True)
    texts(r["steps"], "steps")
    enum(r["kind"], "issue|error|suspicion|process|documentation", "kind")
    enum(r["system_side"], "root_app|cloud|model|mechanical|human|workflow|documentation", "system_side")
    enum(r["status"], "open|fixed|wontfix|superseded|monitoring", "status")
    enum(r["classification"], "confirmed|repaired|suspicion|unknown", "classification")
    enum(r["fix_state"], "none|proposed|applied|synthetic-pass|live-verified", "fix_state")
    enum(r["origin"], "unknown|proven", "origin")
    enum(r["acceptance_scope"], "none|synthetic|in-use|document", "acceptance_scope")
    times = {k: utc(r[k], k, k not in ("created_at", "updated_at")) for k in
             ("created_at", "updated_at", "first_observed", "earliest_located", "fixed_at")}
    require(times["updated_at"] >= times["created_at"], "updated_at precedes created_at")
    if times["fixed_at"]:
        require(times["created_at"] <= times["fixed_at"] <= times["updated_at"], "fixed_at outside record lifetime")
    identifier(r["supersedes"], "issue", "supersedes", True)
    require(r["supersedes"] != r["id"], "issue cannot supersede itself")
    shape(r["reproduction"], {"status", "source"}, "reproduction")
    enum(r["reproduction"]["status"], "reproduced|not-reproduced|unknown", "reproduction.status")
    string(r["reproduction"]["source"], "reproduction.source", True)
    require(r["reproduction"]["status"] == "unknown" or r["reproduction"]["source"] is not None,
            "reproduction decision requires source")
    shape(r["cause"], {"status", "description"}, "cause")
    enum(r["cause"]["status"], "proven|suspected|unknown", "cause.status")
    string(r["cause"]["description"], "cause.description", True)
    require(r["cause"]["status"] == "unknown" or r["cause"]["description"] is not None,
            "cause decision requires description")
    require(r["origin"] != "proven" or bool(r["provenance"]), "proven origin requires provenance")
    number(r["confidence"], "confidence", maximum=1, nullable=True)
    shape(r["verification_cost"], {"level", "estimate_minutes", "note"}, "verification_cost")
    enum(r["verification_cost"]["level"], "low|medium|high|unknown", "verification_cost.level")
    number(r["verification_cost"]["estimate_minutes"], "verification_cost.estimate_minutes", nullable=True)
    string(r["verification_cost"]["note"], "verification_cost.note", empty=True)
    shape(r["weights"], WEIGHTS, "weights")
    for key, value in r["weights"].items():
        integer(value, "weights." + key, 1, 5, True)
    if r["status"] in ("fixed", "wontfix", "superseded"):
        require(r["closed_reason"] is not None, "closed status requires rationale")
    if r["status"] == "fixed":
        require(r["fixed_at"] is not None and r["acceptance_scope"] != "none",
                "fixed status requires explicit fixed_at and acceptance_scope")
        require(r["fix_state"] in ("applied", "synthetic-pass", "live-verified"),
                "fixed status requires an applied fix")


def validate_counts(r, count_key):
    integer(r[count_key], count_key, 1 if count_key == "occurrence_count" else 0, nullable=True)
    enum(r["count_basis"], "observed|unknown", "count_basis")
    string(r["count_source"], "count_source", True)
    start = utc(r["window_start"], "window_start", True)
    end = utc(r["window_end"], "window_end", True)
    require((start is None) == (end is None), "observation window requires both endpoints")
    if start:
        require(start <= end, "observation window reversed")
    if r[count_key] is not None:
        require(r["count_basis"] == "observed" and r["count_source"] is not None and start is not None,
                "known count requires observed provenance and window")
    else:
        require(r["count_basis"] == "unknown", "unknown count requires unknown basis")


def validate_observation(r):
    if r["type"] == "transition":
        identifier(r["issue_id"], "issue", "issue_id")
        utc(r["recorded_at"], "recorded_at")
        string(r["reason"], "reason")
        enum(r["field"], "status|fix_state|classification|revision", "field")
        require(r["before"] != r["after"], "transition requires a change")
        choices = {"status": "open|fixed|wontfix|superseded|monitoring",
                   "fix_state": "none|proposed|applied|synthetic-pass|live-verified",
                   "classification": "confirmed|repaired|suspicion|unknown"}
        for key in ("before", "after"):
            if r["field"] == "revision":
                integer(r[key], key, 1)
            else:
                enum(r[key], choices[r["field"]], key)
        if r["field"] == "revision":
            require(r["after"] > r["before"], "transition revision must increase")
        return
    observed = utc(r["observed_at"], "observed_at", True)
    recorded = utc(r["recorded_at"], "recorded_at")
    require(observed is None or recorded >= observed, "recorded_at precedes observed_at")
    if r["type"] == "error":
        identifier(r["issue_id"], "issue", "issue_id", True)
        for key in ("signature", "dedupe_key", "grouping_version"):
            string(r[key], key)
        enum(r["expectation"], "expected|unexpected|unknown", "expectation")
        enum(r["transience"], "transient|persistent|unknown", "transience")
        texts(r["evidence"], "evidence")
        validate_counts(r, "occurrence_count")
    else:
        identifier(r["issue_id"], "issue", "issue_id")
        integer(r["issue_revision"], "issue_revision", 1)
        shape(r["artifact"], {"ref", "sha256", "version"}, "artifact")
        string(r["artifact"]["ref"], "artifact.ref", True)
        string(r["artifact"]["version"], "artifact.version", True)
        hex_digest(r["artifact"]["sha256"], "artifact.sha256", True)
        for key in ("method", "environment", "scenario"):
            string(r[key], key)
        number(r["duration_seconds"], "duration_seconds", nullable=True)
        enum(r["outcome"], "pass|fail|inconclusive", "outcome")
        enum(r["use_mode"], "synthetic|in-use|document", "use_mode")
        enum(r["event_kind"], "behavior|tool|log|unknown", "event_kind")
        require(r["result_scope"] == {"synthetic": "synthetic-fixture", "in-use": "in-use-observation",
                    "document": "document-review"}[r["use_mode"]], "result_scope conflicts with use_mode")
        integer(r["exposures"], "exposures", nullable=True)
        validate_counts(r, "events_observed")
        if r["exposures"] is not None and r["events_observed"] is not None and r["event_kind"] == "behavior":
            require(r["events_observed"] <= r["exposures"], "behavior events exceed exposures")
    if r["window_end"] is not None:
        require(utc(r["window_end"], "window_end") <= recorded, "window ends after recorded_at")
        if observed is not None:
            require(utc(r["window_start"], "window_start") <= observed <= utc(r["window_end"], "window_end"),
                    "observed_at outside count window")


def payload(record):
    return {k: v for k, v in record.items() if k != "screening"}


def digest(record, records):
    """Canonical UTF-8 JSON payload; issue digest additionally binds all linked observations."""
    bundle = [payload(record)]
    if record["type"] == "issue":
        bundle += [payload(r) for r in sorted(records, key=lambda x: x["id"])
                   if r["type"] != "issue" and r["issue_id"] == record["id"]]
    data = json.dumps(bundle, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)
    return hashlib.sha256(data.encode("utf-8")).hexdigest()


def approved(record, records):
    s = record["screening"]
    return (s["status"] == "approved" and s["revision"] == record["revision"]
            and s["text_digest"] == digest(record, records))


def validate(records, baseline=None):
    require(type(records) is list and len(records) <= MAX_RECORDS, "record limit exceeded")
    ids = set()
    observation_keys = set()
    for r in records:
        require(type(r) is dict and type(r.get("type")) is str and r["type"] in FIELDS, "invalid record type")
        shape(r, FIELDS[r["type"]], "record")
        validate_common(r)
        require(r["id"] not in ids, "duplicate record id")
        ids.add(r["id"])
        (validate_issue if r["type"] == "issue" else validate_observation)(r)
        if r["type"] == "error":
            key = (r["grouping_version"], r["dedupe_key"])
            require(key not in observation_keys, "duplicate error observation key")
            observation_keys.add(key)
    issues = {r["id"]: r for r in records if r["type"] == "issue"}
    for r in records:
        if r["type"] != "issue":
            require(r["issue_id"] is None or r["issue_id"] in issues, "dangling issue reference")
            if r["type"] == "trial":
                require(r["issue_revision"] <= issues[r["issue_id"]]["revision"], "trial references future issue revision")
            if r["type"] == "transition":
                require(r["recorded_at"] <= issues[r["issue_id"]]["updated_at"], "transition recorded after issue update")
            continue
        require(r["supersedes"] is None or r["supersedes"] in issues, "dangling supersedes reference")
        if r["status"] == "superseded":
            require(any(x["supersedes"] == r["id"] for x in issues.values()), "superseded issue requires successor")
        candidates = [x for x in records if x["type"] == "trial" and x["issue_id"] == r["id"]
                      and x["issue_revision"] == r["revision"]]
        latest = {}
        for x in sorted(candidates, key=lambda x: (x["recorded_at"], x["id"])):
            latest[x["use_mode"]] = x
        def valid_pass(x, cutoff):
            return (x["outcome"] == "pass" and x["observed_at"] is not None and x["recorded_at"] <= cutoff
                    and x["artifact"]["ref"] is not None
                    and (x["artifact"]["sha256"] is not None or x["artifact"]["version"] is not None))
        passing = {mode for mode, x in latest.items() if valid_pass(x, r["updated_at"])}
        if r["fix_state"] == "synthetic-pass":
            require("synthetic" in passing, "synthetic-pass requires passing synthetic trial")
        if r["fix_state"] == "live-verified":
            require("in-use" in passing, "live-verified requires passing in-use trial")
        if r["status"] == "fixed":
            require(r["acceptance_scope"] in latest and valid_pass(latest[r["acceptance_scope"]], r["fixed_at"]),
                    "fixed acceptance requires current matching passing trial before fixed_at")
    for issue in issues.values():
        seen = set()
        cursor = issue
        while cursor["supersedes"] is not None:
            require(cursor["id"] not in seen, "supersedes cycle")
            seen.add(cursor["id"])
            cursor = issues[cursor["supersedes"]]
    chains = {}
    for r in sorted((x for x in records if x["type"] == "transition"), key=lambda x: (x["recorded_at"], x["id"])):
        key = (r["issue_id"], r["field"])
        if key in chains:
            require(chains[key] == r["before"], "transition chain is discontinuous")
        chains[key] = r["after"]
    for (issue_id, field), value in chains.items():
        require(issues[issue_id][field] == value, "latest transition disagrees with issue snapshot")
    if baseline is not None:
        validate(baseline)
        current = {r["id"]: r for r in records}
        for old in baseline:
            require(old["id"] in current, "baseline record removed")
            new = current[old["id"]]
            require(new["revision"] >= old["revision"], "revision regressed")
            if old["type"] in ("error", "trial", "transition"):
                require(payload(old) == payload(new), "immutable observation changed")
            elif payload(old) != payload(new):
                require(new["revision"] > old["revision"], "edited issue requires new revision")
    return records


def no_duplicates(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, "duplicate JSON key")
        result[key] = value
    return result


def load(path):
    with Path(path).open("rb") as handle:
        data = handle.read(MAX_BYTES + 1)
    require(len(data) <= MAX_BYTES, "file size limit exceeded")
    try:
        lines = data.decode("utf-8").splitlines()
    except UnicodeError:
        raise LedgerError("ledger is not UTF-8") from None
    records = []
    for line in lines:
        if not line.strip():
            continue
        require(len(records) < MAX_RECORDS, "record limit exceeded")
        try:
            record = json.loads(line, object_pairs_hook=no_duplicates,
                                parse_constant=lambda _: (_ for _ in ()).throw(LedgerError("nonfinite JSON number")))
        except (json.JSONDecodeError, RecursionError):
            raise LedgerError("invalid JSON record") from None
        records.append(record)
    return validate(records)


def score(issue):
    missing = [key for key in WEIGHTS if issue["weights"][key] is None]
    return {"weight": None if missing else sum(issue["weights"][key] * factor for key, factor in WEIGHTS.items()),
            "missing": missing, "confidence": issue["confidence"], "verification_cost": issue["verification_cost"]}


def warnings(records):
    result = []
    for r in records:
        rid = r["id"]
        if r["type"] == "issue":
            missing = score(r)["missing"]
            if missing:
                result.append(rid + ": unscored; missing " + ", ".join(missing))
        if r["screening"]["status"] == "approved" and not approved(r, records):
            result.append(rid + ": stale screening revision or digest")
        if r["type"] == "error" and r["occurrence_count"] is None:
            result.append(rid + ": occurrence count unknown")
        if r["type"] == "trial":
            issue = next(x for x in records if x["id"] == r["issue_id"])
            if r["issue_revision"] != issue["revision"]:
                result.append(rid + ": historical trial; issue revision differs")
        if any(p["privacy_flags"] for p in r["provenance"]):
            result.append(rid + ": declared privacy flags; manual review needed")
        text = json.dumps(payload(r), ensure_ascii=False)
        if re.search(r"(?i)(?:[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}|[A-Z]:\\\\|(?:api[_-]?key|password|secret)\s*[:=])", text):
            result.append(rid + ": possible private text; heuristic warning only")
    return result


def literal(text):
    """Render supplied text as quoted plain text without active Markdown/HTML."""
    return "\n".join("> " + re.sub(r"([\\`*_{}\[\]()#+.!|<>-])", r"\\\1", line)
                     for line in text.splitlines())


def render(records, public=False):
    validate(records)
    issues = [r for r in records if r["type"] == "issue"]
    if public:
        selected = []
        for r in issues:
            if r["screening"]["status"] != "approved":
                continue
            linked = [x for x in records if x["type"] != "issue" and x["issue_id"] == r["id"]]
            require(all(approved(x, records) for x in [r] + linked), "public export blocked by missing or stale screening")
            for x in [r] + linked:
                require(all(p["rights"] not in ("restricted", "unknown") and p["redaction"] != "unknown"
                            and not p["privacy_flags"] for p in x["provenance"]),
                        "public export blocked by provenance rights, redaction or declared privacy flags")
            require(r["public_summary"] is not None, "public export requires authored public_summary")
            selected.append(r)
        issues = selected
    lines = ["# Issue ledger (" + ("public approved excerpts" if public else "local/private") + ")",
             "", "Reviewer attestations are recorded evidence, not authenticated authority.", ""]
    if not public:
        errors = [r for r in records if r["type"] == "error"]
        known = sum(r["occurrence_count"] for r in errors if r["occurrence_count"] is not None)
        unknown = sum(r["occurrence_count"] is None for r in errors)
        lines += [f"Records: {len(records)}; error observation records: {len(errors)}; observed occurrences: {known}; unknown-count records: {unknown}.",
                  "Trial tool/log events and manual transitions are separate from error occurrences. Audit coverage depends on supplied transition records.", ""]
        lines += ["Warning: " + w for w in warnings(records)] + [""]
        untriaged = [r for r in errors if r["issue_id"] is None]
        if untriaged:
            lines += ["## Untriaged error observations", ""]
            for r in untriaged:
                lines += ["Observation " + r["id"] + ":", literal(json.dumps(payload(r), ensure_ascii=False)), ""]
    for r in issues:
        result = score(r)
        weight = "unscored" if result["weight"] is None else str(result["weight"]) + "/50"
        lines += ["## " + r["id"], "", f"Status: {r['status']}; classification: {r['classification']}; fix: {r['fix_state']}; weight: {weight}.", ""]
        if public:
            lines += [literal(r["public_summary"]), ""]
            if r["status"] != "fixed":
                for p in r["provenance"]:
                    if p["public_excerpt"] is not None:
                        lines += [literal(p["public_excerpt"]), ""]
        else:
            lines += [literal(r["title"]), "", "Owner:", literal(r["owner"]), "",
                "Observed:", literal(r["observed"]), "", "Expected:", literal(r["expected"]), "",
                f"First observed: {r['first_observed']}; earliest located: {r['earliest_located']}; origin: {r['origin']}.",
                f"Fixed at: {r['fixed_at']}; updated at: {r['updated_at']}; acceptance: {r['acceptance_scope']}.",
                "Confidence and verification cost: " + json.dumps({k: result[k] for k in ("confidence", "verification_cost")}), "",
                "Reproduction, cause, steps and hoped fix:", literal(json.dumps({k: r[k] for k in ("reproduction", "cause", "steps", "hoped_fix", "closed_reason")}, ensure_ascii=False)), "",
                "Provenance:", literal(json.dumps(r["provenance"], ensure_ascii=False)), ""]
            for child in records:
                if child["type"] != "issue" and child["issue_id"] == r["id"]:
                    lines += ["Observation " + child["id"] + ":", literal(json.dumps(payload(child), ensure_ascii=False)), ""]
    if not issues:
        lines += ["No eligible issues.", ""]
    return "\n".join(lines)


def example_issue():
    """Neutral example only. No workspace observations, approvals, or measured score."""
    return {"type": "issue", "id": "ISS-example", "revision": 1,
        "title": "Example: record an observation", "owner": "unassigned", "kind": "issue",
        "system_side": "workflow", "status": "open", "classification": "unknown", "fix_state": "none",
        "created_at": "2026-10-05T00:00:00Z", "updated_at": "2026-10-05T00:00:00Z",
        "first_observed": None, "earliest_located": None, "origin": "unknown", "fixed_at": None,
        "closed_reason": None, "supersedes": None, "observed": "Replace with a bounded observation.",
        "expected": "Replace with the expected behavior.", "steps": [],
        "reproduction": {"status": "unknown", "source": None},
        "cause": {"status": "unknown", "description": None}, "hoped_fix": "To be investigated.",
        "acceptance_scope": "none", "confidence": None,
        "verification_cost": {"level": "unknown", "estimate_minutes": None, "note": ""},
        "weights": {key: None for key in WEIGHTS}, "public_summary": None, "provenance": [],
        "screening": {"status": "pending", "reviewer": None, "date": None, "revision": None, "text_digest": None}}


def example_records():
    """Fictional fixture: a synthetic passing trial leaves the issue open and unverified."""
    issue = example_issue()
    common = {"revision": 1, "provenance": [], "screening": copy.deepcopy(issue["screening"]),
              "issue_id": issue["id"], "observed_at": "2026-10-05T00:00:00Z",
              "recorded_at": "2026-10-05T00:00:00Z", "count_basis": "observed",
              "count_source": "Fictional fixture, not workspace evidence.",
              "window_start": "2026-10-05T00:00:00Z", "window_end": "2026-10-05T00:00:00Z"}
    error = dict(copy.deepcopy(common), type="error", id="ERR-example", signature="fictional-example",
                 dedupe_key="fictional-example-v1", grouping_version="example-v1", expectation="unexpected",
                 transience="unknown", evidence=["fictional://example"], occurrence_count=1)
    trial = dict(copy.deepcopy(common), type="trial", id="TRY-example", method="Fictional synthetic check.",
                 environment="Fictional fixture.", duration_seconds=None, outcome="pass",
                 result_scope="synthetic-fixture", use_mode="synthetic", events_observed=0,
                 event_kind="behavior", exposures=1, issue_revision=1,
                 artifact={"ref": "fictional://fixture", "sha256": None, "version": "fixture-v1"},
                 scenario="Fictional neutral test scenario.")
    return [issue, error, trial]


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    for command in ("check", "score", "report", "digest"):
        cmd = sub.add_parser(command)
        cmd.add_argument("ledger")
        if command == "check":
            cmd.add_argument("--baseline")
        if command == "report":
            cmd.add_argument("--public", action="store_true")
            cmd.add_argument("--output", help="new output file; existing files are never overwritten")
    init = sub.add_parser("init")
    init.add_argument("ledger", help="new empty ledger file; parent directory must exist")
    example = sub.add_parser("example", help="print neutral examples; does not write files")
    example.add_argument("--bundle", action="store_true", help="include fictional error and trial")
    args = parser.parse_args(argv)
    try:
        if args.command == "init":
            with Path(args.ledger).open("xb"):
                pass
            print("Created empty private ledger.")
            return 0
        if args.command == "example":
            for record in example_records() if args.bundle else [example_issue()]:
                print(json.dumps(record, ensure_ascii=False, sort_keys=True))
            return 0
        records = load(args.ledger)
        if args.command == "check":
            validate(records, load(args.baseline) if args.baseline else None)
            print(json.dumps({"records": len(records), "warnings": warnings(records)}))
        elif args.command == "score":
            print(json.dumps({r["id"]: score(r) for r in records if r["type"] == "issue"}))
        elif args.command == "digest":
            print(json.dumps({r["id"]: {"revision": r["revision"], "text_digest": digest(r, records)} for r in records}))
        else:
            report = render(records, args.public)
            if args.output:
                with Path(args.output).open("x", encoding="utf-8", newline="\n") as handle:
                    handle.write(report)
                print("Created report.")
            else:
                print(report)
        return 0
    except (LedgerError, OSError, UnicodeError) as exc:
        # Never echo paths, record contents, OS exception messages, or tracebacks.
        print("Ledger rejected: " + (str(exc) if isinstance(exc, LedgerError) else type(exc).__name__), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
