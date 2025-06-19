class AreaEvent:
    def __init__(self, name, condition_fn, effect_fn, once=True):
        self.name = name
        self.condition_fn = condition_fn  # (world_state, area) => bool
        self.effect_fn = effect_fn        # (world_state, area) => None
        self.once = once
        self.triggered = False

    def check_and_trigger(self, world_state, area):
        if self.triggered and self.once:
            return
        if self.condition_fn(world_state, area):
            self.effect_fn(world_state, area)
            self.triggered = True
