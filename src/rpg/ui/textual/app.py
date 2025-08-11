from __future__ import annotations
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Log

class RPGApp(App):
    """UI minimaliste : un panneau de log et deux raccourcis."""
    CSS_PATH = "styles.tcss"
    BINDINGS = [
        ("e", "emit_event", "Emit test event"),
        ("q", "quit", "Quit"),
    ]

    def compose(self) -> ComposeResult:
        self.log_panel = Log(id="log", highlight=True)  # wrap retiré
        yield self.log_panel
        yield Footer()

    def on_mount(self) -> None:
        self.title = "RPG — UI (Textual) — Minimal Log"
        self.log_panel.write("UI prête. Appuie sur 'E' pour ajouter une ligne.")

    def action_emit_event(self) -> None:
        self.log_panel.write("➡️  Event simulé (on branchera l'EventBus ici à la prochaine étape).")

if __name__ == "__main__":
    RPGApp().run()
