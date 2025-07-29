def draw_selection_list(*, win, items, selection_index, start_y=1, prefix_func=None):
    """
    Affiche une liste d'items avec un marqueur de sélection.
    """
    for i, item in enumerate(items):
        marker = " <--" if i == selection_index else ""
        prefix = prefix_func(i, item) if prefix_func else f"{i+1}. "
        try:
            win.addstr(start_y + i, 4, f"{prefix}{item}{marker}")
        except Exception:
            pass
    
    return start_y + len(items)
