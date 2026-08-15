# -*- coding: utf-8 -*-
"""Browser reading workflow: select words, learn from SMD output, then deep-read."""

import argparse
import datetime
import html
import json
import os
import re
import socket
import subprocess
import sys
import threading
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(SCRIPT_DIR)
READING_DIR = os.path.join(ROOT, "reading")
SMD_PATH = os.path.join(SCRIPT_DIR, "smd.py")
WORD_RE = re.compile(r"[A-Za-z][a-zA-Z'-]*[a-zA-Z]|[A-Za-z]")
SENT_END = (".", "!", "?", "。", "！", "？")
MAX_SUBMIT_BYTES = 64 * 1024


class SubmissionInProgressError(RuntimeError):
    pass


def resolve_day_dir(day=None):
    if day:
        path = os.path.join(READING_DIR, day)
        if not os.path.isdir(path):
            sys.exit(f"目录不存在: {path}")
        return path
    today = os.path.join(READING_DIR, datetime.date.today().isoformat())
    if os.path.isfile(os.path.join(today, "article.txt")):
        return today
    if os.path.isdir(READING_DIR):
        for name in sorted(os.listdir(READING_DIR), reverse=True):
            path = os.path.join(READING_DIR, name, "article.txt")
            if os.path.isfile(path):
                print(f"今天没有 article.txt，使用最近的: {name}")
                return os.path.join(READING_DIR, name)
    sys.exit("没有找到 article.txt。先跑 python tools/prep.py 备料")


def source_sentence(text, start, end):
    left = start
    while left > 0 and text[left - 1] not in SENT_END and text[left - 1] != "\n":
        left -= 1
    right = end
    while right < len(text) and text[right] not in SENT_END and text[right] != "\n":
        right += 1
    if right < len(text) and text[right] in SENT_END:
        right += 1
    return " ".join(text[left:right].split())


def inline_markdown(value):
    safe = html.escape(value, quote=False)
    safe = re.sub(r"&lt;u&gt;(.*?)&lt;/u&gt;", r"<u>\1</u>", safe, flags=re.I)
    safe = re.sub(r"`([^`]+)`", r"<code>\1</code>", safe)
    safe = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", safe)
    safe = re.sub(r"__([^_]+)__", r"<strong>\1</strong>", safe)
    safe = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", safe)
    safe = re.sub(r"(?<!_)_([^_]+)_(?!_)", r"<em>\1</em>", safe)
    return safe


def split_table_row(line):
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def is_table_separator(line):
    cells = split_table_row(line)
    return bool(cells) and all(re.fullmatch(r":?-{3,}:?", cell) for cell in cells)


def markdown_to_html(markdown):
    """Render the Markdown subset used by SMD, escaping all raw HTML."""
    lines = markdown.splitlines()
    blocks = []
    paragraph = []
    list_type = None
    i = 0

    def flush_paragraph():
        nonlocal paragraph
        if paragraph:
            blocks.append("<p>" + "<br>".join(inline_markdown(x) for x in paragraph) + "</p>")
            paragraph = []

    def close_list():
        nonlocal list_type
        if list_type:
            blocks.append(f"</{list_type}>")
            list_type = None

    while i < len(lines):
        raw = lines[i]
        line = raw.strip()
        if not line:
            flush_paragraph()
            close_list()
            i += 1
            continue
        if line.startswith("|") and i + 1 < len(lines) and is_table_separator(lines[i + 1]):
            flush_paragraph()
            close_list()
            headers = split_table_row(line)
            i += 2
            rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                rows.append(split_table_row(lines[i]))
                i += 1
            head = "".join(f"<th scope=\"col\">{inline_markdown(cell)}</th>" for cell in headers)
            body = "".join("<tr>" + "".join(f"<td>{inline_markdown(cell)}</td>" for cell in row) + "</tr>" for row in rows)
            blocks.append(f'<div class="table-wrap"><table><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>')
            continue
        if line == "---":
            flush_paragraph()
            close_list()
            blocks.append("<hr>")
            i += 1
            continue
        heading = re.match(r"^(#{1,6})\s+(.*)$", line)
        if heading:
            flush_paragraph()
            close_list()
            level = min(len(heading.group(1)), 4)
            blocks.append(f"<h{level}>{inline_markdown(heading.group(2))}</h{level}>")
            i += 1
            continue
        quote = re.match(r"^>\s?(.*)$", line)
        if quote:
            flush_paragraph()
            close_list()
            quoted = []
            while i < len(lines) and re.match(r"^\s*>\s?", lines[i]):
                quoted.append(re.sub(r"^\s*>\s?", "", lines[i]))
                i += 1
            blocks.append("<blockquote>" + markdown_to_html("\n".join(quoted)) + "</blockquote>")
            continue
        item = re.match(r"^[-*+]\s+(.*)$", line)
        ordered = re.match(r"^\d+[.)]\s+(.*)$", line)
        if item or ordered:
            flush_paragraph()
            wanted = "ul" if item else "ol"
            if list_type != wanted:
                close_list()
                blocks.append(f"<{wanted}>")
                list_type = wanted
            blocks.append(f"<li>{inline_markdown((item or ordered).group(1))}</li>")
            i += 1
            continue
        close_list()
        paragraph.append(line)
        i += 1
    flush_paragraph()
    close_list()
    return "\n".join(blocks)


ANSWER_HEADING_RE = re.compile(r"^\s*#{1,6}\s+.*answer\s*key\s*$", re.I)
ITEM_RE = re.compile(r"^\s*(?:\*\*|__)?([VJS]\d+)[.:]?(?:\*\*|__)?[.:]?\s*(.*)$", re.I)
ANSWER_ITEM_RE = re.compile(r"^\s*(?:\*\*|__)?([VJS]\d+)\s*[—–-]\s*(.*?)(?:\*\*|__)?\s*$", re.I)


def split_answer_key(markdown):
    lines = markdown.splitlines()
    for index, line in enumerate(lines):
        if ANSWER_HEADING_RE.match(line):
            return lines[:index], lines[index + 1:]
    return lines, []


def answer_token(label, text):
    kind = label[0]
    patterns = {
        "V": r"\b(Yes|No)\b",
        "J": r"\b(Unnatural|Yes|No)\b",
        "S": r"(?:^|[—–-]\s*|\b)([NMSE])(?:\b|\s*[—–-])",
    }
    match = re.search(patterns[kind], text, re.I)
    return match.group(1).title() if match else ""


def parse_answers(lines):
    answers = {}
    current = None
    buffer = []

    def save():
        if not current:
            return
        text = "\n".join(buffer).strip()
        answers[current] = {
            "answer": answer_token(current, text),
            "explanation_html": markdown_to_html(text),
        }

    for line in lines:
        match = ANSWER_ITEM_RE.match(line.strip())
        if match:
            save()
            current = match.group(1).upper()
            buffer = [match.group(2)]
        elif current and line.strip() != "---" and not re.match(r"^#{1,6}\s+", line.strip()):
            buffer.append(line)
    save()
    return answers


def render_learning_content(markdown):
    """Render all non-answer content and replace each practice item in place."""
    body_lines, answer_lines = split_answer_key(markdown)
    answers = parse_answers(answer_lines)
    questions = []
    output = []
    plain = []
    i = 0

    def flush_plain():
        nonlocal plain
        if plain:
            output.append(markdown_to_html("\n".join(plain)))
            plain = []

    while i < len(body_lines):
        match = ITEM_RE.match(body_lines[i].strip())
        if not match:
            plain.append(body_lines[i])
            i += 1
            continue
        label = match.group(1).upper()
        flush_plain()
        prompt_lines = [match.group(2)] if match.group(2) else []
        i += 1
        while i < len(body_lines):
            next_line = body_lines[i].strip()
            if ITEM_RE.match(next_line) or re.match(r"^###\s+", next_line):
                break
            prompt_lines.append(body_lines[i])
            i += 1
        while prompt_lines and not prompt_lines[-1].strip():
            prompt_lines.pop()
        while prompt_lines and prompt_lines[-1].strip() == "---":
            prompt_lines.pop()
        kind = label[0]
        answer = answers.get(label, {"answer": "", "explanation_html": ""})
        question = {
            "id": label,
            "prompt_html": markdown_to_html("\n".join(prompt_lines)),
            "options": {"V": ["Yes", "No"], "J": ["Yes", "No", "Unnatural"], "S": ["N", "M", "S", "E"]}[kind],
            **answer,
        }
        questions.append(question)
        output.append(f'<div class="quiz-slot" data-quiz-id="{label}"></div>')
    flush_plain()
    return "\n".join(output), questions


def article_html(text, selectable=True):
    parts, pos = [], 0
    for match in WORD_RE.finditer(text):
        parts.append(html.escape(text[pos:match.start()]))
        word = match.group(0)
        if selectable:
            sentence = source_sentence(text, match.start(), match.end())
            parts.append(f'<span class="w" data-word="{html.escape(word, quote=True)}" '
                         f'data-lower="{html.escape(word.lower(), quote=True)}" '
                         f'data-sent="{html.escape(sentence, quote=True)}">{html.escape(word)}</span>')
        else:
            parts.append(html.escape(word))
        pos = match.end()
    parts.append(html.escape(text[pos:]))
    body = "".join(parts)
    return "".join(f"<p>{p.replace(chr(10), '<br>')}</p>" for p in body.split("\n\n") if p.strip())


PAGE_CSS = r"""
:root { color-scheme:light dark; --ink:#20252b; --paper:#fff; --muted:#6b7280; --line:#d9dde3; --accent:#2563eb; --soft:#f3f5f8; --success:#e3f6ea; --success-ink:#11643b; --error:#fde8e8; --error-ink:#8b2525; }
* { box-sizing:border-box; }
body { margin:0; background:var(--paper); color:var(--ink); font-family:Georgia,'Times New Roman',serif; }
@media (prefers-color-scheme:dark) { :root { --ink:#e8eaf0; --paper:#17191e; --muted:#a8afbb; --line:#363b45; --soft:#22262e; --success:#173d2b; --success-ink:#a9ebc7; --error:#482323; --error-ink:#ffc2c2; } }
.layout { display:grid; grid-template-columns:minmax(96px,1fr) minmax(0,900px) 300px; min-height:100vh; }
#article { grid-column:2; width:100%; padding:44px 48px 140px; font-size:19px; line-height:1.85; }
#article p { margin:0 0 1.2em; }
.w { cursor:pointer; border-radius:3px; padding:0 2px; transition:background .12s; }
.w:hover { background:rgba(59,130,246,.22); }
.w.sel { background:#ffd54a; color:#111; }
#sidebar { grid-column:3; width:300px; padding:22px 16px; border-left:1px solid var(--line); position:sticky; top:49px; height:calc(100vh - 49px); overflow-y:auto; font-family:ui-sans-serif,system-ui,sans-serif; }
#sidebar h2 { font-size:15px; margin:0 0 12px; }
#count { font-weight:700; }
.sel-item { background:var(--soft); border-radius:8px; padding:8px 10px; margin-bottom:8px; font-size:13px; }
.sel-item .word { font-weight:700; font-size:15px; display:flex; justify-content:space-between; }
.sel-item button { border:0; background:none; color:var(--muted); cursor:pointer; font-size:16px; }
.sel-item .sent { color:var(--muted); margin-top:4px; line-height:1.4; max-height:3.9em; overflow:hidden; }
#addrow { display:flex; gap:6px; margin:10px 0; }
#addrow input { flex:1; min-width:0; padding:8px; border:1px solid var(--line); border-radius:6px; font-size:13px; background:var(--paper); color:var(--ink); }
button { cursor:pointer; }
button:disabled { cursor:not-allowed; opacity:.45; }
#addrow button,.phase-nav button,.word-nav button,.continue-button { padding:8px 12px; border:1px solid var(--line); border-radius:6px; background:var(--soft); color:var(--ink); }
#actions { position:sticky; bottom:0; padding-top:12px; background:var(--paper); }
#submit { width:100%; padding:12px; border:0; border-radius:8px; background:var(--accent); color:#fff; font-weight:700; }
#main { min-width:0; }
.phase-nav { position:sticky; top:0; z-index:3; display:flex; gap:8px; padding:10px 24px; background:var(--paper); border-bottom:1px solid var(--line); font:13px ui-sans-serif,system-ui,sans-serif; }
.phase-nav button.active { background:var(--accent); color:#fff; border-color:var(--accent); }
.phase { display:none; }
.phase.active { display:block; }
.panel { max-width:940px; margin:0 auto; padding:36px 44px 100px; font-family:ui-sans-serif,system-ui,sans-serif; }
.panel h1 { font:700 30px Georgia,serif; margin:0; }
.status { padding:12px 15px; background:var(--soft); border-left:4px solid var(--accent); margin:16px 0 24px; }
.word-nav { display:grid; grid-template-columns:minmax(0,1fr) minmax(230px,auto) minmax(0,1fr); align-items:center; gap:12px; margin:0 0 20px; }
.word-nav button { width:100%; min-width:0; }
.word-nav button:last-child { justify-self:stretch; }
.word-jump-group { display:flex; align-items:center; justify-content:center; gap:8px; min-width:230px; }
.word-jump-group label { color:var(--muted); font-size:13px; white-space:nowrap; }
.word-jump { min-width:150px; max-width:230px; padding:8px 10px; border:1px solid var(--line); border-radius:6px; background:var(--paper); color:var(--ink); }
#word-progress { color:var(--muted); font-size:13px; font-weight:600; white-space:nowrap; }
.word-nav-bottom { margin-top:26px; }
.worksheet { padding:4px 0 30px; }
.worksheet>h2 { font:700 28px Georgia,serif; border-bottom:1px solid var(--line); padding-bottom:12px; }
.worksheet-body { line-height:1.68; }
.worksheet-body h1 { font-size:25px; margin-top:30px; }
.worksheet-body h2 { font-size:22px; margin-top:34px; }
.worksheet-body h3 { font-size:18px; margin-top:28px; }
.worksheet-body h4 { font-size:16px; margin-top:24px; }
.worksheet-body blockquote { margin:18px 0; padding:10px 16px; border-left:3px solid var(--accent); background:var(--soft); }
.worksheet-body blockquote p { margin:4px 0; }
.worksheet-body ul,.worksheet-body ol { padding-left:24px; }
.table-wrap { width:100%; overflow-x:auto; margin:16px 0 24px; }
table { width:100%; border-collapse:collapse; font-size:14px; line-height:1.45; }
th,td { padding:10px 12px; border:1px solid var(--line); text-align:left; vertical-align:top; }
th { background:var(--soft); font-weight:700; }
.quiz-slot { margin:18px 0; }
.quiz-item { padding:17px 18px; border:1px solid var(--line); border-radius:8px; background:var(--soft); }
.quiz-label { margin:0 0 10px; font-weight:700; color:var(--accent); }
.quiz-prompt p:first-child { margin-top:0; }
.option-row { display:flex; flex-wrap:wrap; gap:8px; margin-top:12px; }
.option { min-width:64px; padding:8px 13px; border:1px solid var(--line); border-radius:6px; background:var(--paper); color:var(--ink); }
.option.selected { border-color:var(--accent); background:var(--accent); color:#fff; }
.option.correct { border-color:#16834b; background:var(--success); color:var(--success-ink); }
.option.wrong { border-color:#c43d3d; background:var(--error); color:var(--error-ink); }
.feedback { margin-top:12px; padding:11px 13px; border-radius:6px; background:var(--success); color:var(--success-ink); line-height:1.55; }
.feedback.wrong { background:var(--error); color:var(--error-ink); }
.feedback[hidden] { display:none; }
hr { border:0; border-top:1px solid var(--line); margin:28px 0; }
code { background:var(--soft); padding:2px 4px; border-radius:3px; }
.empty { color:var(--muted); }
#toast { position:fixed; left:50%; bottom:28px; z-index:20; max-width:min(460px,calc(100vw - 32px)); transform:translate(-50%,12px); padding:10px 16px; border-radius:7px; background:#17191e; color:#fff; font:14px/1.4 ui-sans-serif,system-ui,sans-serif; opacity:0; visibility:hidden; transition:opacity .18s,transform .18s,visibility .18s; pointer-events:none; }
#toast.show { opacity:.94; visibility:visible; transform:translate(-50%,0); }
@media (max-width:1000px) { .layout { grid-template-columns:minmax(32px,1fr) minmax(0,1fr) 270px; } #sidebar { width:270px; } #article { padding-inline:32px; } }
@media (max-width:760px) { .layout { display:block; } #article { padding:28px 22px 120px; } #sidebar { position:static; width:100%; height:auto; border-left:0; border-top:1px solid var(--line); } .panel { padding:28px 20px 80px; } .word-nav { grid-template-columns:1fr 1fr; } .word-jump-group { grid-column:1/-1; grid-row:1; } .word-nav button { grid-row:2; } }
"""

PAGE_JS = r"""
const sel = new Map();
const answered = new Map();
let phase = 'select';
let pollTimer = null;
let worksheets = [];
let worksheetIndex = 0;
const $ = id => document.getElementById(id);

function esc(value) {
  return String(value).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
}
function toast(message) {
  const node = $('toast');
  node.textContent = message;
  node.classList.add('show');
  clearTimeout(node.hideTimer);
  node.hideTimer = setTimeout(() => node.classList.remove('show'), 1900);
}
function spansFor(lower) {
  return document.querySelectorAll('.w[data-lower="' + CSS.escape(lower) + '"]');
}
function toggleWord(element) {
  const lower = element.dataset.lower;
  if (sel.has(lower)) {
    sel.delete(lower);
    spansFor(lower).forEach(span => span.classList.remove('sel'));
  } else {
    const spans = spansFor(lower);
    sel.set(lower, {word:element.dataset.word, display:element.dataset.word, sentence:element.dataset.sent, count:spans.length});
    spans.forEach(span => span.classList.add('sel'));
  }
  renderSidebar();
}
function renderSidebar() {
  const list = $('sel-list');
  list.innerHTML = '';
  for (const [lower, info] of sel) {
    const item = document.createElement('div');
    item.className = 'sel-item';
    item.innerHTML = '<div class="word"><span>' + esc(info.display) +
      (info.count > 1 ? ' <small>x' + info.count + '</small>' : '') +
      '</span><button type="button" aria-label="Remove ' + esc(info.display) + '">×</button></div>' +
      '<div class="sent">' + esc(info.sentence) + '</div>';
    item.querySelector('button').onclick = () => {
      sel.delete(lower);
      spansFor(lower).forEach(span => span.classList.remove('sel'));
      renderSidebar();
    };
    list.appendChild(item);
  }
  $('count').textContent = sel.size;
}
function showPhase(name) {
  phase = name;
  document.querySelectorAll('.phase').forEach(node => node.classList.toggle('active', node.id === name + '-phase'));
  document.querySelectorAll('.phase-nav button').forEach(node => node.classList.toggle('active', node.dataset.phase === name));
  if (name === 'learn' && pollTimer === null) pollStatus();
  window.scrollTo({top:0, behavior:'auto'});
}
function quizKey(sheet, question) {
  return sheet.word + ':' + question.id;
}
function renderQuestion(slot, sheet, question) {
  const card = document.createElement('section');
  card.className = 'quiz-item';
  card.setAttribute('aria-labelledby', 'quiz-' + question.id);
  card.innerHTML = '<div class="quiz-label" id="quiz-' + esc(question.id) + '">' + esc(question.id) + '</div>' +
    '<div class="quiz-prompt">' + question.prompt_html + '</div>';
  const options = document.createElement('div');
  options.className = 'option-row';
  options.setAttribute('role', 'group');
  options.setAttribute('aria-label', 'Answer options for ' + question.id);
  const feedback = document.createElement('div');
  feedback.className = 'feedback';
  feedback.hidden = true;
  const key = quizKey(sheet, question);

  function reveal(choice) {
    const correct = Boolean(question.answer) && choice.toLowerCase() === question.answer.toLowerCase();
    options.querySelectorAll('button').forEach(button => {
      button.disabled = true;
      if (button.dataset.option.toLowerCase() === question.answer.toLowerCase()) button.classList.add('correct');
      if (button.dataset.option === choice && !correct) button.classList.add('wrong');
      if (button.dataset.option === choice) button.classList.add('selected');
    });
    feedback.classList.toggle('wrong', !correct);
    feedback.innerHTML = '<strong>' + (correct ? 'Correct.' : 'Correct answer: ' + esc(question.answer || 'Unavailable') + '.') + '</strong>' +
      (question.explanation_html ? '<div>' + question.explanation_html + '</div>' : '');
    feedback.hidden = false;
  }

  question.options.forEach(option => {
    const button = document.createElement('button');
    button.type = 'button';
    button.className = 'option';
    button.dataset.option = option;
    button.textContent = option;
    button.onclick = () => {
      if (answered.has(key)) return;
      answered.set(key, option);
      reveal(option);
    };
    options.appendChild(button);
  });
  card.appendChild(options);
  card.appendChild(feedback);
  slot.replaceWith(card);
  if (answered.has(key)) reveal(answered.get(key));
}
function renderWordNavigation() {
  const previous = document.querySelectorAll('.prev-word');
  const next = document.querySelectorAll('.next-word');
  const progress = document.querySelectorAll('.word-progress');
  const jumps = document.querySelectorAll('.word-jump');
  const hasWords = worksheets.length > 0;
  previous.forEach(button => { button.disabled = !hasWords || worksheetIndex === 0; });
  next.forEach(button => { button.disabled = !hasWords || worksheetIndex === worksheets.length - 1; });
  const current = hasWords ? (worksheetIndex + 1) + ' / ' + worksheets.length + ' · ' + worksheets[worksheetIndex].word : '0 words';
  progress.forEach(node => { node.textContent = current; });
  jumps.forEach(select => {
    select.innerHTML = hasWords ? worksheets.map((sheet, index) => '<option value="' + index + '">' + (index + 1) + '. ' + esc(sheet.word) + '</option>').join('') : '<option value="">No worksheets</option>';
    select.value = hasWords ? String(worksheetIndex) : '';
    select.disabled = !hasWords;
  });
}
function renderCurrentWorksheet(scrollToTop = true) {
  const area = $('worksheets');
  if (!worksheets.length) {
    area.innerHTML = '<p class="empty">No worksheets yet. Select words first, or continue to deep reading.</p>';
    renderWordNavigation();
    return;
  }
  worksheetIndex = Math.max(0, Math.min(worksheetIndex, worksheets.length - 1));
  const sheet = worksheets[worksheetIndex];
  area.innerHTML = '<article class="worksheet"><h2>' + esc(sheet.word) + '</h2><div class="worksheet-body">' + sheet.html + '</div></article>';
  const byId = new Map(sheet.questions.map(question => [question.id, question]));
  area.querySelectorAll('.quiz-slot').forEach(slot => {
    const question = byId.get(slot.dataset.quizId);
    if (question) renderQuestion(slot, sheet, question);
  });
  renderWordNavigation();
  if (scrollToTop) window.scrollTo({top:0, behavior:'auto'});
}
function sameWorksheet(left, right) {
  if (!left || !right || left.word !== right.word || left.html !== right.html) return false;
  if (left.questions.length !== right.questions.length) return false;
  return left.questions.every((question, index) => {
    const other = right.questions[index];
    return other && question.id === other.id && question.answer === other.answer && question.explanation_html === other.explanation_html;
  });
}
function renderWorksheets(data) {
  const currentSheet = worksheets[worksheetIndex];
  const currentWord = currentSheet?.word;
  const nextWorksheets = data.worksheets || [];
  const sameIndex = nextWorksheets.findIndex(sheet => sheet.word === currentWord);
  const nextIndex = sameIndex >= 0 ? sameIndex : Math.min(worksheetIndex, Math.max(0, nextWorksheets.length - 1));
  const currentUnchanged = sameWorksheet(currentSheet, nextWorksheets[nextIndex]) && $('worksheets').querySelector('.worksheet');
  worksheets = nextWorksheets;
  worksheetIndex = nextIndex;
  if (currentUnchanged) {
    renderWordNavigation();
    return;
  }
  const preservePosition = Boolean(currentWord && sameIndex >= 0);
  const scrollPosition = window.scrollY;
  renderCurrentWorksheet(!preservePosition);
  if (preservePosition) window.scrollTo({top:scrollPosition, behavior:'auto'});
}
async function pollStatus() {
  pollTimer = 'requesting';
  try {
    const response = await fetch('/status', {cache:'no-store'});
    const data = await response.json();
    if (data.worksheets) renderWorksheets(data);
    if (data.status === 'running') {
      $('learn-status').textContent = 'SMD is generating worksheets… ' + data.completed + '/' + data.total + ' complete';
      pollTimer = setTimeout(pollStatus, 1200);
    } else if (data.status === 'done') {
      $('learn-status').textContent = data.archive_total ? 'Worksheets ready · ' + data.archive_total + ' words' : 'No vocabulary learning was requested';
      pollTimer = 'done';
    } else if (data.status === 'failed') {
      $('learn-status').textContent = 'Generation finished with an error: ' + data.error;
      pollTimer = 'done';
    } else {
      $('learn-status').textContent = 'Select words on the Select page, then use Generate learning.';
      pollTimer = 'idle';
    }
  } catch (error) {
    $('learn-status').textContent = 'Status unavailable: ' + error;
    pollTimer = setTimeout(pollStatus, 1800);
  }
}

document.querySelectorAll('.w').forEach(node => node.addEventListener('click', () => toggleWord(node)));
document.querySelectorAll('.phase-nav button').forEach(button => button.onclick = () => showPhase(button.dataset.phase));
document.querySelectorAll('.prev-word').forEach(button => button.onclick = () => { if (worksheetIndex > 0) { worksheetIndex -= 1; renderCurrentWorksheet(); } });
document.querySelectorAll('.next-word').forEach(button => button.onclick = () => { if (worksheetIndex < worksheets.length - 1) { worksheetIndex += 1; renderCurrentWorksheet(); } });
document.querySelectorAll('.word-jump').forEach(select => select.onchange = () => { worksheetIndex = Number(select.value); renderCurrentWorksheet(); });
$('add-btn').onclick = () => {
  const input = $('add-input');
  const word = input.value.trim();
  if (!word) return;
  const lower = word.toLowerCase();
  if (!sel.has(lower)) sel.set(lower, {word:word, display:word, sentence:'', count:0});
  input.value = '';
  renderSidebar();
  toast('Added: ' + word);
};
$('add-input').onkeydown = event => { if (event.key === 'Enter') $('add-btn').click(); };
$('submit').onclick = async () => {
  if (!sel.size) {
    showPhase('deep');
    return;
  }
  const button = $('submit');
  button.disabled = true;
  button.textContent = 'Starting…';
  try {
    const response = await fetch('/submit', {
      method:'POST', headers:{'Content-Type':'application/json'},
      body:JSON.stringify({items:[...sel.values()]})
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.message || response.status);
    $('learn-status').textContent = data.message;
    pollTimer = null;
    showPhase('learn');
  } catch (error) {
    button.disabled = false;
    button.textContent = 'Generate learning';
    toast('Submission failed: ' + error);
  }
};
"""


def render_page(text, run_smd):
    label = "Generate learning" if run_smd else "Write batch.txt"
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Reading workflow</title><style>{PAGE_CSS}</style></head><body><div id="main"><nav class="phase-nav" aria-label="Reading phases"><button data-phase="select" class="active">1. Select</button><button data-phase="learn">2. Learn</button><button data-phase="deep">3. Deep reading</button></nav><section id="select-phase" class="phase active"><div class="layout"><div id="article">{article_html(text)}</div><aside id="sidebar"><h2>Selected <span id="count">0</span></h2><div id="addrow"><input id="add-input" type="text" placeholder="Add a word or phrase"><button id="add-btn" type="button">Add</button></div><div id="sel-list"></div><div id="actions"><button id="submit" type="button">{label}</button></div></aside></div></section><section id="learn-phase" class="phase"><div class="panel"><h1>Vocabulary learning</h1><div id="learn-status" class="status">Select words to start generation</div><div class="word-nav"><button class="prev-word" type="button" disabled>← Previous word</button><div class="word-jump-group"><label for="word-jump-top">Jump to</label><select id="word-jump-top" class="word-jump" aria-label="Jump to word"><option value="">No worksheets</option></select><span class="word-progress">0 words</span></div><button class="next-word" type="button" disabled>Next word →</button></div><div id="worksheets"><p class="empty">Your SMD worksheets will appear here</p></div><div class="word-nav word-nav-bottom"><button class="prev-word" type="button" disabled>← Previous word</button><div class="word-jump-group"><label for="word-jump-bottom">Jump to</label><select id="word-jump-bottom" class="word-jump" aria-label="Jump to word"><option value="">No worksheets</option></select><span class="word-progress">0 words</span></div><button class="next-word" type="button" disabled>Next word →</button></div><button class="continue-button" type="button" onclick="showPhase('deep')">Continue to deep reading →</button></div></section><section id="deep-phase" class="phase"><div class="panel"><h1>Deep Reading Phase</h1><p class="status">Read the article closely. Return to Select or Learn above whenever you need to review a word or answer.</p><div id="deep-article">{article_html(text, selectable=False)}</div></div></section></div><div id="toast"></div><script>{PAGE_JS}</script></body></html>'''


class PickServer:
    def __init__(self, page_html, day_dir, run_smd, concurrency):
        self.page_html, self.day_dir = page_html, day_dir
        self.run_smd, self.concurrency = run_smd, concurrency
        self.lock = threading.Lock()
        self.process = None
        self.status = "idle"
        self.error = ""
        self.total = self.completed = 0
        self.selected_words = []
        self._sheets_sig = None
        self._sheets_cache = []

    def handler(self):
        outer = self
        class H(BaseHTTPRequestHandler):
            def log_message(self, fmt, *args): pass
            def send_body(self, code, body, ctype="text/html; charset=utf-8"):
                data = body.encode("utf-8"); self.send_response(code); self.send_header("Content-Type", ctype); self.send_header("Content-Length", str(len(data))); self.end_headers(); self.wfile.write(data)
            def do_GET(self):
                if self.path in ("/", "/index.html"):
                    self.send_body(200, outer.page_html)
                elif self.path == "/status":
                    self.send_body(200, json.dumps(outer.status_payload(), ensure_ascii=False), "application/json; charset=utf-8")
                else: self.send_body(404, "not found", "text/plain")
            def do_POST(self):
                if self.path != "/submit": self.send_body(404, "not found", "text/plain"); return
                try:
                    expected_origin = f"http://127.0.0.1:{self.server.server_port}"
                    if self.headers.get("Origin") != expected_origin:
                        self.send_body(403, json.dumps({"message":"Forbidden origin"}), "application/json; charset=utf-8"); return
                    content_type = self.headers.get("Content-Type", "").partition(";")[0].strip().lower()
                    if content_type != "application/json":
                        self.send_body(415, json.dumps({"message":"Content-Type must be application/json"}), "application/json; charset=utf-8"); return
                    raw_length = self.headers.get("Content-Length")
                    if raw_length is None:
                        self.send_body(411, json.dumps({"message":"Content-Length is required"}), "application/json; charset=utf-8"); return
                    length = int(raw_length)
                    if length < 0:
                        raise ValueError("Invalid Content-Length")
                    if length > MAX_SUBMIT_BYTES:
                        # Drain (bounded) so the client can still read the 413
                        # response before the connection closes.
                        remaining = min(length, 16 * 1024 * 1024)
                        while remaining > 0:
                            chunk = self.rfile.read(min(remaining, 65536))
                            if not chunk: break
                            remaining -= len(chunk)
                        self.send_body(413, json.dumps({"message":"Request body exceeds 64 KB"}), "application/json; charset=utf-8"); return
                    payload=json.loads(self.rfile.read(length) or b"{}"); items=payload.get("items", [])
                    message = outer.submit(items)
                    self.send_body(200, json.dumps({"message":message}, ensure_ascii=False), "application/json; charset=utf-8")
                except SubmissionInProgressError as e:
                    self.send_body(409, json.dumps({"message":str(e)}, ensure_ascii=False), "application/json; charset=utf-8")
                except Exception as e:
                    self.send_body(400, json.dumps({"message":str(e)}, ensure_ascii=False), "application/json; charset=utf-8")
        return H

    def load_sheets(self):
        out = os.path.join(self.day_dir, "smd")
        try:
            names = sorted(os.listdir(out)) if os.path.isdir(out) else []
        except OSError:
            names = []
        paths = [os.path.join(out, x) for x in names if x.endswith(".md")]
        sig = []
        for path in paths:
            try:
                st = os.stat(path)
                sig.append((os.path.basename(path), st.st_mtime_ns, st.st_size))
            except OSError:
                sig.append((os.path.basename(path), 0, 0))
        sig = tuple(sig)
        with self.lock:
            if sig == self._sheets_sig:
                return self._sheets_cache
        sheets = []
        for path in paths:
            try:
                with open(path, encoding="utf-8") as f: content=f.read()
                word = re.sub(r"^# SMD:\s*", "", content.splitlines()[0]) if content else os.path.basename(path)
                rendered, questions = render_learning_content(content)
                sheets.append({"word": word, "html": rendered, "questions": questions})
            except OSError: pass
        with self.lock:
            self._sheets_sig, self._sheets_cache = sig, sheets
        return sheets

    def status_payload(self):
        sheets = self.load_sheets()
        with self.lock:
            status, error, total = self.status, self.error, self.total
            selected_words = list(self.selected_words)
        # Keep the complete SMD archive visible, while reporting generation
        # progress only for the words submitted in this run.
        archived_words = {sheet["word"].strip().casefold() for sheet in sheets}
        completed = (sum(word.casefold() in archived_words for word in selected_words)
                     if selected_words else len(sheets))
        if status == "idle" and sheets:
            status = "done"
            total = len(sheets)
        return {"status": status, "error": error, "total": total,
                "completed": completed, "archive_total": len(sheets),
                "worksheets": sheets}

    def submit(self, items):
        valid = [(str(i.get("word") or i.get("display") or "").strip(), str(i.get("sentence") or "").strip()) for i in items if str(i.get("word") or i.get("display") or "").strip()]
        if not valid: raise ValueError("No words selected")
        batch_path = os.path.join(self.day_dir, "batch.txt")
        with self.lock:
            if self.status == "running":
                raise SubmissionInProgressError("SMD generation is already running")
            self.selected_words = [word for word, _ in valid]
            with open(batch_path, "w", encoding="utf-8") as f:
                f.write(f"# Selected {datetime.datetime.now():%Y-%m-%d %H:%M}\n" + "\n".join(f"{w} | {s} | " for w,s in valid) + "\n")
            if not self.run_smd:
                self.status, self.error, self.total = "done", "", len(valid)
                return f"Wrote {len(valid)} words to batch.txt"
            out = os.path.join(self.day_dir, "smd"); os.makedirs(out, exist_ok=True)
            cmd = [sys.executable, SMD_PATH, "-f", batch_path, "--out", out, "--concurrency", str(self.concurrency)]
            try:
                process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding="utf-8", errors="replace")
            except Exception as exc:
                self.status, self.error, self.total = "failed", str(exc), len(valid)
                return f"Batch saved, but SMD could not start: {exc}"
            self.process = process
            self.status, self.error, self.total = "running", "", len(valid)
        threading.Thread(target=self._drain, args=(process, out), daemon=True).start()
        return f"Started SMD for {len(valid)} words. This page will update when worksheets are ready."

    def _drain(self, process, out):
        for line in process.stdout: print("[smd] " + line.rstrip(), flush=True)
        code = process.wait()
        with self.lock:
            if self.process is process:
                self.process = None
            self.status = "done" if code == 0 else "failed"
            self.error = "SMD exited with code " + str(code) if code else ""
        print(f"[smd] finished ({code}), output -> {out}", flush=True)


def free_port(preferred):
    sock=socket.socket()
    try:
        sock.bind(("127.0.0.1", preferred)); return preferred
    except OSError:
        sock.bind(("127.0.0.1", 0)); return sock.getsockname()[1]
    finally: sock.close()


def main():
    ap=argparse.ArgumentParser(description="Browser reading workflow: select -> learn -> deep read")
    ap.add_argument("-d", "--day"); ap.add_argument("--port", type=int, default=8009); ap.add_argument("--no-run", action="store_true"); ap.add_argument("--concurrency", type=int, default=2); ap.add_argument("--no-browser", action="store_true")
    args=ap.parse_args(); day_dir=resolve_day_dir(args.day)
    with open(os.path.join(day_dir, "article.txt"), encoding="utf-8") as f: text=f.read()
    server=PickServer(render_page(text, not args.no_run), day_dir, not args.no_run, args.concurrency)
    port=free_port(args.port); httpd=ThreadingHTTPServer(("127.0.0.1", port), server.handler()); url=f"http://127.0.0.1:{port}/"
    print(f"Reading workflow: {url}", flush=True)
    if not args.no_browser: webbrowser.open(url)
    try: httpd.serve_forever()
    except KeyboardInterrupt: print("\nServer stopped")


if __name__ == "__main__": main()
