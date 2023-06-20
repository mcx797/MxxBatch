# coding: utf-8
from enum import Enum

from qfluentwidgets import StyleSheetBase, Theme, isDarkTheme, qconfig


class StyleSheet(StyleSheetBase, Enum):
    """ Style sheet  """

    LINK_CARD = "link_card"
    MAIN_WINDOW = "main_window"
    SAMPLE_CARD = "sample_card"
    HOME_INTERFACE = "home_interface"
    ICON_INTERFACE = "icon_interface"
    VIEW_INTERFACE = "view_interface"
    SETTING_INTERFACE = "setting_interface"
    MXX_INTERFACE = "mxx_interface"
    NAVIGATION_VIEW_INTERFACE = "navigation_view_interface"
    UNLABELED_INTERFACE = 'unlabeled_interface'

    def path(self, theme=Theme.AUTO):
        theme = qconfig.theme if theme == Theme.AUTO else theme
        #return f":/LeadingBatch/qss/{theme.value.lower()}/{self.value}.qss"
        return f".\\app\\resource\\qss\\{theme.value.lower()}\\{self.value}.qss"
