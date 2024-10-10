from prompt_toolkit import Application
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout import Layout, ScrollOffsets, FormattedTextControl, Window, HSplit


class MenuSelection:
    def __init__(self, options, visible_items=10):
        self.options = options
        self.cursor_index = 0
        self.visible_items = visible_items
        self.scroll_offset = 0
        self.kb = KeyBindings()

        @self.kb.add('up')
        def up_key(event):
            self.cursor_index = max(0, self.cursor_index - 1)
            self._adjust_scroll()
            self.update_display()

        @self.kb.add('down')
        def down_key(event):
            self.cursor_index = min(len(self.options) - 1, self.cursor_index + 1)
            self._adjust_scroll()
            self.update_display()

        @self.kb.add('pageup')
        def pageup_key(event):
            self.cursor_index = max(0, self.cursor_index - self.visible_items)
            self._adjust_scroll()
            self.update_display()

        @self.kb.add('pagedown')
        def pagedown_key(event):
            self.cursor_index = min(len(self.options) - 1, self.cursor_index + self.visible_items)
            self._adjust_scroll()
            self.update_display()

        @self.kb.add('enter')
        def enter_key(event):
            event.app.exit(result=self.options[self.cursor_index])

        @self.kb.add('q')
        def quit_key(event):
            event.app.exit(result=None)

    def _adjust_scroll(self):
        if self.cursor_index < self.scroll_offset:
            self.scroll_offset = self.cursor_index
        elif self.cursor_index >= self.scroll_offset + self.visible_items:
            self.scroll_offset = self.cursor_index - self.visible_items + 1

    def create_menu_text(self):
        lines = []
        visible_options = self.options[self.scroll_offset:self.scroll_offset + self.visible_items]

        for idx, option in enumerate(visible_options, start=self.scroll_offset):
            cursor = '>' if idx == self.cursor_index else ' '
            lines.append(f'{cursor} {option}')

        if self.scroll_offset > 0:
            lines.insert(0, '▲ More options above')
        if self.scroll_offset + self.visible_items < len(self.options):
            lines.append('▼ More options below')

        return '\n'.join(lines)

    def update_display(self):
        self.menu_window.content.text = self.create_menu_text()

    def run(self):
        self.menu_window = Window(
            content=FormattedTextControl(''),
            height=self.visible_items + 2,
            scroll_offsets=ScrollOffsets(top=1, bottom=1)
        )
        self.update_display()

        layout = Layout(
            HSplit([
                Window(
                    height=1,
                    content=FormattedTextControl(
                        'Use ↑↓/PgUp/PgDn to move, Enter to select, q to quit'
                    )
                ),
                Window(height=1),  # Spacer
                self.menu_window,
            ])
        )

        app = Application(
            layout=layout,
            key_bindings=self.kb,
            full_screen=True,
        )

        return app.run()
