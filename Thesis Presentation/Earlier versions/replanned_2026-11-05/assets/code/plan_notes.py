"""Extract speaker-note fields verbatim from the presentation execution plan."""
import re


def _section(lines, start_pat):
    start = next(i for i, l in enumerate(lines) if re.match(start_pat, l))
    end = next((j for j in range(start + 1, len(lines)) if lines[j].startswith("### ") or lines[j].startswith("## ")),
               len(lines))
    return lines[start + 1:end]


def _clean(t):
    return t.replace("`", "").strip()


def _field(sec, labels):
    for i, l in enumerate(sec):
        for lab in labels:
            tag = f"**{lab}:**"
            if l.startswith(tag):
                out = [l[len(tag):].strip()]
                for nxt in sec[i + 1:]:
                    if not nxt.strip() or nxt.startswith("**"):
                        break
                    out.append(nxt.strip())
                return _clean(" ".join(out))
    return None


def _script(sec):
    i = next(k for k, l in enumerate(sec) if l.startswith("**Speaker script:**"))
    paras, cur = [], []
    for l in sec[i + 1:]:
        if l.startswith("**Delivery cue"):
            break
        if l.startswith(">"):
            cur.append(l[1:].strip())
        elif not l.strip() and cur:
            paras.append(" ".join(cur))
            cur = []
    if cur:
        paras.append(" ".join(cur))
    return "\n\n".join(paras)


def load(path):
    lines = open(path, encoding="utf-8").read().split("\n")
    main = {}
    for n in range(1, 15):
        sec = _section(lines, rf"### Slide {n} — ")
        main[n] = dict(script=_script(sec), cue=_field(sec, ["Delivery cue"]),
                       transition=_field(sec, ["Transition"]), source=_field(sec, ["Source"]))
    backups = {}
    for k in range(1, 15):
        sec = _section(lines, rf"### B{k} / Slide {k + 14} — ")
        backups[k] = dict(question=_field(sec, ["Question answered", "Question"]),
                          answer=_field(sec, ["Answer to give", "Answer"]),
                          notes=_field(sec, ["Notes to include", "Notes"]),
                          anchor=_field(sec, ["Additional anchor"]),
                          source=_field(sec, ["Source"]))
    return main, backups


if __name__ == "__main__":
    import sys
    m, b = load(sys.argv[1])
    for n, d in m.items():
        print(f"=== Slide {n}")
        for k, v in d.items():
            print(f"[{k}] {v}")
    for n, d in b.items():
        print(f"=== B{n}")
        for k, v in d.items():
            print(f"[{k}] {v}")
