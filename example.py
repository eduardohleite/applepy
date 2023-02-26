from applepy import App, Scene, Size, Binding, Color, bindable, Alignment, Image
from applepy.scenes import Window
from applepy.views.layout import VerticalStack, HorizontalStack, Spacer
from applepy.views.controls import Label, ImageButton, Checkbox
from applepy.views.feedback import Alert, AlertResponse


class Sample(App):
    def __init__(self) -> None:
        super().__init__()
        self._should_i_go = False

    @bindable(bool)
    def should_i_go(self) -> bool:
        return self._should_i_go

    @should_i_go.setter
    def should_i_go(self, value: bool) -> None:
        self._should_i_go = value

    def quit_clicked(self) -> None:
        if Alert.show_question('Quit', 'Are you sure you want to quit?') == AlertResponse.yes:
            self.quit()
            exit(0)

    def body(self) -> Scene:
        with Window(title='Applepy example', size=Size(640, 480), closable=False) as w:
            with VerticalStack(alignment=Alignment.left) as vs:
                with HorizontalStack() as hs:
                    Label(text=Binding(Window.size, w).transform(lambda x: f'{x.width}:{x.height}'))
                    Label(text=Binding(Window.position, w).transform(lambda x: f'({x.x}, {x.y})'))

                Label(text=Binding(Window.full_screen, w).transform(lambda x: f'is full screen: {"T" if x else "F"}'))

                with HorizontalStack():
                    chk = Checkbox(title='Should I stay or should I go?') \
                        .set_state(Binding(Sample.should_i_go, self))
                    Label(text=Binding(Checkbox.state, chk).transform(lambda x: 'go' if x else 'stay')) \
                        .set_text_color(Binding(Checkbox.state, chk)
                                .transform(lambda x: Color.system_green if x else Color.system_red))

                Spacer()

                with HorizontalStack():
                    Spacer()
                    ImageButton(title='Quit',
                                image=Image.from_system('NSStopProgressFreestandingTemplate'),
                                action=self.quit_clicked) \
                        .set_bezel_color(Color.system_red)

                vs.set_padding()
            return w.center()

Sample().run()
