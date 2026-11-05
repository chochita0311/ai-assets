"""Behavior checks for trusted candidate copies; not a skill-effectiveness score."""

import argparse
import asyncio
import importlib.util
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest


INPUTS = Path(__file__).resolve().parent / "inputs"


def load(path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class Transaction:
    def __init__(self, events, write_error=None, suppress=False, exit_error=None):
        self.events = events
        self.write_error = write_error
        self.suppress = suppress
        self.exit_error = exit_error
        owner = self

        class Connection:
            def write(self, receipt):
                owner.events.append(("write", self, receipt))
                if owner.write_error is not None:
                    raise owner.write_error

        self.connection = Connection()

    def __enter__(self):
        self.events.append("enter")
        return self.connection

    def __exit__(self, kind, error, traceback):
        self.events.append(("exit", error))
        if self.exit_error is not None:
            raise self.exit_error
        return self.suppress


class PricingChecks(unittest.TestCase):
    def call_both(self, rows, region):
        # Each API gets a fresh single-pass iterable; never reuse an exhausted one.
        yield self.subject.preview(iter(rows), region)
        yield self.subject.checkout(iter(rows), region, Transaction([]))

    def test_totals(self):
        for subtotal, local, remote in [(0, "5.00", "15.00"),
                                       (9999, "104.99", "114.99"),
                                       (10000, "90.00", "90.00"),
                                       (10019, "90.18", "90.18")]:
            for region, expected in [("local", local), ("remote", remote)]:
                with self.subTest(subtotal=subtotal, region=region):
                    rows = [{"quantity": 1, "price": subtotal}]
                    self.assertEqual(list(self.call_both(rows, region)), [expected] * 2)
        self.assertEqual(list(self.call_both([], "local")), ["5.00"] * 2)
        rows = [{"quantity": 2, "price": 3000}, {"quantity": 1, "price": 4000}]
        self.assertEqual(list(self.call_both(rows, "remote")), ["90.00"] * 2)

    def test_validation_and_iterator_errors(self):
        for checkout in (False, True):
            for row, kind, args in [({"quantity": -1, "price": -1}, ValueError, ("quantity",)),
                                    ({"quantity": -1}, ValueError, ("quantity",)),
                                    ({"quantity": 1, "price": -1}, ValueError, ("price",)),
                                    ({}, KeyError, ("quantity",)),
                                    ({"quantity": 1}, KeyError, ("price",))]:
                with self.subTest(checkout=checkout, row=row):
                    events = []
                    with self.assertRaises(kind) as caught:
                        if checkout:
                            self.subject.checkout(iter([row]), "invalid", Transaction(events))
                        else:
                            self.subject.preview(iter([row]), "invalid")
                    self.assertEqual(caught.exception.args, args)
                    self.assertEqual(events, [])
            events = []
            error = RuntimeError("iterator failed")

            def failing_rows():
                yield {"quantity": 1, "price": 5}
                raise error

            with self.assertRaises(RuntimeError) as caught:
                if checkout:
                    self.subject.checkout(failing_rows(), "invalid", Transaction(events))
                else:
                    self.subject.preview(failing_rows(), "invalid")
            self.assertIs(caught.exception, error)
            self.assertEqual(events, [])
        for result in (lambda: self.subject.preview(iter([]), "invalid"),
                       lambda: self.subject.checkout(iter([]), "invalid", Transaction([]))):
            with self.assertRaises(ValueError) as caught:
                result()
            self.assertEqual(caught.exception.args, ("region",))

    def test_renderer_and_transaction(self):
        subject = self.subject
        self.assertEqual(subject.money(123), "1.23")
        self.assertEqual(subject.login_key("MiXeD"), "mixed")
        self.assertEqual(subject.display_key("MiXeD"), "mixed")
        original = subject.RENDERER
        events = []

        def renderer(amount):
            events.append(("render", amount))
            return "receipt"

        subject.fixture_renderer = renderer
        subject.RENDERER = "fixture_renderer"
        try:
            self.assertEqual(subject.preview(iter([]), "local"), "receipt")
            self.assertEqual(events, [("render", 500)])
            for suppress in (False, True):
                for fail_write in (False, True):
                    for fail_exit in (False, True):
                        with self.subTest(suppress=suppress, write=fail_write, exit=fail_exit):
                            events.clear()
                            write_error = RuntimeError("write") if fail_write else None
                            exit_error = RuntimeError("exit") if fail_exit else None
                            tx = Transaction(events, write_error, suppress, exit_error)
                            expected = exit_error or (write_error if not suppress else None)
                            if expected is not None:
                                with self.assertRaises(RuntimeError) as caught:
                                    subject.checkout(iter([]), "local", tx)
                                self.assertIs(caught.exception, expected)
                            else:
                                self.assertEqual(subject.checkout(iter([]), "local", tx), "receipt")
                            self.assertEqual(events, [("render", 500), "enter",
                                                      ("write", tx.connection, "receipt"),
                                                      ("exit", write_error)])
            error = RuntimeError("render")

            def broken_renderer(amount):
                raise error

            subject.fixture_renderer = broken_renderer
            events.clear()
            with self.assertRaises(RuntimeError) as caught:
                subject.checkout(iter([]), "local", Transaction(events))
            self.assertIs(caught.exception, error)
            self.assertEqual(events, [])
        finally:
            subject.RENDERER = original
            del subject.fixture_renderer


class PublisherChecks(unittest.IsolatedAsyncioTestCase):
    async def scenario(self, before=(False, 9), after=(False, 9), failure=None):
        events = []
        state = list(before)
        started, resume = asyncio.Event(), asyncio.Event()
        error = RuntimeError("operation")
        release_error = RuntimeError("release")

        async def write():
            events.append("write")
            started.set()
            await resume.wait()
            if failure in ("write", "write+release"):
                raise error

        def mark():
            events.append("mark")
            if failure == "mark":
                raise error

        async def release():
            # A suspension proves cleanup was awaited before the result escapes.
            await asyncio.sleep(0)
            events.append("release")
            if failure in ("release", "write+release", "cancel+release"):
                raise release_error

        task = asyncio.create_task(self.subject.publish(
            lambda: state[0], lambda: state[1], 10, write, mark, release))
        if not before[0] and before[1] < 10:
            await asyncio.wait_for(started.wait(), 2)
            state[:] = after
            if failure in ("cancel", "cancel+release"):
                task.cancel()
            resume.set()
        expected_error = (release_error if failure in ("release", "write+release", "cancel+release")
                          else error if failure in ("write", "mark") else None)
        if expected_error is not None:
            with self.assertRaises(RuntimeError) as caught:
                await asyncio.wait_for(task, 2)
            self.assertIs(caught.exception, expected_error)
        elif failure == "cancel":
            with self.assertRaises(asyncio.CancelledError):
                await asyncio.wait_for(task, 2)
        else:
            result = await asyncio.wait_for(task, 2)
            self.assertIs(result, not (before[0] or before[1] >= 10 or after[0] or after[1] >= 10))
        expected_events = []
        if not before[0] and before[1] < 10:
            expected_events.append("write")
            if failure not in ("write", "write+release", "cancel", "cancel+release") and not after[0] and after[1] < 10:
                expected_events.append("mark")
        self.assertEqual(events, expected_events + ["release"])

    async def test_state_and_deadline(self):
        for before in [(False, 9), (False, 10), (False, 11), (True, 9)]:
            for after in [(False, 9), (False, 10), (False, 11), (True, 9)]:
                with self.subTest(before=before, after=after):
                    await self.scenario(before, after)

    async def test_failures_and_cancellation(self):
        for failure in ["write", "mark", "release", "write+release", "cancel", "cancel+release"]:
            with self.subTest(failure=failure):
                await self.scenario(failure=failure)
        await self.scenario(before=(True, 9), failure="release")


def check(candidate, stream):
    sys.path.insert(0, str(candidate))
    try:
        PricingChecks.subject = load(candidate / "pricing.py")
        PublisherChecks.subject = load(candidate / "publish.py")
        suite = unittest.TestSuite(unittest.defaultTestLoader.loadTestsFromTestCase(cls)
                                   for cls in (PricingChecks, PublisherChecks))
        return unittest.TextTestRunner(stream=stream, verbosity=2).run(suite)
    finally:
        sys.path.pop(0)


def self_test():
    """Check oracle sensitivity with valid cleanups and targeted bad edits."""
    pricing = (INPUTS / "pricing.py").read_text()
    publisher = (INPUTS / "publish.py").read_text()
    start = pricing.index("def _checkout_total(")
    end = pricing.index("def preview(")
    cleaned = (pricing[:start] + pricing[end:]).replace("_checkout_total", "_preview_total")
    cleaned = cleaned.replace("return _forward(globals()[RENDERER](_preview_total(rows, region)))",
                              "return globals()[RENDERER](_preview_total(rows, region))")
    module_lookup = "import sys\n\n" + cleaned.replace(
        "globals()[RENDERER]", "getattr(sys.modules[__name__], RENDERER)")
    guard = "        if stopping() or clock() >= deadline:\n            return False\n"
    mutants = [
        ("missing runtime renderer", pricing.replace("def money(", "def lost_money("), publisher,
         "test_renderer_and_transaction"),
        ("wrong transaction ordering", pricing.replace(
            "    receipt = globals()[RENDERER](_checkout_total(rows, region))\n    with transaction as connection:\n",
            "    with transaction as connection:\n        receipt = globals()[RENDERER](_checkout_total(rows, region))\n"),
         publisher, "test_renderer_and_transaction"),
        ("eager field lookup", pricing.replace("    for row in rows:\n",
            '    for row in rows:\n        quantity, price = row["quantity"], row["price"]\n'),
         publisher, "test_validation_and_iterator_errors"),
        ("missing later guard", pricing, publisher.replace("        await write()\n" + guard,
                                                            "        await write()\n"),
         "test_state_and_deadline"),
        ("wrong equality boundary", pricing, publisher.replace(">= deadline", "> deadline"),
         "test_state_and_deadline"),
        ("unawaited release", pricing, publisher.replace("        await release()", "        pass"),
         "test_failures_and_cancellation"),
        ("blocked finalization", pricing,
         "import asyncio\n\n"
         "async def publish(stopping, clock, deadline, write, mark_complete, release):\n"
         "    try:\n        await write()\n        await asyncio.Event().wait()\n"
         "    finally:\n        await asyncio.Event().wait()\n", "timeout"),
    ]
    with tempfile.TemporaryDirectory(prefix="clean-code-regression-") as directory:
        candidate = Path(directory)
        for label, price_source, publish_source, expected_failure in [
                ("baseline", pricing, publisher, None),
                ("valid cleanup", cleaned, publisher, None),
                ("valid module lookup", module_lookup, publisher, None)] + mutants:
            (candidate / "pricing.py").write_text(price_source)
            (candidate / "publish.py").write_text(publish_source)
            result = run_checks(candidate, timeout=3 if expected_failure == "timeout" else 15)
            if expected_failure == "timeout":
                valid = result.returncode == 124
            elif expected_failure is None:
                valid = result.returncode == 0
            else:
                valid = result.returncode == 1 and re.search(
                    r"^(?:FAIL|ERROR): " + expected_failure + r"\b", result.stdout, re.MULTILINE)
            if not valid:
                raise AssertionError(label + "\n" + result.stdout + result.stderr)
            print(label + ": expected result observed")


def run_checks(candidate, timeout=15):
    command = [sys.executable, "-B", str(Path(__file__).resolve()),
               "--worker", "--candidate", str(candidate)]
    try:
        return subprocess.run(command, capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired as error:
        # subprocess.run kills and waits for this worker before returning here.
        output = error.stdout or b""
        if isinstance(output, bytes):
            output = output.decode(errors="replace")
        return subprocess.CompletedProcess(command, 124,
            output + f"\nBehavior-check process exceeded {timeout} seconds and was terminated.\n", "")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--candidate", type=Path, help="trusted directory containing both modules")
    group.add_argument("--self-test", action="store_true", help="exercise valid and invalid controls")
    parser.add_argument("--worker", action="store_true", help=argparse.SUPPRESS)
    args = parser.parse_args()
    # Repeated control imports must not reuse timestamp-based bytecode.
    sys.dont_write_bytecode = True
    if args.self_test:
        self_test()
        return 0
    candidate = (args.candidate or INPUTS).resolve()
    if not args.worker:
        result = run_checks(candidate)
        print(result.stdout, end="")
        print(result.stderr, end="", file=sys.stderr)
        return result.returncode
    result = check(candidate, sys.stdout)
    print("Behavior checks only; structure, authority, and routing still need review.")
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(main())
