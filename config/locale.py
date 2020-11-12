import gettext

from .settings import LOCALEDOMAIN, LOCALEDIR, DEFAULT_LOCALE, LOCALE

try:
    translation = gettext.translation(
        LOCALEDOMAIN, localedir=LOCALEDIR, languages=[LOCALE]
    )
except FileNotFoundError:
    translation = gettext.translation(
        LOCALEDOMAIN, localedir=LOCALEDIR, languages=[DEFAULT_LOCALE]
    )

_ = translation.gettext
