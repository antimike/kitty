#!/usr/bin/env python
# License: GPLv3 Copyright: 2021, Kovid Goyal <kovid at kovidgoyal.net>

import datetime
import http
import json
import os
import re
import shutil
import signal
import tempfile
import zipfile
from contextlib import suppress
from typing import Any, Callable, Dict, Iterator, Match, Optional, Tuple, Union, Type
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from kitty.config import atomic_save, parse_config
from kitty.constants import cache_dir, config_dir
from kitty.options.types import Options as KittyOptions
from kitty.fast_data_types import Color
from kitty.utils import reload_conf_in_all_kitties

from ..choose.match import match

MARK_BEFORE = '\033[33m'
MARK_AFTER = '\033[39m'


def patch_conf(raw: str, theme_name: str) -> str:
    addition = f'# BEGIN_KITTY_THEME\n# {theme_name}\ninclude current-theme.conf\n# END_KITTY_THEME'
    nraw, num = re.subn(r'^# BEGIN_KITTY_THEME.+?# END_KITTY_THEME', addition, raw, flags=re.MULTILINE | re.DOTALL)
    if not num:
        if raw:
            raw += '\n\n'
        nraw = raw + addition
    # comment out all existing color definitions
    color_conf_items = (  # {{{
        # generated by gen-config.py DO NOT edit
        # ALL_COLORS_START
        'active_border_color',
        'active_tab_background',
        'active_tab_foreground',
        'background',
        'bell_border_color',
        'color0',
        'color1',
        'color10',
        'color100',
        'color101',
        'color102',
        'color103',
        'color104',
        'color105',
        'color106',
        'color107',
        'color108',
        'color109',
        'color11',
        'color110',
        'color111',
        'color112',
        'color113',
        'color114',
        'color115',
        'color116',
        'color117',
        'color118',
        'color119',
        'color12',
        'color120',
        'color121',
        'color122',
        'color123',
        'color124',
        'color125',
        'color126',
        'color127',
        'color128',
        'color129',
        'color13',
        'color130',
        'color131',
        'color132',
        'color133',
        'color134',
        'color135',
        'color136',
        'color137',
        'color138',
        'color139',
        'color14',
        'color140',
        'color141',
        'color142',
        'color143',
        'color144',
        'color145',
        'color146',
        'color147',
        'color148',
        'color149',
        'color15',
        'color150',
        'color151',
        'color152',
        'color153',
        'color154',
        'color155',
        'color156',
        'color157',
        'color158',
        'color159',
        'color16',
        'color160',
        'color161',
        'color162',
        'color163',
        'color164',
        'color165',
        'color166',
        'color167',
        'color168',
        'color169',
        'color17',
        'color170',
        'color171',
        'color172',
        'color173',
        'color174',
        'color175',
        'color176',
        'color177',
        'color178',
        'color179',
        'color18',
        'color180',
        'color181',
        'color182',
        'color183',
        'color184',
        'color185',
        'color186',
        'color187',
        'color188',
        'color189',
        'color19',
        'color190',
        'color191',
        'color192',
        'color193',
        'color194',
        'color195',
        'color196',
        'color197',
        'color198',
        'color199',
        'color2',
        'color20',
        'color200',
        'color201',
        'color202',
        'color203',
        'color204',
        'color205',
        'color206',
        'color207',
        'color208',
        'color209',
        'color21',
        'color210',
        'color211',
        'color212',
        'color213',
        'color214',
        'color215',
        'color216',
        'color217',
        'color218',
        'color219',
        'color22',
        'color220',
        'color221',
        'color222',
        'color223',
        'color224',
        'color225',
        'color226',
        'color227',
        'color228',
        'color229',
        'color23',
        'color230',
        'color231',
        'color232',
        'color233',
        'color234',
        'color235',
        'color236',
        'color237',
        'color238',
        'color239',
        'color24',
        'color240',
        'color241',
        'color242',
        'color243',
        'color244',
        'color245',
        'color246',
        'color247',
        'color248',
        'color249',
        'color25',
        'color250',
        'color251',
        'color252',
        'color253',
        'color254',
        'color255',
        'color26',
        'color27',
        'color28',
        'color29',
        'color3',
        'color30',
        'color31',
        'color32',
        'color33',
        'color34',
        'color35',
        'color36',
        'color37',
        'color38',
        'color39',
        'color4',
        'color40',
        'color41',
        'color42',
        'color43',
        'color44',
        'color45',
        'color46',
        'color47',
        'color48',
        'color49',
        'color5',
        'color50',
        'color51',
        'color52',
        'color53',
        'color54',
        'color55',
        'color56',
        'color57',
        'color58',
        'color59',
        'color6',
        'color60',
        'color61',
        'color62',
        'color63',
        'color64',
        'color65',
        'color66',
        'color67',
        'color68',
        'color69',
        'color7',
        'color70',
        'color71',
        'color72',
        'color73',
        'color74',
        'color75',
        'color76',
        'color77',
        'color78',
        'color79',
        'color8',
        'color80',
        'color81',
        'color82',
        'color83',
        'color84',
        'color85',
        'color86',
        'color87',
        'color88',
        'color89',
        'color9',
        'color90',
        'color91',
        'color92',
        'color93',
        'color94',
        'color95',
        'color96',
        'color97',
        'color98',
        'color99',
        'cursor',
        'cursor_text_color',
        'foreground',
        'inactive_border_color',
        'inactive_tab_background',
        'inactive_tab_foreground',
        'macos_titlebar_color',
        'mark1_background',
        'mark1_foreground',
        'mark2_background',
        'mark2_foreground',
        'mark3_background',
        'mark3_foreground',
        'selection_background',
        'selection_foreground',
        'tab_bar_background',
        'tab_bar_margin_color',
        'url_color',
        'visual_bell_color',
        'wayland_titlebar_color',
        # ALL_COLORS_END
    )  # }}}
    pat = fr'^\s*({"|".join(color_conf_items)})\b'
    return re.sub(pat, r'# \1', nraw, flags=re.MULTILINE)


def set_comment_in_zip_file(path: str, data: str) -> None:
    with zipfile.ZipFile(path, 'a') as zf:
        zf.comment = data.encode('utf-8')


class NoCacheFound(ValueError):
    pass


def fetch_themes(
    name: str = 'kitty-themes',
    url: str = 'https://codeload.github.com/kovidgoyal/kitty-themes/zip/master',
    cache_age: float = 1,
) -> str:
    now = datetime.datetime.now(datetime.timezone.utc)
    cache_age_delta = datetime.timedelta(days=cache_age)

    class Metadata:
        def __init__(self) -> None:
            self.etag = ''
            self.timestamp = now

        def __str__(self) -> str:
            return json.dumps({'etag': self.etag, 'timestamp': self.timestamp.isoformat()})

    dest_path = os.path.join(cache_dir(), f'{name}.zip')
    m = Metadata()
    with suppress(Exception), zipfile.ZipFile(dest_path, 'r') as zf:
        q = json.loads(zf.comment)
        m.etag = str(q.get('etag') or '')
        m.timestamp = datetime.datetime.fromisoformat(q['timestamp'])
        if cache_age < 0 or (now - m.timestamp) < cache_age_delta:
            return dest_path
    if cache_age < 0:
        raise NoCacheFound('No local themes cache found and negative cache age specified, aborting')

    rq = Request(url)
    m.timestamp = now
    if m.etag:
        rq.add_header('If-None-Match', m.etag)
    try:
        res = urlopen(rq, timeout=30)
    except HTTPError as e:
        if m.etag and e.code == http.HTTPStatus.NOT_MODIFIED:
            set_comment_in_zip_file(dest_path, str(m))
            return dest_path
        raise
    m.etag = res.headers.get('etag') or ''

    needs_delete = False
    try:
        with tempfile.NamedTemporaryFile(suffix=f'-{os.path.basename(dest_path)}', dir=os.path.dirname(dest_path), delete=False) as f:
            needs_delete = True
            shutil.copyfileobj(res, f)
            f.flush()
            set_comment_in_zip_file(f.name, str(m))
            os.replace(f.name, dest_path)
            needs_delete = False
    finally:
        if needs_delete:
            os.unlink(f.name)
    return dest_path


def zip_file_loader(path_to_zip: str, theme_file_name: str, file_name: str) -> Callable[[], str]:

    name = os.path.join(os.path.dirname(theme_file_name), file_name)

    def zip_loader() -> str:
        with zipfile.ZipFile(path_to_zip, 'r') as zf, zf.open(name) as f:
            return f.read().decode('utf-8')

    return zip_loader


def theme_name_from_file_name(fname: str) -> str:
    ans = fname.rsplit('.', 1)[0]
    ans = ans.replace('_', ' ')

    def camel_case(m: 'Match[str]') -> str:
        return f'{m.group(1)} {m.group(2)}'

    ans = re.sub(r'([a-z])([A-Z])', camel_case, ans)
    return ' '.join(x.capitalize() for x in filter(None, ans.split()))


class LineParser:

    def __init__(self) -> None:
        self.in_metadata = False
        self.in_blurb = False
        self.keep_going = True

    def __call__(self, line: str, ans: Dict[str, Any]) -> None:
        is_block = line.startswith('## ')
        if self.in_metadata and not is_block:
            self.keep_going = False
            return
        if not self.in_metadata and is_block:
            self.in_metadata = True
        if not self.in_metadata:
            return
        line = line[3:]
        if self.in_blurb:
            ans['blurb'] += ' ' + line
            return
        try:
            key, val = line.split(':', 1)
        except Exception:
            self.keep_going = False
            return
        key = key.strip().lower()
        val = val.strip()
        if val:
            ans[key] = val
        if key == 'blurb':
            self.in_blurb = True


def parse_theme(fname: str, raw: str, exc_class: Type[BaseException] = SystemExit) -> Dict[str, Any]:
    lines = raw.splitlines()
    conf = parse_config(lines)
    bg: Color = conf.get('background', Color())
    is_dark = max((bg.red, bg.green, bg.blue)) < 115
    ans: Dict[str, Any] = {'name': theme_name_from_file_name(fname)}
    parser = LineParser()
    for i, line in enumerate(raw.splitlines()):
        line = line.strip()
        if not line:
            continue
        try:
            parser(line, ans)
        except Exception as e:
            raise exc_class(
                f'Failed to parse {fname} line {i+1} with error: {e}')
        if not parser.keep_going:
            break
    if is_dark:
        ans['is_dark'] = True
    ans['num_settings'] = len(conf) - len(parse_config(()))
    if ans['num_settings'] < 1 and fname != 'default.conf':
        raise exc_class(f'The theme {fname} has no settings')
    return ans


def update_theme_file(path: str) -> bool:
    with open(path) as f:
        raw = f.read()
    td = parse_theme(os.path.basename(path), raw, exc_class=ValueError)
    if 'upstream' not in td:
        return False
    nraw = urlopen(td['upstream']).read().decode('utf-8')
    if raw == nraw:
        return False
    atomic_save(nraw.encode('utf-8'), path)
    return True


class Theme:
    name: str = ''
    author: str = ''
    license: str = ''
    is_dark: bool = False
    blurb: str = ''
    num_settings: int = 0

    def apply_dict(self, d: Dict[str, Any]) -> None:
        self.name = str(d['name'])
        for x in ('author', 'license', 'blurb'):
            a = d.get(x)
            if isinstance(a, str):
                setattr(self, x, a)
        for x in ('is_dark', 'num_settings'):
            a = d.get(x)
            if isinstance(a, int):
                setattr(self, x, a)

    def __init__(self, loader: Callable[[], str]):
        self._loader = loader
        self._raw: Optional[str] = None
        self._opts: Optional[KittyOptions] = None

    @property
    def raw(self) -> str:
        if self._raw is None:
            self._raw = self._loader()
        return self._raw

    @property
    def kitty_opts(self) -> KittyOptions:
        if self._opts is None:
            self._opts = KittyOptions(options_dict=parse_config(self.raw.splitlines()))
        return self._opts

    def save_in_dir(self, dirpath: str) -> None:
        atomic_save(self.raw.encode('utf-8'), os.path.join(dirpath, f'{self.name}.conf'))

    def save_in_conf(self, confdir: str, reload_in: str, config_file_name: str = 'kitty.conf') -> None:
        os.makedirs(confdir, exist_ok=True)
        atomic_save(self.raw.encode('utf-8'), os.path.join(confdir, 'current-theme.conf'))
        confpath = os.path.realpath(os.path.join(confdir, config_file_name))
        try:
            with open(confpath) as f:
                raw = f.read()
        except FileNotFoundError:
            raw = ''
        nraw = patch_conf(raw, self.name)
        if raw:
            with open(f'{confpath}.bak', 'w') as f:
                f.write(raw)
        atomic_save(nraw.encode('utf-8'), confpath)
        if reload_in == 'parent':
            if 'KITTY_PID' in os.environ:
                os.kill(int(os.environ['KITTY_PID']), signal.SIGUSR1)
        elif reload_in == 'all':
            reload_conf_in_all_kitties()


class Themes:

    def __init__(self) -> None:
        self.themes: Dict[str, Theme] = {}
        self.index_map: Tuple[str, ...] = ()

    def __len__(self) -> int:
        return len(self.themes)

    def __iter__(self) -> Iterator[Theme]:
        return iter(self.themes.values())

    def __getitem__(self, key: Union[int, str]) -> Theme:
        if isinstance(key, str):
            return self.themes[key]
        if key < 0:
            key += len(self.index_map)
        return self.themes[self.index_map[key]]

    def load_from_zip(self, path_to_zip: str) -> None:
        with zipfile.ZipFile(path_to_zip, 'r') as zf:
            for name in zf.namelist():
                if os.path.basename(name) == 'themes.json':
                    theme_file_name = name
                    with zf.open(theme_file_name) as f:
                        items = json.loads(f.read())
                    break
            else:
                raise ValueError(f'No themes.json found in {path_to_zip}')

            for item in items:
                t = Theme(zip_file_loader(path_to_zip, theme_file_name, item['file']))
                t.apply_dict(item)
                if t.name:
                    self.themes[t.name] = t

    def load_from_dir(self, path: str) -> None:
        if not os.path.isdir(path):
            return
        for name in os.listdir(path):
            if name.endswith('.conf'):
                with open(os.path.join(path, name), 'rb') as f:
                    raw = f.read().decode()
                try:
                    d = parse_theme(name, raw)
                except (Exception, SystemExit):
                    continue
                t = Theme(raw.__str__)
                t.apply_dict(d)
                if t.name:
                    self.themes[t.name] = t

    def filtered(self, is_ok: Callable[[Theme], bool]) -> 'Themes':
        ans = Themes()

        def sort_key(k: Tuple[str, Theme]) -> str:
            return k[1].name.lower()

        ans.themes = {k: v for k, v in sorted(self.themes.items(), key=sort_key) if is_ok(v)}
        ans.index_map = tuple(ans.themes)
        return ans

    def copy(self) -> 'Themes':
        ans = Themes()
        ans.themes = self.themes.copy()
        ans.index_map = self.index_map
        return ans

    def apply_search(
        self, expression: str, mark_before: str = MARK_BEFORE, mark_after: str = MARK_AFTER
    ) -> Iterator[str]:
        raw = '\n'.join(self.themes)
        results = match(raw, expression, positions=True, level1=' ')
        themes: Dict[str, Theme] = {}
        for r in results:
            pos, k = r.split(':', 1)
            positions = tuple(map(int, pos.split(',')))
            text = k
            for p in reversed(positions):
                text = text[:p] + mark_before + text[p] + mark_after + text[p+1:]
            themes[k] = self.themes[k]
            yield text
        self.themes = themes
        self.index_map = tuple(self.themes)


def load_themes(cache_age: float = 1., ignore_no_cache: bool = False) -> Themes:
    ans = Themes()
    try:
        fetched = fetch_themes(cache_age=cache_age)
    except NoCacheFound:
        if not ignore_no_cache:
            raise
    else:
        ans.load_from_zip(fetched)
    ans.load_from_dir(os.path.join(config_dir, 'themes'))
    ans.index_map = tuple(ans.themes)
    return ans
