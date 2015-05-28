import sublime, sublime_plugin
import re

PATH_REGEX = r'ui\/src\/(.*?)$'
INDEX_JS_REGEX = r'\/index\.js$'
JS_EXT_REGEX = r'(\.js)?$'

class PrcltFinderCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        find = ''

        file_name_match = re.search(PATH_REGEX, self.view.file_name())
        if file_name_match:
            file_name = file_name_match.group(1)

            file_name = re.sub(INDEX_JS_REGEX, '(\/index)?', file_name)
            file_name = re.sub(JS_EXT_REGEX, '(\.js)?', file_name)

            find = "require\('%s'\)" % file_name

        if find:
            sublime.active_window().run_command('show_panel', {'panel':'find_in_files'})
            cb = sublime.get_clipboard()
            sublime.set_clipboard(find)
            sublime.active_window().run_command('paste')
            sublime.set_clipboard(cb)
