import sublime, sublime_plugin
import re

PRCLT_REGEX = r'(PRCLT\..*?) = '
PATH_REGEX = r'ui\/src\/(.*?)(.js)?$'

class PrcltFinderCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        find = ''


        file_name = re.search(PATH_REGEX, self.view.file_name())
        if file_name:
            find += "require\('%s'\)" % file_name.group(1)

        prclt_region = self.view.find(PRCLT_REGEX, 0)
        if prclt_region:
            prclt = re.match(PRCLT_REGEX, self.view.substr(prclt_region)).group(1)

            find += "|(%s\\b)" % prclt

        if find:
            sublime.active_window().run_command('show_panel', {'panel':'find_in_files'})
            cb = sublime.get_clipboard()
            sublime.set_clipboard(find)
            sublime.active_window().run_command('paste')
            sublime.set_clipboard(cb)
