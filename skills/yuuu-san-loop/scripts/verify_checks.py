"""Run and verify a frozen list of executable acceptance checks."""

import argparse
import hashlib
import json
import os
from pathlib import Path
import platform
import shutil
import subprocess
import sys


NODE_REPORTER = Path(__file__).resolve().with_name("node_test_reporter.mjs")


def require(condition, message):
    if not condition:
        raise ValueError(message)


def valid_text(value):
    return isinstance(value, str) and bool(value.strip())


def unique_keys(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, f"Duplicate JSON key: {key}")
        result[key] = value
    return result


def load_plan(path):
    raw = path.read_bytes()
    plan = json.loads(raw, object_pairs_hook=unique_keys)
    require(isinstance(plan, dict) and set(plan) == {"checks"}, "Plan must contain checks")
    checks = plan["checks"]
    require(isinstance(checks, list) and checks, "At least one check is required")
    ids = set()
    for check in checks:
        required = {"id", "argv", "report", "timeout_seconds"}
        optional = {"cases", "os"}
        require(isinstance(check, dict) and required <= check.keys() <= required | optional,
                "Invalid check fields")
        check_id = check["id"]
        require(valid_text(check_id) and check_id not in ids, "Check IDs must be unique")
        ids.add(check_id)
        argv = check["argv"]
        require(isinstance(argv, list) and argv and valid_text(argv[0])
                and all(isinstance(arg, str) and "\0" not in arg for arg in argv),
                f"{check_id}: invalid argv")
        require(type(check["timeout_seconds"]) is int and check["timeout_seconds"] > 0,
                f"{check_id}: timeout_seconds must be a positive integer")
        require("os" not in check or valid_text(check["os"]), f"{check_id}: invalid os")
        report = check["report"]
        require(report in ("exit", "node-test"), f"{check_id}: expected report exit or node-test")
        if report == "exit":
            require("cases" not in check, f"{check_id}: cases require a node-test report")
            continue
        require("--test" in argv[1:] and not any(arg.startswith("--test-reporter") for arg in argv[1:]),
                f"{check_id}: use Node --test without a custom reporter")
        cases = check.get("cases")
        require(isinstance(cases, list) and cases and all(
            isinstance(case, list) and case and all(valid_text(part) for part in case) for case in cases
        ), f"{check_id}: Node test checks require named cases")
        require(len(set(map(tuple, cases))) == len(cases), f"{check_id}: duplicate required case")
    return checks, hashlib.sha256(raw).hexdigest()


def git(repo, *args):
    result = subprocess.run(["git", "-c", "core.fsmonitor=false", "-C", str(repo), *args],
                            capture_output=True, check=True)
    return result.stdout


def worktree_root(repo):
    return Path(git(repo, "rev-parse", "--show-toplevel").decode("utf-8").strip()).resolve()


def clean_commit(repo):
    require(git(repo, "rev-parse", "--is-inside-work-tree").strip() == b"true",
            "An active Git worktree is required")
    require(not git(repo, "status", "--porcelain=v1", "--untracked-files=all", "--ignore-submodules=none"),
            "Use a clean candidate worktree")
    tracked = git(repo, "ls-files", "-v", "-z", "--recurse-submodules")
    require(not any(entry[:1] == b"S" or entry[:1].islower() for entry in tracked.split(b"\0")),
            "Tracked entries hide worktree changes (skip-worktree or assume-unchanged)")
    return git(repo, "rev-parse", "--verify", "HEAD^{commit}").strip().decode("ascii")


def digest(path):
    require(path.is_file() and not path.is_symlink(), f"Missing or linked evidence file: {path.name}")
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def executable(program, repo):
    if "/" not in program and "\\" not in program and not Path(program).drive:
        located = shutil.which(program)
        if located is None:
            raise FileNotFoundError(program)
        return Path(located).resolve(strict=True)
    path = Path(program)
    require(not path.drive or path.is_absolute(), "Drive-relative executable path")
    return (repo / path).resolve(strict=True)


def node_cases(path):
    with path.open(encoding="utf-8") as stream:
        rows = [json.loads(line, object_pairs_hook=unique_keys) for line in stream]
    require(len(rows) >= 2 and all(isinstance(row, dict) for row in rows)
            and rows[0] == {"kind": "header", "schema": 1}
            and rows[-1].get("kind") == "summary", "Incomplete Node test report")
    summary = rows[-1]
    counts = summary.get("counts")
    metrics = ("tests", "passed", "suites", "failed", "cancelled", "skipped", "todo")
    require(isinstance(counts, dict) and all(type(counts.get(key)) is int and counts[key] >= 0
                                            for key in metrics), "Invalid Node test summary")
    require(summary.get("success") is True and counts["passed"] == counts["tests"] > 0
            and not any(counts[key] for key in ("failed", "cancelled", "skipped", "todo")),
            "Node test run includes an unpassed test or ran no tests")
    found = set()
    observed = {"test": 0, "suite": 0, "file": 0}
    for row in rows[1:-1]:
        kind = row.get("kind")
        if kind == "output":
            continue
        require(isinstance(kind, str) and kind in observed and row.get("status") == "passed",
                "Unexpected or unpassed Node test result")
        observed[kind] += 1
        if kind == "test":
            parts = row.get("path")
            require(isinstance(parts, list) and parts and all(valid_text(part) for part in parts),
                    "Invalid Node test case path")
            case = tuple(parts)
            require(case not in found, f"Ambiguous Node test case: {' / '.join(case)}")
            found.add(case)
    require(observed["test"] + observed["file"] == counts["tests"]
            and observed["suite"] == counts["suites"], "Node summary does not match recorded results")
    return found


def evidence_paths(directory, index):
    return directory / f"{index:03}.stdout", directory / f"{index:03}.stderr"


def run(checks, plan_hash, repo, directory):
    root = worktree_root(repo)
    require(not directory.is_relative_to(root), "Store evidence outside the candidate worktree")
    candidate = clean_commit(root)
    directory.mkdir(mode=0o700, exist_ok=False)
    system = platform.system()
    results = []
    for index, check in enumerate(checks, 1):
        require(clean_commit(root) == candidate, "Candidate changed during the run")
        stdout, stderr = evidence_paths(directory, index)
        row = {"id": check["id"], "executable": None, "exit_code": None, "run_error": None}
        with stdout.open("xb") as output, stderr.open("xb") as errors:
            if "os" in check and system != check["os"]:
                row["run_error"] = f"Requires {check['os']}, running on {system}"
            else:
                try:
                    resolved = executable(check["argv"][0], root)
                    row["executable"] = str(resolved)
                    argv = [str(resolved), *check["argv"][1:]]
                    if check["report"] == "node-test":
                        argv.insert(1, "--test-reporter=" + NODE_REPORTER.as_uri())
                    row["exit_code"] = subprocess.run(
                        argv, cwd=root, stdin=subprocess.DEVNULL,
                        stdout=output, stderr=errors, timeout=check["timeout_seconds"],
                    ).returncode
                except subprocess.TimeoutExpired:
                    row["run_error"] = "Timed out"
                except (ValueError, OSError) as error:
                    row["run_error"] = f"Could not start command: {error}"
        row.update(stdout_sha256=digest(stdout), stderr_sha256=digest(stderr))
        results.append(row)
    require(clean_commit(root) == candidate, "Candidate changed during the run")
    record = {
        "schema": 1, "plan_sha256": plan_hash, "commit": candidate, "worktree": str(root),
        "os": system, "checks": results,
    }
    with (directory / "run.json").open("x", encoding="utf-8") as stream:
        json.dump(record, stream, ensure_ascii=False, indent=2)
        stream.write("\n")


def verify(checks, plan_hash, repo, directory):
    root = worktree_root(repo)
    candidate = clean_commit(root)
    record_path = directory / "run.json"
    require(record_path.is_file() and not record_path.is_symlink(), "No complete run record")
    record_bytes = record_path.read_bytes()
    record = json.loads(record_bytes, object_pairs_hook=unique_keys)
    require(isinstance(record, dict) and type(record.get("schema")) is int
            and record["schema"] == 1, "Invalid run record")
    require(record.get("plan_sha256") == plan_hash, "Run used a different plan")
    require(record.get("worktree") == str(root), "Run used a different worktree")
    require(record.get("commit") == candidate, "Run used a different candidate")
    require(valid_text(record.get("os")), "Run environment is missing")
    rows = record.get("checks")
    require(isinstance(rows, list) and all(isinstance(row, dict) for row in rows)
            and [row.get("id") for row in rows] == [check["id"] for check in checks],
            "Missing, duplicate or unexpected check results")
    failures = []
    for index, (check, row) in enumerate(zip(checks, rows), 1):
        try:
            stdout, stderr = evidence_paths(directory, index)
            require(digest(stdout) == row.get("stdout_sha256")
                    and digest(stderr) == row.get("stderr_sha256"), "Evidence hash mismatch")
            require("os" not in check or check["os"] == record["os"],
                    f"Requires {check.get('os')}, ran on {record['os']}")
            require("run_error" in row and row["run_error"] is None,
                    row.get("run_error") or "Execution result is missing")
            require(valid_text(row.get("executable")), "Executed command was not recorded")
            require(type(row.get("exit_code")) is int and row["exit_code"] == 0,
                    f"Command did not exit successfully ({row.get('exit_code')})")
            if check["report"] == "node-test":
                observed = node_cases(stdout)
                missing = sorted(set(map(tuple, check["cases"])) - observed)
                require(not missing, "Missing Node test cases: " + ", ".join(" / ".join(case) for case in missing))
        except (OSError, ValueError) as error:
            failures.append(f"{check['id']}: {error}")
    require(not failures, "\n".join(failures))
    require(clean_commit(root) == candidate, "Candidate changed during verification")
    return {"status": "passed", "scope": "executable-checks", "commit": candidate,
            "plan_sha256": plan_hash, "run_sha256": hashlib.sha256(record_bytes).hexdigest(),
            "checks": [check["id"] for check in checks]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    actions = parser.add_subparsers(dest="action", required=True)
    actions.add_parser("freeze", help="Validate a plan and print its SHA-256").add_argument("plan", type=Path)
    for action in ("run", "verify"):
        command = actions.add_parser(action)
        command.add_argument("plan", type=Path)
        command.add_argument("plan_sha256", help="Hash recorded before the checks ran")
        command.add_argument("repo", type=Path)
        command.add_argument("evidence", type=Path)
    args = parser.parse_args()
    try:
        checks, plan_hash = load_plan(args.plan)
        if args.action == "freeze":
            print(plan_hash)
            return 0
        require(plan_hash == args.plan_sha256.lower(), "Plan differs from the frozen hash")
        repo, directory = args.repo.resolve(strict=True), args.evidence.resolve()
        if args.action == "run":
            run(checks, plan_hash, repo, directory)
        print(json.dumps(verify(checks, plan_hash, repo, directory), ensure_ascii=True))
        return 0
    except (ValueError, OSError, subprocess.CalledProcessError) as error:
        print(f"Acceptance checks not passed: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    os.umask(0o077)
    sys.exit(main())
