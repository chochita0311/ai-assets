# Codex Reset Alert

A small macOS utility that checks a public reset tracker and posts a local
notification when a new signal is recorded. It uses only Python's standard
library and AppleScript; it does not start Codex, read account credentials, or
inspect a personal usage allowance.

The source is the unauthenticated, read-only `GET /api/v1/status` endpoint of
the [Codex Resets API](https://codex-resets.com/api/docs), an independent
third-party service. Its data is not an OpenAI commitment, and its
collection, classification, availability, and API format can change. It
tracks public posts by Tibo (`@thsottiaux`) and can also record observed
events. An HTTP request exposes normal network metadata, including the
requester's IP address, to that service.

The provider asks users to link to [Codex Resets](https://codex-resets.com/)
where its data is displayed. The compact notification text does not include a
source link; the provider and API documentation are linked here instead.

## What an alert means

This tool watches public reset signals, not the personal seven-day refresh
displayed by Codex. Automatic resets apply only to the accounts and limits
selected for an offer; a banked reset is a separate grant that a user may apply
later. Check the announcement and the account's own usage display for scope and
actual application. [OpenAI's reset documentation](https://help.openai.com/en/articles/20001498-how-resets-work-in-codex)
describes the distinction.

In a reported automatic reset, OpenAI replaced the previous allowance window,
including its unused balance, and changed the next weekly refresh. Advance
signals can help a user plan around such an event, but they do not guarantee
advance notice or application to a particular account. See [OpenAI support's explanation](https://community.openai.com/t/questions-about-an-unexpected-codex-usage-reset-and-new-quota-period/1382610).

| API signal | Notification | Interpretation |
|---|---|---|
| Scheduled regular reset with non-null `scheduled_for` | `Codex Reset` and the formatted time | The time supplied by the tracker; it may represent a deadline, not the precise moment of application. |
| Scheduled regular reset with `scheduled_for: null` | `Codex Reset` and `시각 미정` | A time was not supplied. |
| Scheduled banked reset | Time or `시각 미정`, followed by `(리셋권)` | A reset grant, not necessarily an immediate refresh. |
| Active watch | `시각 미정 (가능성)` | A third-party possibility signal, not a confirmed schedule. |
| New latest reset | Announcement or observation time followed by `(확인)` or `(리셋권 확인)` | The recorded time is not necessarily when an individual account changed. |

For example, a scheduled signal can show the title `Codex Reset` and the body
`01/01 11:55 KST`; this is an illustrative time, not a real announcement.

The site's `scheduled_for` is not proof of completion, even after it passes.
The watch's expiry is not a reset time. A scheduled reset must contain
`scheduled_for`, even if its value is null. A missing required field makes the
response invalid; the tool does not invent a reset time.

A regular check initiates one API status request; HTTP redirects can cause
additional requests. On the first valid API response, it silently baselines the
existing latest reset; once state is saved, this
baseline persists even if a later event notification fails. A scheduled reset
or an unexpired watch can still notify. Later checks notify for unrecorded reset
identities or scheduled times, a new active-watch source and level combination,
and a change between a regular and banked classification even when the reset
identity and time are unchanged. A watch uses its source URL when available,
otherwise its text or `unknown` if both are empty, together with its level for
deduplication.

The same unchanged schedule does not generate a reminder every hour. A check
can also report a new latest reset or an API failure or recovery, so alerts are
not limited to upcoming schedules.

For an already classified key, a type change is recorded only after its
notification succeeds. A failed event notification is eligible for retry on a
later valid check if the same signal is still present and eligible; there is no
pending-notification queue. State retains up to 100 distinct event keys; an
evicted key can notify again if it reappears. When upgrading old state that
did not record classifications, the first observed type for an existing key
is saved silently. A classification change made before that observation cannot
be detected retrospectively.

An hourly check can miss a short-lived announcement, and neither a quiet tracker
nor a successful request proves that no announcement exists. Completion may
reach an account before a public confirmation.

## Requirements and ownership

- macOS with a logged-in GUI user, Python 3.9 or newer, network access, and
  permission for AppleScript notifications. Depending on macOS, notifications
  can be attributed to Script Editor; enable its desktop banner or alert style
  and check Focus settings if they only appear in Notification Center.
- Choose a dedicated absolute state directory **outside the checkout**. When
  source checkouts can be detected, the monitor rejects state paths inside its
  checkout, and the renderer rejects state and output paths inside either its
  own checkout or the selected monitor's checkout. Detection resolves symbolic
  links and requires a `.git` file or directory in an ancestor; keep paths
  outside the checkout even when detection is unavailable. The directory
  holds `state.json`, `monitor.lock`, `monitor.log`, and, after rotation,
  `monitor.log.1` and `monitor.log.2`. State is replaced through a temporary
  `.state-...` file; an interrupted process can leave that temporary file.
  The log rotates at approximately 256 KiB per file with two backups.
- A LaunchAgent is a machine-local installation, not a repository artifact.
  The renderer below produces a candidate only; it does not install, load,
  overwrite, or migrate a job. Resolve any existing job and its state before
  choosing an installation destination.
- The monitor's display time zone defaults to the machine's local zone. Use
  `--timezone` with an installed IANA zone, for example `Asia/Seoul`, to pin
  display times. This option does not change the system time zone or
  `launchd`'s calendar schedule.

## Test and install

Replace each quoted placeholder with an appropriate absolute path or label.
Do not put generated plists, state, or logs in the source checkout.
Run the repository-relative commands below from the checkout's root; if the
package was copied elsewhere, adjust those paths to its location.

To use the tool on another Mac, make this package available there and perform
the local setup below, including notification permission and job installation.
Asking an agent to import it is not itself an installation; the agent needs
access to the package and must be able to perform those steps on that Mac.

1. Test the notification channel. The displayed time is **simulated**: it is
   two hours after the test, not an actual reset. This test does not query the
   API or write state.

   ```sh
   python3 tools/codex/reset-alert/reset_alert.py --test --timezone Asia/Seoul
   ```

   A successful command only means macOS accepted the notification request;
   verify that the banner is actually visible.

2. Select an absolute path to the monitor and a dedicated state directory.
   Run one real check and inspect the result before scheduling it:

   ```sh
   python3 '<absolute-monitor-path>' \
     --state-dir '<absolute-state-directory>' \
     --timezone Asia/Seoul
   ```

   If the monitor is run from a checkout, that checkout must remain at the
   same path for a scheduled job. A copied monitor is independent of the
   repository and does not update when repository source changes.

3. Render a candidate LaunchAgent to a new absolute path outside both the
   renderer's and the selected monitor's checkouts. The Python executable and
   monitor must exist; the renderer validates the label and optional time zone
   and refuses to overwrite an existing output file. `--monitor` can be omitted
   to use this checkout's monitor.

   ```sh
   python3 tools/codex/reset-alert/render_launch_agent.py \
     --python '<absolute-python-executable>' \
     --monitor '<absolute-monitor-path>' \
     --state-dir '<absolute-state-directory>' \
     --timezone Asia/Seoul \
     --label '<job-label>' \
     --output '<absolute-candidate-plist>'

   plutil -lint '<absolute-candidate-plist>'
   plutil -p '<absolute-candidate-plist>'
   ```

4. Review the candidate's paths, label, state directory, and schedule. After
   ensuring the destination and label do not belong to another job, copy the
   validated candidate without overwriting an existing file to
   `~/Library/LaunchAgents/<job-label>.plist`. Then load and inspect it:

   ```sh
   launchctl bootstrap "gui/$(id -u)" "$HOME/Library/LaunchAgents/<job-label>.plist"
   launchctl print "gui/$(id -u)/<job-label>"
   launchctl kickstart "gui/$(id -u)/<job-label>"
   ```

   Inspect `monitor.log` in the selected state directory after the forced
   run. The short-lived job may show as not running between checks; the
   calendar trigger must remain registered. A user LaunchAgent is active in
   the logged-in GUI session.

The generated job uses `StartCalendarInterval` with `Minute` set to `0`, so
it checks on each hour according to the Mac's local clock. During sleep,
missed calendar events are coalesced when the machine wakes; it cannot provide
real-time checks while the machine is asleep or powered off. The time-zone
option controls only notification text.

To unload the job for the current session, use the exact installed plist:

```sh
launchctl bootout "gui/$(id -u)" "$HOME/Library/LaunchAgents/<job-label>.plist"
```

An installed plist may be loaded again at login. If removing an installation,
first verify ownership and unload the job; remove only its own plist and
runtime files when they are no longer needed.

## Failure handling

HTTP status and protocol errors (including truncated chunked or declared-length
responses), connection and timeout errors, and invalid API response JSON or
recognized API schema errors increment the consecutive API-failure count and
are logged. The first two only write to the log and state; the third attempts
an error notification. If that
request fails, later failed checks retry it. After a successful notification
request, further failures do not repeat it. A later valid check attempts a
recovery notification if the error notification was recorded; a failed recovery
notification is retried on a subsequent valid check.
At an hourly cadence, the first error notification can arrive roughly two to
three hours after an outage begins, or later if the Mac is asleep.

Failures loading local state are outside the API-failure counter. This does not
guarantee notification for failures that prevent the script, state directory,
log, or macOS notification service from working. Check the local log and
LaunchAgent status when expected alerts do not arrive.

## Verify the package

The checks use synthetic events and temporary state; they do not call the API
or post notifications:

```sh
python3 -B -m unittest discover -s tools/codex/reset-alert/tests -p 'test_*.py'
```
