#!/usr/bin/env python3
"""급수 안내 페이지·사이트맵·llms 파일·홈 구조화 데이터를 만든다. 표준 라이브러리만 쓴다.

실행: python3 scripts/build-pages.py
입력: data/hanja-by-grade.json(앱 수록 한자), data/kccpt-official.json(한국어문회 공개 표)
출력: public/grades/, public/exam-schedule/, public/sitemap.xml, public/llms.txt,
      public/llms-full.txt, public/index.html의 구조화 데이터 구역
"""
import datetime as dt
import html
import json
import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / 'public'
SITE = 'https://hanja.sunw.kr'
APP = 'https://hanja-app.sunw.kr/'
ORG = {'@type': 'Organization', '@id': 'https://www.sunworks.kr/#organization',
       'name': '썬웍스', 'alternateName': 'SunWorks', 'url': 'https://www.sunworks.kr/'}
WEBSITE_ID = f'{SITE}/#website'
SOCIAL = f'{SITE}/assets/social-card.png'
WEEKDAY = '월화수목금토일'

hanja_data = json.loads((ROOT / 'data/hanja-by-grade.json').read_text())
official = json.loads((ROOT / 'data/kccpt-official.json').read_text())
CHECKED = official['_meta']['checked']
# '다음 시험'은 빌드한 날 기준으로 고른다. 배포 워크플로가 매주 다시 빌드해 지난 회차를 내린다.
TODAY = os.environ.get('BUILD_DATE') or dt.date.today().isoformat()
SRC = official['_meta']['sources']
OFFICIAL = {g['grade']: g for g in official['grades']}
SLUG = {'8급': '8', '7급II': '7-2', '7급': '7', '6급II': '6-2', '6급': '6', '5급II': '5-2',
        '5급': '5', '4급II': '4-2', '4급': '4', '3급II': '3-2', '3급': '3', '2급': '2', '1급': '1'}
GRADES = hanja_data['grades']  # 쉬운 급수부터
for g in GRADES:
    # 목록은 음(훈음의 마지막 글자) 가나다순. 같은 음은 앱 수록 순서를 지킨다.
    g['hanja'] = sorted(g['hanja'], key=lambda h: h['hoondok'].split()[-1])

# 앱 수록 한자의 누적 수가 공식 읽기 배정한자 수와 다르면 만들지 않는다.
total = 0
for g in GRADES:
    total += len(g['hanja'])
    g['cum'] = total
    g['new'] = len(g['hanja'])
    assert OFFICIAL[g['grade']]['read'] == total, (g['grade'], total)


def esc(s):
    return html.escape(str(s), quote=True)


def kdate(iso, weekday=True):
    d = dt.date.fromisoformat(iso)
    s = f'{d.year}년 {d.month}월 {d.day}일'
    return f'{s}({WEEKDAY[d.weekday()]})' if weekday else s


def md(iso):
    d = dt.date.fromisoformat(iso)
    return f'{d.month}월 {d.day}일({WEEKDAY[d.weekday()]})'


def won(n):
    return f'{n:,}원'


def aux_of(h):
    """함께 쓰는 다른 훈음. 대표 훈음과 같으면 보이지 않는다."""
    aux = h.get('soundsAux', '').replace(' | ', ', ')
    return aux if aux and aux != h['hoondok'] else ''


def ld(obj):
    return json.dumps(obj, ensure_ascii=False, indent=1).replace('</', '<\\/')


def page_ld(url, name, description, crumbs, faqs, extra=(), modified=CHECKED):
    graph = [
        {'@type': 'WebPage', '@id': f'{url}#webpage', 'url': url, 'name': name,
         'description': description, 'inLanguage': 'ko', 'dateModified': modified,
         'isPartOf': {'@id': WEBSITE_ID}, 'publisher': {'@id': ORG['@id']},
         'breadcrumb': {'@id': f'{url}#breadcrumb'}},
        {'@type': 'BreadcrumbList', '@id': f'{url}#breadcrumb', 'itemListElement': [
            {'@type': 'ListItem', 'position': i + 1, 'name': n, 'item': u}
            for i, (n, u) in enumerate(crumbs)]},
        {'@type': 'FAQPage', '@id': f'{url}#faq', 'mainEntity': [
            {'@type': 'Question', 'name': q,
             'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in faqs]},
        ORG,
        *extra,
    ]
    return ld({'@context': 'https://schema.org', '@graph': graph})


def faq_html(faqs):
    items = ''.join(
        f'<details><summary>{esc(q)}<span aria-hidden="true">+</span></summary>'
        f'<p>{esc(a)}</p></details>' for q, a in faqs)
    return (f'<section class="guide-block" aria-labelledby="faq-title">'
            f'<h2 id="faq-title">자주 묻는 질문</h2><div class="guide-faq">{items}</div></section>')


def sources_html(keys, extra=''):
    names = {'schedule': '시행 일정', 'levels': '급수 배정', 'questions': '출제 기준',
             'passRule': '합격 기준', 'examTime': '시험 시간', 'fee': '검정료', 'cert': '자격 정보'}
    links = ' · '.join(f'<a href="{SRC[k]}">{names[k]}</a>' for k in keys)
    return (f'<section class="guide-block guide-sources" aria-labelledby="src-title">'
            f'<h2 id="src-title">출처</h2><p>사단법인 한국어문회 누리집: {links} '
            f'({kdate(CHECKED, False)} 확인). 한국어문회 기준이 바뀌면 이 페이지도 고칩니다. '
            f'접수 전에는 한국어문회 공지를 꼭 함께 확인해 주세요. 어흥!한자는 사단법인 한국어문회와 제휴·인증 관계가 없는 자체 제작 학습 앱입니다.</p>{extra}</section>')


CTA = (f'<aside class="guide-cta" aria-label="어흥!한자 소개"><div>'
       f'<p class="guide-cta-title">목록을 읽는 데서 끝내지 않게.</p>'
       f'<p>어흥!한자는 읽기·뜻·쓰기·부수를 따로 확인하고, 12시간 뒤 다시 맞혀야 익힘으로 칩니다. '
       f'급수에 따라 제공되는 학습 유형·삽화·음성 범위는 다릅니다.</p></div>'
       f'<a class="button button-primary" href="{APP}">웹에서 체험하기</a></aside>')


def shell(path, title, description, h1, lead, body, ld_json, noindex=False):
    url = f'{SITE}{path}'
    robots = '<meta name="robots" content="noindex" />' if noindex else ''
    return f'''<!doctype html>
<html lang="ko">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <meta name="theme-color" content="#fff9ed" />
    <title>{esc(title)}</title>
    <meta name="description" content="{esc(description)}" />
    {robots}<link rel="canonical" href="{url}" />
    <meta property="og:type" content="article" />
    <meta property="og:locale" content="ko_KR" />
    <meta property="og:site_name" content="어흥!한자" />
    <meta property="og:title" content="{esc(title)}" />
    <meta property="og:description" content="{esc(description)}" />
    <meta property="og:url" content="{url}" />
    <meta property="og:image" content="{SOCIAL}" />
    <meta property="og:image:width" content="1200" />
    <meta property="og:image:height" content="630" />
    <meta name="twitter:card" content="summary_large_image" />
    <link rel="icon" href="/favicon.ico" sizes="48x48" />
    <link rel="icon" href="/assets/favicon-32.png" type="image/png" sizes="32x32" />
    <link rel="apple-touch-icon" href="/assets/apple-touch-icon.png" />
    <link rel="stylesheet" href="/styles.css?v=20261006-mastery" />
    <link rel="stylesheet" href="/legal.css?v=20261003" />
    <link rel="stylesheet" href="/guide.css?v=20261017" />
    <script src="/analytics.js?v=20261016" defer></script>
    <script type="application/ld+json">
{ld_json}
    </script>
  </head>
  <body class="guide-page">
    <a class="skip-link" href="#main">본문으로 바로 가기</a>
    <header class="site-header legal-header">
      <div class="nav-wrap">
        <a class="brand" href="/"><img src="/assets/hanja-icon.webp?v=20261006b" width="42" height="42" alt="" /><span>어흥!한자<span class="brand-dot">.</span></span></a>
        <a class="button button-small button-ink" href="{APP}">웹에서 체험하기</a>
      </div>
    </header>
    <main id="main" class="section-wrap guide-main">
      <nav class="guide-crumbs" aria-label="현재 위치">{crumbs_html(path)}</nav>
      <div class="guide-title">
        <h1>{h1}</h1>
        <p class="guide-answer">{lead}</p>
        <p class="guide-date">한국어문회 자료 확인: {kdate(CHECKED, False)}</p>
      </div>
{body}
    </main>
    <footer class="site-footer section-wrap legal-footer">
      <div class="footer-main">
        <div><a class="brand" href="/">어흥!한자<span class="brand-dot">.</span></a><p>중2 아들과 함께 만들고, 계속 자라는 한자 앱.</p></div>
        <nav class="footer-links" aria-label="사이트 안내">
          <a href="/grades/">급수별 한자 목록</a><a href="/exam-schedule/">한자 시험 일정</a>
          <a href="/support">고객지원</a><a href="/privacy"><strong>개인정보 처리방침</strong></a>
          <a href="/terms">이용약관</a><a href="https://www.sunworks.kr/">썬웍스 소개</a>
        </nav>
      </div>
      <p class="footer-status">어흥!한자는 사단법인 한국어문회와 제휴·인증 관계가 없는 자체 제작 학습 앱입니다.</p>
      <p class="footer-status">썬웍스 · 대표 남선 · 사업자등록번호 463-11-02942 · 통신판매업 신고번호 2026-서울송파-2924 · 서울특별시 송파구 위례광장로 199, 성희프라자 501-3-10호 · 070-8717-8850 · support@sunworks.kr</p>
      <small>© 2026 Sunworks. All rights reserved.</small>
    </footer>
  </body>
</html>
'''


CRUMBS = {}


def crumbs_html(path):
    parts = CRUMBS[path]
    out = []
    for i, (name, url) in enumerate(parts):
        if i == len(parts) - 1:
            out.append(f'<span aria-current="page">{esc(name)}</span>')
        else:
            out.append(f'<a href="{url.removeprefix(SITE)}">{esc(name)}</a>')
    return ' <span aria-hidden="true">›</span> '.join(out)


def write(path, text):
    target = PUBLIC / path.strip('/') / 'index.html' if path.endswith('/') else PUBLIC / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text)


def type_rows(grade):
    col = official['questionTypes']['columns'].index(grade)
    return [(row[0], row[col + 1]) for row in official['questionTypes']['rows'] if row[col + 1]]


def start_time(grade):
    upper = grade.startswith(('특급', '1급', '2급', '3급'))
    return official['schedule']['startTimes']['특급~3급II' if upper else '4급~8급']


def pass_percent(grade):
    return 80 if grade in ('특급', '특급II', '1급') else 70


# ---------- 급수별 페이지 ----------
home_crumb = ('어흥!한자', f'{SITE}/')
grades_crumb = ('급수별 한자', f'{SITE}/grades/')
for i, g in enumerate(GRADES):
    name, o = g['grade'], OFFICIAL[g['grade']]
    path = f'/grades/{SLUG[name]}/'
    url = f'{SITE}{path}'
    CRUMBS[path] = [home_crumb, grades_crumb, (f'{name} 한자', url)]
    lower = GRADES[i - 1]['grade'] if i else None
    if lower:
        count_sentence = (f'{name}의 읽기 배정한자는 {o["read"]:,}자입니다. 이 가운데 {g["new"]:,}자가 {name}에서 '
                          f'새로 나오고, 나머지 {o["read"] - g["new"]:,}자는 {lower}까지의 한자입니다.')
    else:
        count_sentence = f'{name}의 읽기 배정한자는 {o["read"]:,}자이고, 모두 처음 배우는 한자입니다.'
    pass_sentence = f'{name} 시험은 {o["questions"]}문항이며 {o["pass"]}문항 이상 맞히면 합격입니다.'
    lead = f'한자능력검정시험(한국어문회) {count_sentence} {pass_sentence}'
    counts = f'{o["read"]:,}자' if o['read'] == g['new'] else f'{o["read"]:,}자 · 신출 {g["new"]:,}자'
    title = f'한자 {name} 배정한자 {counts} 목록과 합격 기준 | 어흥!한자'
    description = (f'한자능력검정시험 {name} 배정한자 {o["read"]:,}자 중 {name}에서 새로 나오는 {g["new"]:,}자의 훈음·부수·총획 목록. '
                   f'{o["questions"]}문항 중 {o["pass"]}문항 합격, 시험 {o["minutes"]}분, 검정료 {won(o["fee"])}.')
    write_text = f'{o["write"]:,}자' if o['write'] else '없음(한자 쓰기 문제 없음)'
    facts = [
        ('읽기 배정한자', f'{o["read"]:,}자 (이번 급수에서 새로 {g["new"]:,}자)'),
        ('쓰기 배정한자', write_text),
        ('출제 문항', f'{o["questions"]}문항'),
        ('합격 기준', f'{o["pass"]}문항 이상 (출제 문항의 {pass_percent(name)}%)'),
        ('시험 시간', f'{o["minutes"]}분, 2026년 정기시험은 {start_time(name)} 시작'),
        ('검정료', won(o['fee'])),
        ('자격 종류', '공인민간자격' if o['cert'] == '공인' else '등록 민간자격'),
        ('수준', o['level']),
    ]
    facts_html = ''.join(f'<div><dt>{esc(k)}</dt><dd>{esc(v)}</dd></div>' for k, v in facts)
    types_html = ''.join(f'<tr><th scope="row">{esc(t)}</th><td>{n}</td></tr>' for t, n in type_rows(name))
    rows = []
    for n, h in enumerate(g['hanja'], 1):
        aux = f' <span class="guide-aux">({esc(aux_of(h))})</span>' if aux_of(h) else ''
        rows.append(f'<tr><td>{n}</td><td class="guide-char" lang="ko">{esc(h["hanja"])}</td>'
                    f'<td>{esc(h["hoondok"])}{aux}</td><td class="guide-char-sm">{esc(h.get("radical", "—"))}</td>'
                    f'<td>{h.get("totalStrokes", "—")}</td></tr>')
    lower_links = ''
    if lower:
        lows = ' · '.join(f'<a href="/grades/{SLUG[x["grade"]]}/">{x["grade"]}</a>' for x in GRADES[:i])
        lower_links = (f'<p>{name} 시험 범위에는 아래 {g["new"]:,}자에 더해 하위 급수 한자 {o["read"] - g["new"]:,}자가 '
                       f'모두 들어갑니다. 하위 급수 목록: {lows}</p>')
    faqs = [
        (f'{name} 한자는 몇 자인가요?', count_sentence),
        (f'{name} 합격 기준은 몇 문항인가요?',
         f'{o["questions"]}문항 중 {o["pass"]}문항 이상 맞히면 합격입니다. 1문항이 1점이고, 출제 문항의 {pass_percent(name)}% 이상이 기준입니다.'),
        (f'{name} 시험 시간과 검정료는 얼마인가요?',
         f'시험 시간은 {o["minutes"]}분, 검정료는 {won(o["fee"])}입니다. 2026년 정기시험에서 {name} 시험은 {start_time(name)}에 시작합니다.'),
    ]
    prev_link = f'<a href="/grades/{SLUG[lower]}/">← {lower} 한자</a>' if lower else '<span></span>'
    upper = GRADES[i + 1]['grade'] if i + 1 < len(GRADES) else None
    next_link = f'<a href="/grades/{SLUG[upper]}/">{upper} 한자 →</a>' if upper else '<span></span>'
    body = f'''      <section class="guide-block" aria-labelledby="facts-title">
        <h2 id="facts-title">{name} 한눈에 보기</h2>
        <dl class="legal-facts">{facts_html}</dl>
      </section>
      <section class="guide-block" aria-labelledby="types-title">
        <h2 id="types-title">{name} 출제 유형</h2>
        <div class="guide-table-wrap"><table class="guide-table"><caption>{name} 유형별 문항 수 (총 {o["questions"]}문항)</caption><thead><tr><th scope="col">유형</th><th scope="col">문항</th></tr></thead><tbody>{types_html}</tbody></table></div>
      </section>
      <section class="guide-block" aria-labelledby="list-title">
        <h2 id="list-title">{name}에서 새로 나오는 한자 {g["new"]:,}자</h2>
        {lower_links}
        <div class="guide-table-wrap"><table class="guide-table guide-hanja"><caption>{name} 신출 한자 {g["new"]:,}자 · 음 가나다순</caption><thead><tr><th scope="col">번호</th><th scope="col">한자</th><th scope="col">훈음</th><th scope="col">부수</th><th scope="col">총획</th></tr></thead><tbody>{''.join(rows)}</tbody></table></div>
        <p class="guide-note">훈음·부수·총획은 어흥!한자 앱 수록 데이터입니다. 괄호 안은 함께 쓰는 다른 훈음입니다. 시험 대비 때는 한국어문회 배정한자표도 함께 확인해 주세요.</p>
      </section>
      {CTA}
      {faq_html(faqs)}
      <nav class="guide-pager" aria-label="다른 급수">{prev_link}<a href="/grades/">급수 전체 보기</a>{next_link}</nav>
      <p class="guide-more"><a href="/exam-schedule/">2026 한자능력검정시험 일정 보기</a></p>
      {sources_html(['levels', 'questions', 'passRule', 'examTime', 'fee', 'cert'])}'''
    h1 = f'한자 {name} 배정한자 목록'
    write(path, shell(path, title, description, h1, esc(lead), body,
                      page_ld(url, title, description, CRUMBS[path], faqs)))

# ---------- 급수 전체 페이지 ----------
path = '/grades/'
url = f'{SITE}{path}'
CRUMBS[path] = [home_crumb, ('급수별 한자', url)]
title = '한자능력검정시험 급수별 배정한자 수·합격 기준 총정리 | 어흥!한자'
description = ('한자능력검정시험 8급 50자부터 1급 3,500자, 특급 5,978자까지 급수별 배정한자 수, 출제 문항, 합격 기준, '
               '시험 시간, 검정료를 한국어문회 공개 자료 기준으로 정리했습니다. 8급~1급은 한자 목록도 볼 수 있습니다.')
lead = ('한국어문회 한자능력검정시험은 8급부터 특급까지 15개 급수가 있습니다. 읽기 배정한자는 8급 50자, 4급 1,000자, '
        '3급 1,817자, 1급 3,500자, 특급 5,978자입니다. 상위 급수는 하위 급수 한자를 모두 포함하며, '
        '2급~8급은 출제 문항의 70% 이상, 특급·특급II·1급은 80% 이상 맞히면 합격입니다.')
rows = []
for o in reversed(official['grades']):
    name = o['grade']
    cell = f'<a href="/grades/{SLUG[name]}/">{name}</a>' if name in SLUG else name
    new = next((f'{x["new"]:,}' for x in GRADES if x['grade'] == name), '—')
    write_cell = f'{o["write"]:,}' if o['write'] else '—'
    rows.append(f'<tr><th scope="row">{cell}</th><td>{o["read"]:,}</td><td>{new}</td>'
                f'<td>{write_cell}</td><td>{o["questions"]}</td><td>{o["pass"]}</td>'
                f'<td>{o["minutes"]}분</td><td>{o["fee"]:,}원</td><td>{"공인" if o["cert"] == "공인" else "민간"}</td></tr>')
cols = official['questionTypes']['columns']
type_head = ''.join(f'<th scope="col">{c}</th>' for c in cols)
type_body = ''.join('<tr><th scope="row">' + esc(r[0]) + '</th>' + ''.join(f'<td>{v or "—"}</td>' for v in r[1:]) + '</tr>'
                    for r in official['questionTypes']['rows'])
links = ''.join(f'<li><a href="/grades/{SLUG[g["grade"]]}/"><strong>{g["grade"]}</strong> '
                f'<span>{g["cum"]:,}자 · 새로 {g["new"]:,}자</span></a></li>' for g in GRADES)
faqs = [
    ('한자능력검정시험 급수별 한자 수는 몇 자인가요?',
     '읽기 배정한자 기준으로 8급 50자, 7급II 100자, 7급 150자, 6급II 225자, 6급 300자, 5급II 400자, 5급 500자, '
     '4급II 750자, 4급 1,000자, 3급II 1,500자, 3급 1,817자, 2급 2,355자, 1급 3,500자, 특급II 4,918자, 특급 5,978자입니다.'),
    ('상위 급수에는 하위 급수 한자가 포함되나요?', '네. 상위 급수 한자는 하위 급수 한자를 모두 포함합니다.'),
    ('어느 급수부터 국가공인인가요?', '3급II부터 특급까지가 공인 급수입니다. ' + official['certNote']),
    ('몇 급을 목표로 공부하면 좋을까요?',
     '한국어문회는 초등학생은 4급, 중·고등학생은 3급, 대학생은 2급과 1급 취득을 목표로 학습하길 권합니다.'),
]
body = f'''      <section class="guide-block" aria-labelledby="table-title">
        <h2 id="table-title">급수별 배정한자 수와 합격 기준</h2>
        <div class="guide-table-wrap"><table class="guide-table guide-wide"><caption>한국어문회 공개 자료 기준 · 급수 이름을 누르면 한자 목록으로 이동합니다</caption>
          <thead><tr><th scope="col">급수</th><th scope="col">읽기 배정</th><th scope="col">새로 나오는 한자</th><th scope="col">쓰기 배정</th><th scope="col">출제 문항</th><th scope="col">합격 문항</th><th scope="col">시험 시간</th><th scope="col">검정료</th><th scope="col">자격</th></tr></thead>
          <tbody>{''.join(rows)}</tbody></table></div>
        <p class="guide-note">새로 나오는 한자 수는 어흥!한자 수록 데이터 기준이며, 누적 수가 한국어문회 읽기 배정한자 수와 같습니다. 특급·특급II 한자 목록은 이 사이트에서 제공하지 않습니다. "자격" 열은 시험 급수 자체의 공인·민간 구분이며, 어흥!한자가 받은 공인이나 인증이 아닙니다.</p>
      </section>
      <section class="guide-block" aria-labelledby="pick-title">
        <h2 id="pick-title">급수별 한자 목록 보기</h2>
        <ul class="guide-grade-grid">{links}</ul>
      </section>
      <section class="guide-block" aria-labelledby="types-title">
        <h2 id="types-title">급수별 출제 유형과 문항 수</h2>
        <div class="guide-table-wrap"><table class="guide-table guide-wide guide-types"><caption>유형별 문항 수 · — 는 출제하지 않는 유형</caption><thead><tr><th scope="col">유형</th>{type_head}</tr></thead><tbody>{type_body}</tbody></table></div>
      </section>
      {CTA}
      {faq_html(faqs)}
      <p class="guide-more"><a href="/exam-schedule/">2026 한자능력검정시험 일정 보기</a></p>
      {sources_html(['levels', 'questions', 'passRule', 'examTime', 'fee', 'cert'])}'''
write(path, shell(path, title, description, '한자능력검정시험 급수별 배정한자 수', esc(lead), body,
                  page_ld(url, title, description, CRUMBS[path], faqs)))

# ---------- 시험 일정 페이지 ----------
path = '/exam-schedule/'
url = f'{SITE}{path}'
CRUMBS[path] = [home_crumb, ('한자 시험 일정', url)]
sched = official['schedule']
rounds = sched['rounds']
upcoming = [r for r in rounds if r['examDate'] >= TODAY]
# 지난 회차가 내려간 날(시험 다음 날)을 이 페이지의 수정일로 쓴다.
EXAM_CHANGED = max([CHECKED] + [(dt.date.fromisoformat(r['examDate']) + dt.timedelta(days=1)).isoformat()
                                for r in rounds if r['examDate'] < TODAY])
if upcoming:
    r = upcoming[0]
    next_sentence = (f'다음 정기시험은 제{r["round"]}회입니다. 인터넷 접수는 {md(r["applyStart"])}~{md(r["applyEnd"])}, '
                     f'시험은 {kdate(r["examDate"])}, 합격 발표는 {md(r["resultDate"])}입니다.')
else:
    next_sentence = f'{sched["year"]}년 정기시험은 모두 끝났습니다. 다음 해 일정은 한국어문회 공지를 확인해 주세요.'
time_sentence = (f'시험은 4급~8급이 {sched["startTimes"]["4급~8급"]}, 특급~3급II가 {sched["startTimes"]["특급~3급II"]}에 시작합니다.')
lead = f'{sched["year"]}년 한자능력검정시험(한국어문회) 정기시험은 연 4회입니다. {next_sentence} {time_sentence}'
title = f'{sched["year"]} 한자능력검정시험 일정 — 접수기간·시험일·합격발표 | 어흥!한자'
description = (f'{sched["year"]}년 한자능력검정시험 정기시험 제{rounds[0]["round"]}회~제{rounds[-1]["round"]}회의 접수기간, 시험일, 시험 시각, '
               f'합격발표일을 한국어문회가 공개한 일정으로 정리했습니다. 급수별 시험 시간과 검정료, 환불 기준도 함께 확인하세요.')
NEXT_ROW = ' class="is-next"'
NEXT_BADGE = ' <span class="guide-badge">다음 시험</span>'
round_rows = ''.join(
    f'<tr{NEXT_ROW if upcoming and r is upcoming[0] else ""}><th scope="row">제{r["round"]}회{NEXT_BADGE if upcoming and r is upcoming[0] else ""}</th>'
    f'<td>{md(r["applyStart"])} ~ {md(r["applyEnd"])}</td><td>{kdate(r["examDate"])}</td><td>{kdate(r["resultDate"])}</td></tr>'
    for r in rounds)
time_rows = ''.join(f'<tr><th scope="row">{k}</th><td>{v}</td></tr>' for k, v in [
    ('특급·특급II', '100분'), ('1급', '90분'), ('2급·3급·3급II', '60분'), ('4급~8급 (4급II·5급II·6급II·7급II 포함)', '50분')])
fee_rows = ''.join(f'<tr><th scope="row">{k}</th><td>{v}</td></tr>' for k, v in [
    ('특급·특급II·1급', '50,000원'), ('2급·3급·3급II', '30,000원'), ('4급~8급 (4급II·5급II·6급II·7급II 포함)', '25,000원')])
faqs = [
    ('다음 한자능력검정시험은 언제인가요?', next_sentence),
    ('한자능력검정시험은 몇 시에 시작하나요?',
     f'{time_sentence} 응시자는 시험 시작 20분 전까지 고사실에 들어가야 합니다.'),
    ('한자능력검정시험 검정료는 얼마인가요?', '특급·특급II·1급은 50,000원, 2급·3급·3급II는 30,000원, 4급~8급은 25,000원입니다.'),
    ('접수를 취소하면 환불되나요?', official['refundRule']),
]
body = f'''      <section class="guide-block" aria-labelledby="rounds-title">
        <h2 id="rounds-title">{sched["year"]}년 정기시험 일정</h2>
        <div class="guide-table-wrap"><table class="guide-table guide-wide"><caption>한국어문회 공개 일정 · 인터넷 접수 기준</caption><thead><tr><th scope="col">회차</th><th scope="col">접수 기간</th><th scope="col">시험일</th><th scope="col">합격 발표</th></tr></thead><tbody>{round_rows}</tbody></table></div>
        <p class="guide-note">시험 시작 시각: 4급~8급 {sched["startTimes"]["4급~8급"]}, 특급~3급II {sched["startTimes"]["특급~3급II"]}. 일정은 {sched["notice"]} 접수는 <a href="{SRC["schedule"]}">한국어문회 누리집</a>에서 합니다.</p>
      </section>
      <section class="guide-block" aria-labelledby="time-title">
        <h2 id="time-title">급수별 시험 시간</h2>
        <div class="guide-table-wrap"><table class="guide-table"><caption>급수별 시험 시간 · 한국어문회 공개 자료 기준</caption><thead><tr><th scope="col">급수</th><th scope="col">시험 시간</th></tr></thead><tbody>{time_rows}</tbody></table></div>
        <p class="guide-note">{official["arrival"]}</p>
      </section>
      <section class="guide-block" aria-labelledby="fee-title">
        <h2 id="fee-title">검정료와 환불</h2>
        <div class="guide-table-wrap"><table class="guide-table"><caption>급수별 검정료 · 한국어문회 공개 자료 기준</caption><thead><tr><th scope="col">급수</th><th scope="col">검정료</th></tr></thead><tbody>{fee_rows}</tbody></table></div>
        <p class="guide-note">{official["refundRule"]}</p>
      </section>
      <section class="guide-block" aria-labelledby="next-title">
        <h2 id="next-title">시험 전에 확인할 것</h2>
        <ul class="guide-list">
          <li>내 급수의 배정한자와 합격 기준: <a href="/grades/">급수별 한자 목록</a></li>
          <li>어흥!한자 모바일 앱은 접수·시험 일정 알림을 준비하고 있습니다. 웹 베타에서는 푸시 알림을 제공하지 않습니다.</li>
        </ul>
      </section>
      {CTA}
      {faq_html(faqs)}
      {sources_html(['schedule', 'examTime', 'fee', 'cert'])}'''
write(path, shell(path, title, description, f'{sched["year"]} 한자능력검정시험 일정', esc(lead), body,
                  page_ld(url, title, description, CRUMBS[path], faqs, modified=EXAM_CHANGED)))

# ---------- 홈 구조화 데이터: 화면의 FAQ 글자 그대로 ----------
index_path = PUBLIC / 'index.html'
index = index_path.read_text()


def text_of(fragment):
    fragment = re.sub(r'<span aria-hidden="true">.*?</span>', '', fragment, flags=re.S)
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', '', fragment))).strip()


faq_block = re.search(r'<div class="faq-list">(.*?)</section>', index, flags=re.S).group(1)
home_faqs = [(text_of(q), text_of(a)) for q, a in
             re.findall(r'<summary[^>]*>(.*?)</summary>\s*<div>(.*?)</div>', faq_block, flags=re.S)]
assert len(home_faqs) >= 8, home_faqs
home_ld = ld({'@context': 'https://schema.org', '@graph': [
    ORG,
    {'@type': 'WebSite', '@id': WEBSITE_ID, 'url': f'{SITE}/', 'name': '어흥!한자', 'inLanguage': 'ko',
     'description': '한자 공부 앱 어흥!한자의 소개 사이트', 'publisher': {'@id': ORG['@id']}},
    {'@type': 'SoftwareApplication', '@id': f'{SITE}/#app', 'name': '어흥!한자',
     'applicationCategory': 'EducationalApplication', 'operatingSystem': '웹 브라우저(베타). iOS·Android 정식 출시 준비 중',
     'inLanguage': 'ko', 'url': f'{SITE}/', 'sameAs': [APP], 'image': f'{SITE}/assets/icon-512.png',
     'screenshot': f'{SITE}/assets/video/poster-motion-landscape.webp',
     'description': '한자능력검정시험 8급부터 1급까지 한자 3,500자를 읽기·뜻·쓰기·부수로 나눠 익히는 한자 공부 앱. '
                    '12시간 넘게 지난 뒤 다시 맞혀야 익힘으로 판정하고, FSRS로 복습 간격을 조절합니다.',
     'featureList': ['8급~1급 한자 3,500자, 단어 14,425개 항목', '읽기·뜻·쓰기·부수 네 칸 익힘 판정',
                     '손글씨와 획순 연습', 'FSRS 간격 반복 복습', '연상 그림과 옛이야기', '모바일 시험 일정 알림(앱 출시 준비 중)'],
     'audience': {'@type': 'EducationalAudience', 'educationalRole': 'student'},
     'author': {'@id': ORG['@id']}, 'publisher': {'@id': ORG['@id']}},
    {'@type': 'VideoObject', '@id': f'{SITE}/#film', 'name': '어흥!한자 소개 영상',
     'description': '맞히고, 쓰고, 12시간 뒤 다시 떠올리기까지. 어흥!한자의 공부를 38초에 담은 실제 웹 베타 화면 영상입니다.',
     'thumbnailUrl': f'{SITE}/assets/video/poster-motion-landscape.webp',
     'contentUrl': f'{SITE}/assets/video/hanja-motion-landscape.mp4', 'uploadDate': '2026-10-07T00:00:00+09:00',
     'duration': 'PT38S', 'inLanguage': 'ko', 'publisher': {'@id': ORG['@id']}},
    {'@type': 'FAQPage', '@id': f'{SITE}/#faq', 'mainEntity': [
        {'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in home_faqs]},
]})
start, end = '<!-- build-pages:home-ld -->', '<!-- /build-pages:home-ld -->'
new_block = f'{start}\n    <script type="application/ld+json">\n{home_ld}\n    </script>\n    {end}'
assert start in index and end in index, '홈에 구조화 데이터 표시 구역이 없다'
index = re.sub(re.escape(start) + '.*?' + re.escape(end), lambda _: new_block, index, flags=re.S)
index_path.write_text(index)

# ---------- 사이트맵 ----------
# 정적 문서의 lastmod는 내용을 고친 날짜로 직접 맞춘다.
static_pages = [('/', '2026-10-17'), ('/support', '2026-10-16'), ('/privacy', '2026-10-16'),
                ('/terms', '2026-10-21'), ('/app-terms', '2026-10-21'), ('/refund', '2026-10-08')]
generated = [('/grades/', CHECKED), ('/exam-schedule/', EXAM_CHANGED)] + [(f'/grades/{SLUG[g["grade"]]}/', CHECKED) for g in GRADES]
urls = ''.join(f'  <url><loc>{SITE}{p}</loc><lastmod>{d}</lastmod></url>\n' for p, d in static_pages + generated)
(PUBLIC / 'sitemap.xml').write_text(
    '<?xml version="1.0" encoding="UTF-8"?>\n'
    '<!-- scripts/build-pages.py가 만든다. 직접 고치지 않는다. -->\n'
    f'<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n')

# ---------- llms.txt / llms-full.txt ----------
grade_lines = '\n'.join(f'- [{g["grade"]} 한자 목록]({SITE}/grades/{SLUG[g["grade"]]}/): 읽기 배정 {g["cum"]:,}자, {g["grade"]}에서 새로 {g["new"]:,}자, '
                        f'{OFFICIAL[g["grade"]]["questions"]}문항 중 {OFFICIAL[g["grade"]]["pass"]}문항 합격' for g in GRADES)
llms = f'''# 어흥!한자

> 한자능력검정시험 8급~1급 한자 3,500자를 읽기·뜻·쓰기·부수로 나눠 익히는 한자 공부 앱의 소개 사이트입니다. 만든 곳은 썬웍스(SunWorks)입니다. 이 사이트는 한국어문회가 공개한 시험 기준(급수별 배정한자 수, 합격 기준, 시험 일정)을 출처와 확인 날짜를 붙여 정리합니다. 어흥!한자는 사단법인 한국어문회와 제휴·인증 관계가 없는 자체 제작 학습 앱입니다.

- 앱 상태: 웹 베타 공개({APP}), iOS·Android 정식 출시 준비 중
- 출시 예정 가격: 3일 체험 후 29,900원 한 번 구매, 자동 갱신 구독 없음(결제는 출시 준비 중)
- 익힘 기준: 12시간 넘게 지난 뒤 다시 맞혀야 그 칸(읽기·뜻·쓰기·부수)을 익힘으로 표시하고, 30일 동안 다시 맞히지 않으면 끕니다.
- 한국어문회 자료 확인일: {CHECKED}

## 앱 소개

- [어흥!한자 소개]({SITE}/): 학습 방식, 익힘 기준, FSRS 복습, 가격·이용 안내, 자주 묻는 질문
- [웹 베타]({APP}): 설치·가입 없이 브라우저에서 쓰는 앱. 학습 기록은 그 기기·브라우저에 저장됩니다.

## 한자능력검정시험 정보 (한국어문회 공개 자료 기준)

- [급수별 배정한자 수·합격 기준]({SITE}/grades/): 8급~특급 15개 급수의 읽기·쓰기 배정한자, 출제 문항, 합격 문항, 시험 시간, 검정료, 유형별 문항 수
- [{sched["year"]} 한자능력검정시험 일정]({SITE}/exam-schedule/): 정기시험 회차별 접수기간·시험일·합격발표, 시험 시각, 환불 기준
{grade_lines}

## 운영

- [고객지원]({SITE}/support), [개인정보 처리방침]({SITE}/privacy), [이용약관]({SITE}/terms), [앱 이용약관]({SITE}/app-terms), [취소·환불 안내]({SITE}/refund)
- 운영: 썬웍스 (https://www.sunworks.kr/), 문의 support@sunworks.kr
- 전체 데이터(급수별 한자 목록 포함): {SITE}/llms-full.txt

## 인용 안내

- 시험 기준과 일정의 원출처는 사단법인 한국어문회(https://www.hanja.re.kr)입니다. 인용할 때 확인 날짜를 함께 적어 주세요.
- 한자의 훈음·부수·총획은 어흥!한자 앱 수록 데이터입니다.
'''
(PUBLIC / 'llms.txt').write_text(llms)

full = [llms, '\n# 전체 데이터\n',
        f'\n## 급수별 기준 ({CHECKED} 확인, 출처: {SRC["levels"]}, {SRC["passRule"]}, {SRC["examTime"]}, {SRC["fee"]})\n\n',
        '| 급수 | 읽기 배정 | 쓰기 배정 | 출제 문항 | 합격 문항 | 시험 시간 | 검정료 | 자격 |\n|---|---|---|---|---|---|---|---|\n']
full += [f'| {o["grade"]} | {o["read"]:,} | {o["write"]:,} | {o["questions"]} | {o["pass"]} | {o["minutes"]}분 | {o["fee"]:,}원 | {o["cert"]} |\n'
         for o in reversed(official['grades'])]
full.append(f'\n{official["passRuleNote"]} {official["certNote"]} {official["inclusionNote"]} {official["recommendation"]}\n')
full.append(f'\n## {sched["year"]} 정기시험 일정 (출처: {SRC["schedule"]})\n\n| 회차 | 접수 | 시험일 | 합격 발표 |\n|---|---|---|---|\n')
full += [f'| 제{r["round"]}회 | {r["applyStart"]} ~ {r["applyEnd"]} | {r["examDate"]} | {r["resultDate"]} |\n' for r in rounds]
full.append(f'\n{time_sentence} {sched["notice"]} {official["refundRule"]}\n')
for g in GRADES:
    full.append(f'\n## {g["grade"]}에서 새로 나오는 한자 {g["new"]:,}자 (누적 {g["cum"]:,}자) — {SITE}/grades/{SLUG[g["grade"]]}/\n\n')
    full.append('\n'.join(f'- {h["hanja"]} {h["hoondok"]}' + (f' ({aux_of(h)})' if aux_of(h) else '') for h in g['hanja']) + '\n')
(PUBLIC / 'llms-full.txt').write_text(''.join(full))

print(f'pages: {len(GRADES) + 2}, home faqs: {len(home_faqs)}, checked: {CHECKED}')
