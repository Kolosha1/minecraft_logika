from ursina import*

Text.default_font = "assets\\PressStart2P-Regular.ttf"

class MenuButton(Button):
    def __init__(self, text, action, x, y, parent):
        super().__init__(text=text, on_click=action, x=x, y=y, parent=parent,
                         scale=(0.6, 0.1),
                         origin=(0, 0),
                         ignore_paused=True,
                         texture='assets\\block_textures\\stone.png',
                         color=color.color(0, 0, random.uniform(0.9, 1)),
                         highlight_color=color.gray,
                         highlight_scale=1.05,
                         pressed_scale=1.05,
                         )


class Menu(Entity):
    def __init__(self, game, **kwargs):
        game.menu = self
        super().__init__(parent=camera.ui, ignore_paused=True, **kwargs)
        self.bg = Sprite(texture='assets\\menu_bg.png',
                         parent=self, z=1, color=color.white, scale=0.1)
        self.title = Text(text="LogikaCraft", scale=5,
                          parent=self, origin=(0, 0), x=0, y=0.35)
        
        MenuButton("Нова гра", game.generate, 0,0,self)
        MenuButton("Завантажити гру", application.quit, 0,0.02,self)
        MenuButton("Зберегти гру", application.quit, 0,-0.11,self)
        MenuButton("Вихід з гри", application.quit, 0,-0.24,self)

    def toggle_menu(self):
        application.paused = not application.paused
        self.enabled = application.paused
        self.visible = self.visible
        mouse.locked = not mouse.locked
        mouse.visible = not mouse.visible


if __name__ == "__main__":
    app = Ursina()
    menu = Menu(app)
    app.run()