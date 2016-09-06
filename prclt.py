import sublime
import sublime_plugin
import re
import itertools

PATH_REGEXS = [
    r'src\/(.*?)$',
    r'(?!src\/)(.*?)$',
]
INDEX_JS_REGEX = r'\/index\.js$'
JS_EXT_REGEX = r'(\.jsx?)$'


class PrcltFinderCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        arrs_of_exprs = [
            compute_file_name_regexes(self.view.file_name(), regex)
            for regex in PATH_REGEXS]

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


def compute_file_name_regexes(file_name, regex):
    file_name_match = re.search(regex, file_name)

    if not file_name_match:
        return []

    file_name = file_name_match.group(1)
    file_name = re.sub(INDEX_JS_REGEX, '(\/index(\.js)?)?', file_name)
    file_name = re.sub(JS_EXT_REGEX, '(\.jsx?)?', file_name)

    return [file_name]
