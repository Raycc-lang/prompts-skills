# Prompt and learning plugins

The three self-contained packages below contain the current skills and their
supporting references. They need no MCP server or app connection. Installing one
adds its workflow; it does not add shell access, browsing, or other tools.

| Plugin | Package directory | Included skill |
| --- | --- | --- |
| Ray's Prompt Wording | [ray-prompt-wording](../plugins/ray-prompt-wording/) | `ray-prompt-wording` |
| Focused Teaching | [focused-teaching](../plugins/focused-teaching/) | `focused-teaching` |
| Jiangou Learning Analysis | [jiangou-learning-analysis](../plugins/jiangou-learning-analysis/) | `jiangou-learning-analysis` |

Resume Workflow is excluded. Each package contains a portable `plugin.json`, a
Codex compatibility manifest, a complete `skills/<name>/` directory, and its icon.
Only runtime skill resources are bundled; maintenance records stay in `meta/`.

## Use in ChatGPT on the web

Packaging and account installation are separate steps. These repository packages
are not automatically installed in a ChatGPT account.

1. In ChatGPT, select **@Plugin Creator**. It must be installed and available in
   the current workspace.
2. Ask it to create three private plugins from the package directories linked
   above. Supply their GitHub links. Preserve each included `SKILL.md` and all
   supporting references; use the existing manifest name, description, and version.
   No apps or MCP servers are needed. If it cannot retrieve a source, provide the
   package contents rather than having it reconstruct the instructions from a summary.
3. Follow its creation and installation prompts. Then start a new Chat conversation
   and select the relevant plugin with an **@ mention**.
4. Verify a familiar task in Chat. Keep the distinction between prompt wording and
   agent objectives, the explanation-only option in teaching, and the chosen-direction
   boundary in learning analysis.

The Plugin Creator flow and workspace availability are controlled by ChatGPT.
A local marketplace install in a Codex client does not by itself establish that the
plugin has been registered or installed in ChatGPT on the web.

## Local development and Codex clients

The repository catalog is `.agents/plugins/marketplace.json`. In a supported client:

```bash
codex plugin marketplace add Raycc-lang/prompts-skills --ref main
```

Then open the ChatGPT desktop app's Plugins Directory, select the
**Ray's Prompt and Learning Skills** source, and install the desired packages.
This is a local marketplace development route, separate from the web account flow.

## Maintain packages

Edit `skills/<name>/` as the canonical source. Then regenerate and check the packages:

```bash
python scripts/build_plugins.py
python scripts/build_plugins.py --check
```

The three `plugins/<name>/` directories are generated; changes there are overwritten.
Commit the source changes and generated packages together. Bump the package version
in the builder when publishing an updated plugin version. Existing account plugins
need an explicit update; a GitHub push does not update an imported snapshot by itself.

## Official references

- [Build plugins in ChatGPT](https://learn.chatgpt.com/docs/build-plugins)
- [Package your plugin](https://developers.openai.com/plugins/build/plugins)
- [Build skills](https://learn.chatgpt.com/docs/build-skills)
