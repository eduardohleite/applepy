from typing import Optional, Tuple

from ..backend.app_kit import NSAlert, NSOpenPanel, NSSavePanel, UTType, NSURL
from ..base.types import AlertStyle, AlertResponse, Image


class Alert:
    """ Class that represents a MacOS native Alert modal """

    def __init__(self, style: AlertStyle,
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
    def show_info(cls, informative_text: str,
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
        alert = cls(AlertStyle.informational,
                    informative_text,
                    message_text,
                    None,
                    custom_image)
        return alert.show()

    @classmethod
    def show_error(cls, informative_text: str,
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
        alert = cls(AlertStyle.critical,
                    informative_text,
                    message_text,
                    None,
                    custom_image)
        return alert.show()

    @classmethod
    def show_warning(cls, informative_text: str,
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
        alert = cls(AlertStyle.warning,
                    informative_text,
                    message_text,
                    None,
                    custom_image)
        return alert.show()

    @classmethod
    def show_question(cls, title: str,
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
        alert = cls(AlertStyle.informational,
                    title,
                    question,
                    ('Yes', 'No'),
                    custom_image)
        return alert.show()

    @classmethod
    def show_confirmation(cls, title: str,
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
        alert = cls(AlertStyle.warning,
                    title,
                    question,
                    ('Ok', 'Cancel'),
                    custom_image)
        return alert.show()


class OpenModal:
    def __init__(self,
                 title: str,
                 path: Optional[str]=None,
                 allowed_extensions: Optional[Tuple[str]]=None,
                 prompt: Optional[str]=None,
                 message: Optional[str]=None,
                 can_choose_files: bool=True,
                 can_choose_directories: bool=False,
                 resolve_aliases: bool=True,
                 allow_multiple_selection: bool=False,
                 can_create_directories: bool=False,
                 can_show_all_extensions: bool=False,
                 expanded: bool=False
                ) -> None:
        self.modal = NSOpenPanel.openPanel()
        self.modal.title = title
        self.modal.message = message or ''
        self.modal.canChooseFiles = can_choose_files
        self.modal.canChooseDirectories = can_choose_directories
        self.modal.resolvesAliases = resolve_aliases
        self.modal.allowsMultipleSelection = allow_multiple_selection
        self.modal.canCreateDirectories = can_create_directories
        self.modal.canSelectHiddenExtension = can_show_all_extensions
        self.modal.expanded = expanded

        if prompt:
            self.modal.prompt = prompt

        if allowed_extensions:
            self.modal.allowedContentTypes = [UTType.typeWithFilenameExtension(e) for e in allowed_extensions]

        if path:
            self.modal.directoryURL = NSURL.fileURLWithPath_(path)

    def show(self):
        return self.modal.runModal()

    @classmethod
    def open_file(cls, title: str):
        modal = cls(title)
        return modal.show()
