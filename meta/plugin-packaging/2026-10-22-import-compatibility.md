# Account import compatibility — 2026-10-22

Ray installed Plugin Creator and requested account installation of the three
prepared plugins. Resume Workflow remains excluded.

## Newly available requirements and corrections

The installed Plugin Creator 0.1.28 package specifies account-import component
requirements that were not checked in the initial wrapper build:

- Listing shortDescription is at most 30 characters.
- Optional skill policy.products accepts CHAT, CODEX, and HERMES; the standalone
  skill host had written a legacy chatgpt/codex/api/atlas list.
- Plugin listing icons are at least 48 by 48 pixels.

Bumped the package version to 0.1.1, added concise subtitles, omitted only the known
legacy product block from packaged agent metadata, and retained implicit invocation
and all instructional content. Reused the artwork and viewBox at 96 by 96 pixels
for plugin listing icons. Categorized the two learning plugins as Education &
Research. Source skill packages were not modified.

The builder performs a narrow legacy-block transformation, rather than removing all
future product policies. New product restrictions would therefore remain visible for
explicit compatibility review.

## Verification

Executed the builder and --check. Parsed JSON and YAML; checked the exact required
schema URL, matching names and versions, subtitle/display lengths, default-prompt
counts and lengths, accepted category titles, and icon dimensions. Validated the
three bundled skills and local references. Confirmed identical source instruction
files and only the documented product-list difference in agent metadata. Created
three scratch upload archives, inspected their complete inventory including hidden
compatibility manifests, and verified ZIP integrity. Archives are intermediate upload
inputs, not installed plugin records. No account ingestion diagnostics were available.

## Account-save limitation

Plugin Creator's create-plugin skill and package references were loaded, but the
create_plugin tool was absent from the callable tool registry after repeated checks.
No account-save call was made, and no creation response or plugin_url was returned.
The browser fallback could open ChatGPT Plugins, but both DOM inspection routes failed
with Debugger unattached after a recovery attempt. No private account plugin was
created or installed through that route. Account creation/installation is still pending.

This is a missing execution capability, not an approval requirement or a failed
installation by the user. Do not ask the user to reinstall Plugin Creator or claim
the prepared packages are installed. A fresh Plugin Creator conversation is a possible
recovery step; its tool availability must be checked before promising completion.
