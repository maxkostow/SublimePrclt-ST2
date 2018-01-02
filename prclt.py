import sublime
import sublime_plugin
import re
import itertools


def extract_src(f):
    match = re.search(r'rosetta\/(src\/.*?)$', f)
    if not match:
        return None
    return match.group(1)


def extract_non_src(f):
    match = re.search(r'rosetta\/(?!src\/)(.*?)$', f)
    if not match:
        return None
    return match.group(1)


PATH_EXTRACTERS = [
    extract_src,
    extract_non_src,
]


class PrcltFinderCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        arrs_of_exprs = [
            compute_file_name_regexes(self.view.file_name(), extracter)
            for extracter in PATH_EXTRACTERS]

        flat_exprs = itertools.chain.from_iterable(arrs_of_exprs)
        exprs = list(filter(None, flat_exprs))

        if len(exprs):
            find = '|'.join(exprs)
            sublime.active_window()\
                .run_command('show_panel',
                             {'panel': 'find_in_files'})
            cb = sublime.get_clipboard()
            sublime.set_clipboard(find)
            sublime.active_window().run_command('paste')
            sublime.set_clipboard(cb)


def compute_file_name_regexes(file_name, extracter):
    file_name = extracter(file_name)

    if not file_name:
        return []

    # optional /src/
    file_name = re.sub(r'src\/', '(src\/)?', file_name)
    # optional index.js
    file_name = re.sub(r'\/index\.js$', '(\/index(.js)?)?', file_name)
    # escape other extensions
    file_name = re.sub(r'\.(.*?)$',
                       lambda m: '(\.%s)?' % m.group(1),
                       file_name)

    return [file_name]
