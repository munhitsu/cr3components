from django.conf import settings

_ = lambda s: s
LANGUAGES = getattr(settings, "LANGUAGES", (
  ('pl', _('Polish')),
#  ('en', _('English')),
))

LANGUAGES_FALLBACK = getattr(settings, "LANGUAGES_FALLBACK", {
#    'en':'pl',
})

LANGUAGE_CODE = getattr(settings, "LANGUAGE_CODE", 'pl')
