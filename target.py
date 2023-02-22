from applepy import App, View, Scene, Color
from applepy.scenes import Window
from applepy.views.layout import VStack
from applepy.views.controls import Image, ImageScale, Text


class ContentView(View):
    def body(self) -> View:
        with VStack as v:
            Image(system_name='globe') \
                .image_scale(ImageScale.large) \
                .foreground_color(Color.accent_color)
            Text('Hello, world!')
            v.padding()


class MyApp(App):
    def body(self) -> Scene:
        with Window():
            ContentView()


MyApp().run()
