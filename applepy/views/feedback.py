from typing import Optional, Any, Tuple, List

from ..backend.app_kit import NSAlert, NSOpenPanel, NSSavePanel, UTType, NSURL
from ..base.types import AlertStyle, AlertResponse, Image, DialogResponse


class Alert:
    """ Class that represents a MacOS native Alert modal """

    def __init__(self, *,
                       style: AlertStyle,
                       informative_text: str,
                       message_text: str,
                       buttons: Optional[Tuple[str]] = None,
                       custom_image: Optional[Image]=None) -> None:
        """
        Create a new custom `Alert` modal. For common alert modals, use the shortcut
        methods `show_info`, `show_error`, `show_warning`, `show_question` or `show_confirmation`.

        Args:
            style (AlertStyle): Style of the alert modal.
            informative_text (str): Informative text / title of the alert modal.
            message_text (str): Message text / question of the alert modal.
            buttons (Optional[Tuple[str]], optional): Buttons that should be displayed by the modal. None adds an `Ok` button. Defaults to None.
            custom_image (Optional[Image], optional): Custom image to display as the modal's icon. None displays the App's icon. Defaults to None.
        """        
        self.alert = NSAlert.alloc().init()
        self.alert.alertStyle = style.value
        self.alert.informativeText = informative_text
        self.alert.messageText = message_text

        if custom_image:
            self.alert.icon = custom_image.value

        if buttons:
            for btn in buttons:
                self.alert.addButtonWithTitle_(btn)

    def show(self) -> AlertResponse:
        """
        Show the modal alert.

        Returns:
            AlertResponse: User response.
        """        
        res = self.alert.runModal()
        return AlertResponse(res)

    @classmethod
    def show_info(cls, *,
                       informative_text: str,
                       message_text: str,
                       custom_image: Optional[Image]=None) -> AlertResponse:
        """
        Display an informational alert with an `Ok` button.
        Example:
        >>> Alert.show_info('Done', 'Done processing document.')

        Args:
            informative_text (str): Title / Informative text of the alert.
            message_text (str): Message text of the alert.
            custom_image (Optional[Image], optional): Custom image to display as the modal's icon. None displays the App's icon. Defaults to None.

        Returns:
            AlertResponse: User response.
        """                       
        alert = cls(style=AlertStyle.informational,
                    informative_text=informative_text,
                    message_text=message_text,
                    buttons=None,
                    custom_image=custom_image)
        return alert.show()

    @classmethod
    def show_error(cls, *,
                        informative_text: str,
                        message_text: str,
                        custom_image: Optional[Image]=None) -> AlertResponse:
        """
        Display a critial alert with an `Ok` button.
        Example:
        >>> Alert.show_error('Error', 'Failed to process document.')

        Args:
            informative_text (str): Title / Informative text of the alert.
            message_text (str): Message text of the alert.
            custom_image (Optional[Image], optional): Custom image to display as the modal's icon. None displays the App's icon. Defaults to None.

        Returns:
            AlertResponse: User response.
        """        
        alert = cls(style=AlertStyle.critical,
                    informative_text=informative_text,
                    message_text=message_text,
                    buttons=None,
                    custom_image=custom_image)
        return alert.show()

    @classmethod
    def show_warning(cls, *
                          informative_text: str,
                          message_text: str,
                          custom_image: Optional[Image]=None) -> AlertResponse:
        """
        Display a warning alert with an `Ok` button.
        Example:
        >>> Alert.show_warning('Done', 'Done processing document. However, some sections failed.')

        Args:
            informative_text (str): Title / Informative text of the alert.
            message_text (str): Message text of the alert.
            custom_image (Optional[Image], optional): Custom image to display as the modal's icon. None displays the App's icon. Defaults to None.

        Returns:
            AlertResponse: User response.
        """                          
        alert = cls(style=AlertStyle.warning,
                    informative_text=informative_text,
                    message_text=message_text,
                    buttons=None,
                    custom_image=custom_image)
        return alert.show()

    @classmethod
    def show_question(cls, *,
                           title: str,
                           question: str,
                           custom_image: Optional[Image]=None) -> AlertResponse:
        """
        Display an informational alert with a question and two buttons: `Yes` and `No`.
        Example:
        >>> Alert.show_question('Quit', 'Are you sure you want to quit?')

        The button clicked by the user is identified in the method's response.
        >>> if Alert.show_question('Quit', 'Are you sure you want to quit?') == AlertResponse.yes:
                self.quit()

        Args:
            title (str): Title of the alert.
            question (str): Question as the message text of the alert.
            custom_image (Optional[Image], optional): Custom image to display as the modal's icon. None displays the App's icon. Defaults to None.

        Returns:
            AlertResponse: User response.
        """                           
        alert = cls(style=AlertStyle.informational,
                    informative_text=title,
                    message_text=question,
                    buttons=('Yes', 'No'),
                    custom_image=custom_image)
        return alert.show()

    @classmethod
    def show_confirmation(cls, *,
                               title: str,
                               question: str,
                               custom_image: Optional[Image]=None) -> AlertResponse:
        """
        Display an informational alert with a question and two buttons: `Ok` and `Cancel`.
        Example:
        >>> Alert.show_confirmation('Processing document', 'Continue to process the document?')

        The button clicked by the user is identified in the method's response.
        >>> if Alert.show_confirmation('Processing document', 'Continue to process the document?') == AlertResponse.ok:
                self.process_document()

        Args:
            title (str): Title of the alert.
            question (str): Question as the message text of the alert.
            custom_image (Optional[Image], optional): Custom image to display as the modal's icon. None displays the App's icon. Defaults to None.

        Returns:
            AlertResponse: User response.
        """      
        alert = cls(style=AlertStyle.warning,
                    informative_text=title,
                    message_text=question,
                    buttons=('Ok', 'Cancel'),
                    custom_image=custom_image)
        return alert.show()


class SaveDialog:
    """ Class that represents a Macos native SavePanel """

    def __new__(cls, **kwargs) -> Any:
        """
        Instantiate a new `SaveDialog`

        Returns:
            SaveDialog: self
        """
        obj = object.__new__(cls)
        obj.dialog = NSSavePanel.savePanel()
        return obj

    def __init__(self,
                 *,
                 title: str,
                 initial_path: Optional[str]=None,
                 allowed_extensions: Optional[Tuple[str]]=None,
                 prompt: Optional[str]=None,
                 message: Optional[str]=None,
                 can_create_directories: bool=False,
                 can_show_all_extensions: bool=False,
                 expanded: bool=False) -> None:
        """
        Create a new custom `SaveDialog` modal. For common file saving modals, use one of the shortcut
        methods in the `FileDialog` class.

        Args:
            title (str): Title of the modal.
            initial_path (Optional[str], optional): Initial directory path. Defaults to None.
            allowed_extensions (Optional[Tuple[str]], optional): Extensions allowed in the modal. Defaults to None.
            prompt (Optional[str], optional): Modal's prompt button text. Defaults to None.
            message (Optional[str], optional): Message text of the modal. Defaults to None.
            can_create_directories (bool, optional): Whether the user can create directories in the modal. Defaults to False.
            can_show_all_extensions (bool, optional): Whether the modal will allow the user to show all extensions. Defaults to False.
            expanded (bool, optional): Whether the modal will be expanded. Defaults to False.
        """
        self.dialog.title = title
        self.dialog.message = message or ''
        self.dialog.canCreateDirectories = can_create_directories
        self.dialog.canSelectHiddenExtension = can_show_all_extensions
        self.dialog.expanded = expanded

        if prompt:
            self.dialog.prompt = prompt

        if allowed_extensions:
            self.dialog.allowedContentTypes = [UTType.typeWithFilenameExtension(e) for e in allowed_extensions]

        if initial_path:
            self.dialog.directoryURL = NSURL.fileURLWithPath_isDirectory_(initial_path, True)

    @property
    def path(self) -> Optional[str]:
        """
        Path selected in the dialog, if any.

        Returns:
            Optional[str]: Path selected in the dialog as string if any. None otherwise.
        """        
        return str(self.dialog.URL.path) if self.dialog.URL else None

    def show(self) -> DialogResponse:
        """
        Displays the dialog as modal.

        Returns:
            DialogResponse: The user response
        """        
        res = self.dialog.runModal()
        return DialogResponse(res)


class OpenDialog(SaveDialog):
    """ Class that represents a Macos native OpenPanel """

    def __new__(cls, **kwargs) -> Any:
        """
        Instantiate a new `OpenDialog`

        Returns:
            OpenDialog: self
        """
        obj = object.__new__(cls)
        obj.dialog = NSOpenPanel.openPanel()
        return obj

    def __init__(self,
                 *,
                 title: str,
                 initial_path: Optional[str]=None,
                 allowed_extensions: Optional[Tuple[str]]=None,
                 prompt: Optional[str]=None,
                 message: Optional[str]=None,
                 can_choose_files: bool=True,
                 can_choose_directories: bool=False,
                 resolve_aliases: bool=True,
                 allow_multiple_selection: bool=False,
                 can_create_directories: bool=False,
                 can_show_all_extensions: bool=False,
                 expanded: bool=False) -> None:
        """
        Create a new custom `OpenDialog` modal. For common file or directory open modals, use one of the shortcut
        methods in the `FileDialog` class.

        Args:
            title (str): Title of the modal.
            initial_path (Optional[str], optional): Initial directory path. Defaults to None.
            allowed_extensions (Optional[Tuple[str]], optional): Extensions allowed in the modal. Defaults to None.
            prompt (Optional[str], optional): Modal's prompt button text. Defaults to None.
            message (Optional[str], optional): Message text of the modal. Defaults to None.
            can_choose_files (bool, optional): Whether the user can select files in the modal. Defaults to True.
            can_choose_directories (bool, optional): Whether the user can select directories in the modal. Defaults to False.
            resolve_aliases (bool, optional): Whether the modal will resolve aliases when selecting directories. Defaults to True.
            allow_multiple_selection (bool, optional): Whether the user can select multiple files in the modal. Defaults to False.
            can_create_directories (bool, optional): Whether the user can create directories in the modal. Defaults to False.
            can_show_all_extensions (bool, optional): Whether the modal will allow the user to show all extensions. Defaults to False.
            expanded (bool, optional): Whether the modal will be expanded. Defaults to False.
        """
        super().__init__(title=title,
                         initial_path=initial_path,
                         allowed_extensions=allowed_extensions,
                         prompt=prompt,
                         message=message,
                         can_create_directories=can_create_directories,
                         can_show_all_extensions=can_show_all_extensions,
                         expanded=expanded)

        self.dialog.canChooseFiles = can_choose_files
        self.dialog.canChooseDirectories = can_choose_directories
        self.dialog.resolvesAliases = resolve_aliases
        self.dialog.allowsMultipleSelection = allow_multiple_selection
        self.dialog.resolvesAliases = resolve_aliases

    @property
    def paths(self) -> List[str]:
        """
        Paths selected in the dialog, if any.

        Returns:
            List[str]: Paths selected in the dialog as string if any. An empty list otherwise.
        """ 
        return [str(url.path) for url in self.dialog.URLs] if self.dialog.URLs else [] 


class FileDialog:
    """ Class with utility shortcut methods for creating `OpenDialog` and `SaveDialog` objects for common tasks."""

    @staticmethod
    def open_file(*,
                  title: str,
                  message: Optional[str]=None,
                  extensions: Optional[Tuple[str]]=None,
                  initial_path: Optional[str]=None) -> Tuple[DialogResponse, Optional[str]]:
        """
        Display an `OpenDialog` modal that allows user to choose a single file.

        Args:
            title (str): Title of the modal.
            message (Optional[str], optional): Message text of the modal. Defaults to None.
            extensions (Optional[Tuple[str]], optional): Extensions allowed in the modal. Defaults to None.
            initial_path (Optional[str], optional):  Initial directory path. Defaults to None.

        Returns:
            Tuple[DialogResponse, Optional[str]]: Tuple containing the user's response and the path to the
            selected file if any. None otherwise.
        """        
        dialog = OpenDialog(title=title,
                            message=message,
                            allowed_extensions=extensions,
                            initial_path=initial_path)
        response = dialog.show()
        selected = None

        if response == DialogResponse.continue_:
            selected = dialog.path

        return response, selected

    @staticmethod
    def open_files(*,
                   title: str,
                   message: Optional[str]=None,
                   extensions: Optional[Tuple[str]]=None,
                   initial_path: Optional[str]=None) -> Tuple[DialogResponse, List[str]]:
        """
        Display an `OpenDialog` modal that allows user to choose multiple files.

        Args:
            title (str): Title of the modal.
            message (Optional[str], optional): Message text of the modal. Defaults to None.
            extensions (Optional[Tuple[str]], optional): Extensions allowed in the modal. Defaults to None.
            initial_path (Optional[str], optional): Initial directory path. Defaults to None.

        Returns:
            Tuple[DialogResponse, List[str]]: Tuple containing the user's response and a list of the paths
            to the selected files if any. An empty list otherwise.
        """        
        dialog = OpenDialog(title=title,
                            message=message,
                            allow_multiple_selection=True,
                            allowed_extensions=extensions,
                            initial_path=initial_path)
        response = dialog.show()
        selected = []

        if response == DialogResponse.continue_:
            selected = dialog.paths

        return response, selected

    @staticmethod
    def open_dir(*,
                 title: str,
                 message: Optional[str]=None,
                 initial_path: Optional[str]=None) -> Tuple[DialogResponse, Optional[str]]:
        """
        Display an `OpenDialog` modal that allows user to choose a single directory.

        Args:
            title (str): Title of the modal.
            message (Optional[str], optional): Message text of the modal. Defaults to None.
            initial_path (Optional[str], optional):  Initial directory path. Defaults to None.

        Returns:
            Tuple[DialogResponse, Optional[str]]: Tuple containing the user's response and the path to the
            selected folder if any. None otherwise.
        """        
        dialog = OpenDialog(title,
                            can_choose_files=False,
                            can_choose_directories=True,
                            can_create_directories=True,
                            message=message,
                            initial_path=initial_path)
        response = dialog.show()
        selected = None

        if response == DialogResponse.continue_:
            selected = dialog.path

        return response, selected

    @staticmethod
    def save_file(*,
                  title: str,
                  message: Optional[str]=None,
                  extensions: Optional[Tuple[str]]=None,
                  initial_path: Optional[str]=None) -> Tuple[DialogResponse, Optional[str]]:
        """
        Display an `SaveDialog` modal that allows user to choose a single file.

        Args:
            title (str): Title of the modal.
            message (Optional[str], optional): Message text of the modal. Defaults to None.
            extensions (Optional[Tuple[str]], optional): Extensions allowed in the modal. Defaults to None.
            initial_path (Optional[str], optional):  Initial directory path. Defaults to None.

        Returns:
            Tuple[DialogResponse, Optional[str]]: Tuple containing the user's response and the path to the
            selected file if any. None otherwise.
        """        
        dialog = SaveDialog(title=title,
                            message=message,
                            allowed_extensions=extensions,
                            initial_path=initial_path)
        response = dialog.show()
        selected = []

        if response == DialogResponse.continue_:
            selected = dialog.path

        return response, selected
