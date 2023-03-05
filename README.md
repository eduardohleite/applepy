# applepy

Applepy is a UI library inspired by Swift UI that leverages AppKit and UIKit to create native MacOS, iOS and iPadOS user interfaces in the Python programming language with a declarative syntax.

*This project is at proof of concept stage and is not feature complete. Please do not use it in production.* 

## Dependencies

* [rubicon-objc](https://github.com/beeware/rubicon-objc)
* [pydispatcher](https://github.com/mcfletch/pydispatcher)

## Installation

The latest version is available for installation in PyPI:
>pip install applepy-ui

## Usage

```python
class Sample(App):
    def body(self) -> Scene:
        with Window(title='Applepy example', size=Size(640, 100)) as w:
            with VerticalStack():
                with HorizontalStack():
                    Label(text='Hello')
                    Label(text='World')
                
            return w.center()
Sample().run()
```

![image](https://github.com/eduardohleite/applepy/blob/master/screenshot.png)


It also works on mobile:


```python
class MobileSample(App):
    def body(self):
        with SimpleScreen() as s:
            with HorizontalStack():
                with VerticalStack():
                    Label(text='Hello World')
            return s

def main():
    sys.exit(MobileSample().run())
```

<img src="https://github.com/eduardohleite/applepy/blob/master/screenshot-mobile.png" height="600">


Events can be handled synchronously and asynchronously in the same context:


```python
class AsyncSample(App):
    def clicked(self) -> None:
        time.sleep(2)
        Alert.show_info(informative_text='Hello', message_text='Synchronous World')

    async def clicked_async(self) -> None:
        await asyncio.sleep(2)
        Alert.show_info(informative_text='Hello', message_text='Asynchronous World')

    def body(self) -> Scene:
        with Window(title='Applepy async example', size=Size(640,480)) as w:
            with HorizontalStack():
                with VerticalStack():
                    Button(title='Sync action', action=self.clicked)
                    Button(title='Async action', action=self.clicked_async)
                return w.center()

AsyncSample().run_async()
```

For a more complete example, please check [example.py](example.py)
