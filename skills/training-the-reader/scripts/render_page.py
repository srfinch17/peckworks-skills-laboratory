"""Render a day page to plain text the way a reader sees it: headings, lists, code, figure captions, details."""
import re, html, sys, os
def render(src):
    t = open(src, encoding="utf-8").read()
    t = re.sub(r"<style.*?</style>|<script.*?</script>", "", t, flags=re.S)
    # figures: keep step captions, drop the svg body but keep its text labels compactly
    def fig(m):
        block = m.group(0)
        cap = re.search(r'data-cap="([^"]*)"', block)
        steps = re.search(r'data-steps="(\d+)"', block)
        labels = [html.unescape(re.sub(r"<[^>]+>", "", x)).strip() for x in re.findall(r"<text[^>]*>(.*?)</text>", block, flags=re.S)]
        labels = [l for l in labels if l]
        out = "\n[FIGURE, %s steps]\n" % (steps.group(1) if steps else "?")
        if cap:
            for i, c in enumerate(html.unescape(cap.group(1)).split("|"), 1):
                out += "  step %d caption: %s\n" % (i, re.sub(r"<[^>]+>", "", c).strip())
        if labels: out += "  svg labels: " + " | ".join(labels[:40]) + "\n"
        return out + "[/FIGURE]\n"
    t = re.sub(r"<svg[^>]*data-steps=.*?</svg>", fig, t, flags=re.S)
    t = re.sub(r"<svg.*?</svg>", lambda m: "[icon]" if len(m.group(0)) < 600 else "[svg figure: " + " | ".join(l.strip() for l in re.findall(r"<text[^>]*>(.*?)</text>", m.group(0), flags=re.S) if l.strip())[:600] + "]", t, flags=re.S)
    t = t.replace('<span', ' <span').replace('</span>', '</span> ')
    # code blocks
    t = re.sub(r"<pre[^>]*>(.*?)</pre>", lambda m: "\n```\n" + html.unescape(re.sub(r"<[^>]+>", "", m.group(1))) + "\n```\n", t, flags=re.S)
    t = re.sub(r"<details[^>]*>", "\n[DETAILS, collapsed until clicked]\n", t); t = t.replace("</details>", "\n[/DETAILS]\n")
    t = re.sub(r"<summary[^>]*>", "\n[summary shown] ", t)
    t = re.sub(r"<h1[^>]*>", "\n\n# ", t); t = re.sub(r"<h2[^>]*>", "\n\n## ", t); t = re.sub(r"<h3[^>]*>", "\n\n### ", t); t = re.sub(r"<h4[^>]*>", "\n\n#### ", t)
    t = re.sub(r"<li[^>]*>", "\n - ", t)
    t = re.sub(r"<(tr)[^>]*>", "\n| ", t); t = re.sub(r"</t[dh]>", " | ", t)
    t = re.sub(r"<br\s*/?>", "\n", t)
    t = re.sub(r"</?(p|div|section|article|header|footer|nav|figure|figcaption|table|ul|ol|blockquote|aside|hr)[^>]*>", "\n", t)
    t = re.sub(r"<[^>]+>", "", t)
    t = html.unescape(t)
    t = re.sub(r"[ \t]+", " ", t); t = re.sub(r"\n[ \t]+", "\n", t); t = re.sub(r"\n{3,}", "\n\n", t)
    return t.strip() + "\n"
if __name__ == "__main__":
    src, dst = sys.argv[1], sys.argv[2]
    out = render(src); open(dst, "w", encoding="utf-8").write(out)
    print(os.path.basename(src), "->", os.path.basename(dst), len(out), "chars")
