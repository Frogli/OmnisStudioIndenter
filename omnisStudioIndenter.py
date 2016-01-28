import sublime
import sublime_plugin
import re


class OmnisstudioindenterCommand(sublime_plugin.TextCommand):

    LEVEL_UPS = ['For', 'If', 'Else', 'While', 'Switch', 'Begin', 'Repeat']
    LEVEL_DOWNS = ['End', 'Until']

    def getIndentLevel(self, codeStatement, level):
        """

        :rtype: int
        """

        if codeStatement in self.LEVEL_UPS:
            level += 1
        elif codeStatement in self.LEVEL_DOWNS:
            level -= 1

        return level

    def beautifyCode(self, text):
        """
            :rtype: str
        """
        codeStatement = ''
        codeStatementMatch = ''
        indentedCode = ''
        codeList = text.splitlines(True)
        indentionSpace = '  '
        indention = ''
        level = 0

        specialStatement = False
        specialSubStatement = ['Case', 'Default']
        specialStatements = ['Switch', 'On']
        specialLevel = 0
        specialSubLevel = 0
        print (codeList)

        for codeLine in codeList:
            indention = indentionSpace * level
            codeStatementMatch = re.match('^\w+', codeLine)
            if codeStatementMatch:
                codeStatement = codeStatementMatch.group()
                level = self.getIndentLevel(codeStatement, level)
                if codeStatement in self.LEVEL_DOWNS:
                    indention = indentionSpace * level

                if codeStatement in specialStatements:
                    specialStatement = True
                    specialLevel = level - 1
                    if level == 0:
                        specialSubLevel = 1
                    else:
                        specialSubLevel = specialLevel + 1

                elif codeStatement in specialSubStatement:
                    specialSubLevel = specialLevel + 2
                    indention = indentionSpace * (specialLevel + 1)

                elif specialStatement and codeStatement not in specialStatements:
                    if re.match('^End Switch', codeLine):
                        specialStatement = False
                        indention = indentionSpace * specialLevel

                    else:
                        if codeStatement in self.LEVEL_DOWNS:
                            specialSubLevel = self.getIndentLevel(
                                codeStatement, specialSubLevel)
                            indention = indentionSpace * specialSubLevel

                        elif codeStatement in self.LEVEL_UPS:
                            indention = indentionSpace * specialSubLevel
                            specialSubLevel = self.getIndentLevel(
                                codeStatement, specialSubLevel)

                        else:
                            indention = indentionSpace * \
                                self.getIndentLevel(
                                    codeStatement, specialSubLevel)

            indentedCode = indentedCode + indention + codeLine
        return indentedCode

    def run(self, edit):
        code = ''
        bufferRegion = sublime.Region(0, self.view.size())
        bufferText = self.view.substr(bufferRegion).strip()
        if bufferText:
            code = self.beautifyCode(bufferText)
            print(code)
            self.view.replace(edit, bufferRegion, code)



