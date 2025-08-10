def draw_selection_list(*, win, items, selection_index, start_y=1, prefix_func=None, has_marker=True):
    """
    Affiche une liste d'items avec un marqueur de sélection.
    """
    y = start_y
    for i, item in enumerate(items):
        marker = " <--" if has_marker and i == selection_index else ""
        prefix = prefix_func(i, item) if prefix_func else f"{i+1}. "
        
        # On assemble le texte
        full_text = f"{prefix}{item}{marker}"
        
        # On sépare en lignes (en cas de \n)
        lines = full_text.splitlines()
        
        for line in lines:
            try:
                win.addstr(y, 4, line)
            except Exception:
                pass
            y += 1  # ligne suivante
        
    return y
