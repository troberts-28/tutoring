class Label(ppb.Sprite):
    size = 2
    layer = 1
    color = (255, 255, 255)
    text = None
    image = None

    def on_update(self, update_event, signal):
        self.image = ppb.Text(
            self.text,
            font=ppb.Font("resources/ubuntu_font/UbuntuMono-B.ttf", size=40),
            color=self.color,
        )