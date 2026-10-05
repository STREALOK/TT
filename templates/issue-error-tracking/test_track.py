# SPDX-License-Identifier: AGPL-3.0-only
"""Semantic and fail-closed boundaries, without external processes or services."""
import contextlib
import copy
import io
import json
from pathlib import Path
import tempfile
import unittest

import track


class LedgerTests(unittest.TestCase):
    def setUp(self):
        self.records = track.example_records()

    def reject(self, records):
        with self.assertRaises(track.LedgerError):
            track.validate(records)

    def approve(self, records):
        for r in records:
            r["screening"] = {"status": "approved", "reviewer": "Fixture reviewer",
                "date": "2026-10-05", "revision": r["revision"],
                "text_digest": track.digest(r, records)}

    def public(self, records):
        records[0]["public_summary"] = "Newly authored fictional public summary."
        self.approve(records)
        return track.render(records, public=True)

    def test_fixture_pass_does_not_promote_issue(self):
        before = copy.deepcopy(self.records)
        track.validate(self.records)
        track.render(self.records)
        self.assertEqual(self.records, before)
        self.assertEqual(self.records[0]["status"], "open")
        self.assertEqual(self.records[0]["fix_state"], "none")

    def test_weights_range_unknown_and_independent_cost(self):
        issue = self.records[0]
        self.assertIsNone(track.score(issue)["weight"])
        self.assertIn("impact", track.score(issue)["missing"])
        issue["weights"] = {k: 1 for k in track.WEIGHTS}
        self.assertEqual(track.score(issue)["weight"], 10)
        issue["weights"] = {k: 5 for k in track.WEIGHTS}
        self.assertEqual(track.score(issue)["weight"], 50)
        issue["confidence"] = 0.1
        issue["verification_cost"]["estimate_minutes"] = 10000
        self.assertEqual(track.score(issue)["weight"], 50)
        issue["weights"]["reach"] = None
        self.assertIsNone(track.score(issue)["weight"])
        self.assertTrue(any("unscored" in w for w in track.warnings(self.records)))

    def test_booleans_not_counts_weights_revision_confidence(self):
        for index, key in ((0, "revision"), (0, "confidence"), (1, "occurrence_count"),
                           (2, "events_observed"), (2, "exposures"), (2, "duration_seconds")):
            with self.subTest(key=key):
                records = copy.deepcopy(self.records)
                records[index][key] = True
                self.reject(records)
        self.records[0]["weights"]["impact"] = True
        self.reject(self.records)

    def test_strict_schema_ids_enums_and_duplicate_ids(self):
        for change in ({"unexpected_field": "secret"}, {"id": "../path"}, {"status": "resolved"}):
            records = copy.deepcopy(self.records)
            records[0].update(change)
            self.reject(records)
        records = copy.deepcopy(self.records)
        del records[0]["owner"]
        self.reject(records)
        self.reject(self.records + [copy.deepcopy(self.records[0])])
        self.records[1]["issue_id"] = "ISS-missing"
        self.reject(self.records)

    def test_dangling_trial_and_supersedes(self):
        records = copy.deepcopy(self.records)
        records[2]["issue_id"] = "ISS-missing"
        self.reject(records)
        self.records[0]["supersedes"] = "ISS-missing"
        self.reject(self.records)

    def test_calendar_utc_and_recording_order(self):
        for invalid in ("2026-02-30T00:00:00Z", "2026-10-05T00:00:00+00:00",
                        "2026-10-05", "2026-10-05T24:00:00Z", True):
            records = copy.deepcopy(self.records)
            records[1]["observed_at"] = invalid
            self.reject(records)
        self.records[1]["recorded_at"] = "2026-10-04T00:00:00Z"
        self.reject(self.records)

    def test_count_provenance_and_unknown_count(self):
        records = copy.deepcopy(self.records)
        records[1]["count_source"] = None
        self.reject(records)
        records = copy.deepcopy(self.records)
        records[1]["window_start"] = None
        self.reject(records)
        records = copy.deepcopy(self.records)
        records[1]["window_end"] = "2026-10-04T00:00:00Z"
        self.reject(records)
        records = copy.deepcopy(self.records)
        records[1]["occurrence_count"] = None
        records[1]["count_basis"] = "unknown"
        records[1]["window_start"] = records[1]["window_end"] = None
        records[1]["count_source"] = None
        track.validate(records)
        report = track.render(records)
        self.assertIn("observed occurrences: 0; unknown-count records: 1", report)
        records[2]["events_observed"] = 2
        self.reject(records)

    def test_logging_events_never_inflate_incident_count(self):
        self.records[2]["events_observed"] = 99
        self.records[2]["event_kind"] = "log"
        report = track.render(self.records)
        self.assertIn("observed occurrences: 1;", report)
        self.assertIn('"events_observed": 99', report.replace("\\", ""))

    def test_duplicate_observation_key_rejects_copied_occurrence_counts(self):
        duplicate = copy.deepcopy(self.records[1])
        duplicate["id"] = "ERR-copied"
        self.records.append(duplicate)
        self.reject(self.records)
        duplicate["dedupe_key"] = "distinct-observation"
        track.validate(self.records)

    def test_private_report_includes_untriaged_observation_payload(self):
        self.records[1]["issue_id"] = None
        self.records[1]["signature"] = "UNTRIAGED-SIGNATURE"
        report = track.render(self.records)
        self.assertIn("observed occurrences: 1;", report)
        self.assertIn("## Untriaged error observations", report)
        self.assertIn("UNTRIAGED", report)
        self.assertIn("SIGNATURE", report)
        self.assertNotIn("UNTRIAGED", track.render(self.records, public=True))

    def test_fixed_requires_explicit_time_reason_and_acceptance(self):
        issue = self.records[0]
        issue.update(status="fixed", fix_state="synthetic-pass", acceptance_scope="synthetic",
                     closed_reason="Fictional synthetic acceptance.")
        self.reject(self.records)
        issue["fixed_at"] = issue["updated_at"]
        track.validate(self.records)
        issue["updated_at"] = "2026-10-06T00:00:00Z"
        track.validate(self.records)
        self.assertEqual(issue["fixed_at"], "2026-10-05T00:00:00Z")
        issue["closed_reason"] = None
        self.reject(self.records)

    def test_synthetic_or_failed_trials_cannot_prove_live(self):
        self.records[0]["fix_state"] = "live-verified"
        self.reject(self.records)
        self.records[2].update(use_mode="in-use", result_scope="in-use-observation", outcome="fail")
        self.reject(self.records)
        self.records[2]["outcome"] = "pass"
        track.validate(self.records)
        self.records[2]["result_scope"] = "synthetic-fixture"
        self.reject(self.records)

    def test_failed_synthetic_check_cannot_be_accepted(self):
        self.records[0].update(status="fixed", fix_state="applied", acceptance_scope="synthetic",
            fixed_at="2026-10-05T00:00:00Z", closed_reason="Fictional rationale")
        self.records[2]["outcome"] = "fail"
        self.reject(self.records)

    def test_unknown_observed_time_is_preserved_without_inventing_it(self):
        self.records[1]["observed_at"] = None
        self.records[2]["observed_at"] = None
        track.validate(self.records)
        self.assertIsNone(self.records[1]["observed_at"])
        self.records[0]["fix_state"] = "synthetic-pass"
        self.reject(self.records)

    def test_verification_claims_require_current_trial_revision_and_known_artifact(self):
        self.records[0]["fix_state"] = "synthetic-pass"
        track.validate(self.records)
        self.records[0]["revision"] = 2
        self.reject(self.records)
        self.records[0]["fix_state"] = "none"
        track.validate(self.records)
        self.assertTrue(any("historical trial" in w for w in track.warnings(self.records)))
        self.records[2]["issue_revision"] = 2
        self.records[0]["fix_state"] = "synthetic-pass"
        self.records[2]["artifact"] = {"ref": None, "sha256": None, "version": None}
        self.reject(self.records)
        self.records[2]["artifact"] = {"ref": "fictional://fixture", "sha256": None, "version": "v2"}
        track.validate(self.records)
        self.records[2]["issue_revision"] = 3
        self.reject(self.records)

    def test_fixed_document_requires_passing_document_review(self):
        self.records[0].update(status="fixed", fix_state="applied", acceptance_scope="document",
            fixed_at="2026-10-05T00:00:00Z", closed_reason="Fictional document review")
        self.reject(self.records)
        self.records[2].update(use_mode="document", result_scope="document-review", outcome="fail")
        self.reject(self.records)
        self.records[2]["outcome"] = "pass"
        track.validate(self.records)

    def test_later_failure_and_future_evidence_cannot_support_acceptance(self):
        self.records[0]["fix_state"] = "synthetic-pass"
        later = copy.deepcopy(self.records[2])
        later.update(id="TRY-later", outcome="fail", observed_at="2026-10-06T00:00:00Z",
                     recorded_at="2026-10-06T00:00:00Z", window_start="2026-10-06T00:00:00Z",
                     window_end="2026-10-06T00:00:00Z")
        self.records.append(later)
        self.reject(self.records)
        later["outcome"] = "pass"
        self.reject(self.records)
        self.records[0]["updated_at"] = "2026-10-06T00:00:00Z"
        track.validate(self.records)

    def test_superseded_requires_successor_and_cycles_are_rejected(self):
        self.records[0].update(status="superseded", closed_reason="Fictional successor")
        self.reject(self.records)
        successor = track.example_issue()
        successor.update(id="ISS-successor", supersedes="ISS-example")
        self.records.append(successor)
        track.validate(self.records)
        self.records[0]["supersedes"] = "ISS-successor"
        self.reject(self.records)

    def test_huge_numeric_values_are_rejected_without_overflow(self):
        self.records[0]["confidence"] = 10 ** 1000
        self.reject(self.records)

    def test_public_requires_entire_graph_approval_and_summary(self):
        self.assertIn("No eligible issues", track.render(self.records, public=True))
        self.approve(self.records)
        with self.assertRaises(track.LedgerError):
            track.render(self.records, public=True)
        self.public(self.records)
        self.records[2]["screening"]["status"] = "pending"
        with self.assertRaises(track.LedgerError):
            track.render(self.records, public=True)

    def test_public_omits_private_title_owner_steps_and_fixed_pointers(self):
        issue = self.records[0]
        issue.update(title="PRIVATE-TITLE", owner="PRIVATE-OWNER", observed="PRIVATE-OBSERVED",
                     steps=["PRIVATE-REPRO"], status="fixed", fix_state="synthetic-pass",
                     acceptance_scope="synthetic", closed_reason="PRIVATE-RATIONALE",
                     fixed_at=issue["updated_at"])
        issue["provenance"] = [{"ref": "PRIVATE-ORIGIN", "sha256": "0" * 64,
            "rights": "owned", "redaction": "complete", "public_excerpt": "ORIGIN-EXCERPT",
            "privacy_flags": []}]
        report = self.public(self.records)
        for private in ("PRIVATE-TITLE", "PRIVATE-OWNER", "PRIVATE-OBSERVED", "PRIVATE-REPRO",
                        "PRIVATE-RATIONALE", "PRIVATE-ORIGIN", "ORIGIN-EXCERPT"):
            self.assertNotIn(private, report)
        self.assertIn("Newly authored fictional public summary", report)

    def test_screening_binds_revision_text_children_and_source_hash(self):
        for index, key, value in ((0, "revision", 2), (0, "owner", "Changed owner"),
                                 (2, "method", "Changed trial method")):
            records = copy.deepcopy(self.records)
            self.public(records)
            records[index][key] = value
            with self.assertRaises(track.LedgerError):
                track.render(records, public=True)
        records = copy.deepcopy(self.records)
        records[1]["provenance"] = [{"ref": "fictional://source", "sha256": "0" * 64,
            "rights": "owned", "redaction": "complete", "public_excerpt": None, "privacy_flags": []}]
        self.public(records)
        records[1]["provenance"][0]["sha256"] = "1" * 64
        self.assertTrue(any("stale screening" in w for w in track.warnings(records)))
        with self.assertRaises(track.LedgerError):
            track.render(records, public=True)

    def test_approved_metadata_never_overrides_known_provenance_blocks(self):
        for key, value in (("rights", "unknown"), ("rights", "restricted"),
                           ("redaction", "unknown"), ("privacy_flags", ["private-path"])):
            records = copy.deepcopy(self.records)
            records[0]["provenance"] = [{"ref": "fictional://source", "sha256": None,
                "rights": "owned", "redaction": "complete", "public_excerpt": None, "privacy_flags": []}]
            records[0]["provenance"][0][key] = value
            records[0]["public_summary"] = "Fictional excerpt."
            self.approve(records)
            with self.assertRaises(track.LedgerError):
                track.render(records, public=True)

    def test_digest_is_order_independent_and_attestation_metadata_not_payload(self):
        original = track.digest(self.records[0], self.records)
        self.approve(self.records)
        self.assertEqual(original, track.digest(self.records[0], list(reversed(self.records))))
        self.records[1]["signature"] += "-changed"
        self.assertNotEqual(original, track.digest(self.records[0], self.records))

    def test_baseline_immutability_and_issue_revision(self):
        baseline = copy.deepcopy(self.records)
        for index, key in ((1, "signature"), (2, "method")):
            records = copy.deepcopy(baseline)
            records[index][key] += " changed"
            with self.assertRaises(track.LedgerError):
                track.validate(records, baseline)
        records = copy.deepcopy(baseline)
        records[0]["owner"] = "New owner"
        with self.assertRaises(track.LedgerError):
            track.validate(records, baseline)
        records[0]["revision"] = 2
        track.validate(records, baseline)
        with self.assertRaises(track.LedgerError):
            track.validate(records[:-1], baseline)
        self.approve(self.records)
        track.validate(self.records, baseline)

    def test_manual_transition_links_chain_snapshot_and_immutability(self):
        change = {"type": "transition", "id": "CHG-example", "revision": 1,
            "provenance": [], "screening": copy.deepcopy(self.records[0]["screening"]),
            "issue_id": "ISS-example", "recorded_at": "2026-10-05T00:00:00Z",
            "field": "status", "before": "open", "after": "monitoring", "reason": "Fictional observation window"}
        self.records.append(change)
        self.reject(self.records)
        self.records[0]["status"] = "monitoring"
        track.validate(self.records)
        baseline = copy.deepcopy(self.records)
        change["reason"] = "Changed recorded rationale"
        with self.assertRaises(track.LedgerError):
            track.validate(self.records, baseline)
        change["issue_id"] = "ISS-missing"
        self.reject(self.records)

    def test_render_neutralizes_active_markdown_and_html(self):
        self.records[0]["public_summary"] = "[click](https://example.invalid) <script>alert(1)</script>"
        self.approve(self.records)
        report = track.render(self.records, public=True)
        self.assertNotIn("[click](", report)
        self.assertNotIn("<script>", report)

    def test_reader_duplicate_nested_keys_size_records_and_nonfinite(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "ledger.jsonl"
            for malformed in ('{"type":"issue","type":"error"}', '{"nested":{"x":1,"x":2}}',
                              '{"value":NaN}', '{"value":Infinity}', '{'):
                path.write_text(malformed, encoding="utf-8")
                with self.assertRaises(track.LedgerError):
                    track.load(path)
            path.write_bytes(b" " * (track.MAX_BYTES + 1))
            with self.assertRaises(track.LedgerError):
                track.load(path)
            path.write_bytes(b"\xff")
            with self.assertRaises(track.LedgerError):
                track.load(path)
        self.reject([self.records[0]] * (track.MAX_RECORDS + 1))

    def test_cli_init_and_report_refuse_overwrite_and_errors_do_not_echo_data(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "ledger.jsonl"
            output = Path(directory) / "report.md"
            stdout, stderr = io.StringIO(), io.StringIO()
            with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
                self.assertEqual(track.main(["init", str(path)]), 0)
                self.assertEqual(path.read_bytes(), b"")
                self.assertEqual(track.main(["init", str(path)]), 2)
                path.write_text("\n".join(json.dumps(r) for r in self.records), encoding="utf-8")
                self.assertEqual(track.main(["check", str(path)]), 0)
                self.assertEqual(track.main(["digest", str(path)]), 0)
                self.assertEqual(track.main(["report", str(path), "--output", str(output)]), 0)
                original = output.read_bytes()
                self.assertEqual(track.main(["report", str(path), "--output", str(output)]), 2)
                self.assertEqual(output.read_bytes(), original)
                path.write_text('{"PRIVATE_SECRET":"canary",}', encoding="utf-8")
                self.assertEqual(track.main(["check", str(path)]), 2)
            self.assertNotIn("canary", stderr.getvalue())
            self.assertNotIn(str(path), stderr.getvalue())
            self.assertNotIn("Traceback", stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
