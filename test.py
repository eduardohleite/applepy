from applepy import App, Scene, Size, Color, bindable, Binding, get_current_app, BindingExpression
from applepy.scenes import Window
from applepy.views import MainMenu, Menu, MenuItem
from applepy.views.layout import HorizontalStack, VerticalStack
from applepy.views.controls import Label, TextField, Button, Checkbox


def quit():
    get_current_app().quit()
    exit(0)


class ViewModel():
    def __init__(self) -> None:
        self._t = 0
        self._mt = 0
        self.btn_enabled = True

    @bindable(Color)
    def color(self):
        return Color.black

    @bindable(int)
    def proptest(self):
        return self._t

    @proptest.setter
    def proptest(self, val):
        self._t = val

    @bindable(int)
    def menu_title(self):
        return self._mt

    @menu_title.setter
    def menu_title(self, val):
        self._mt = val

    @bindable(bool)
    def btn_enabled(self):
        return self._be

    @btn_enabled.setter
    def btn_enabled(self, val):
        self._be = val

    def increase(self):
        self.proptest += 1
        self.menu_title += 1
        self.btn_enabled = False


class MyApp(App):
    def body(self) -> Scene:
        vm = ViewModel()

        with Window(title='Mac > Windows', size=Size(640, 480)) as w:
            with MainMenu():
                Menu(title='Edit')
                with Menu(title='File'):
                    MenuItem(title=Binding(ViewModel.menu_title, vm)
                                        .transform(lambda x: str(x)))
                with Menu(title='App'):
                    MenuItem(title='Quit', action=quit, key_equivalent='q')

            with VerticalStack():
                Label(text='The book is on the table.')
                Label(text='The show must go on.')
                Label(text='I''m not here, this isn''t happening.')
                Label(text=Binding(ViewModel.proptest, vm)
                                .transform(lambda x: str(x)))
                TextField(text=Binding(ViewModel.proptest, vm))

                with HorizontalStack():
                    Checkbox(title='yes') \
                        .is_checked(True)
                    Button(title='OK', action=vm.increase) \
                        .color(Color.system_purple) \
                        .is_enabled(BindingExpression(
                            lambda x: x < 10, (ViewModel.proptest, vm)
                        ))

            return w

MyApp().run()
