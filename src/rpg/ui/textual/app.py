from __future__ import annotations
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static

class RPGApp(App):
    CSS_PATH = "styles.tcss"
    BINDINGS = [("q", "quit", "Quit")]

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Static("RPG (Textual) — Press Q to quit.", id="main")
        yield Footer()

if __name__ == "__main__":
    RPGApp().run()
