class SceneManager:
    def __init__(self):
        self.scene = None

    def handle_event(self, event):
        if self.scene:
            self.scene.handle_event(event)

    def update(self):
        if self.scene:
            self.scene.update()

    def draw(self):
        if self.scene:
            self.scene.draw()

