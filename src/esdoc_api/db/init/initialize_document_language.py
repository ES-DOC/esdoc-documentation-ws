# -*- coding: utf-8 -*-
"""
.. module:: initialize_document_language.py
   :platform: Unix
   :synopsis: Initializes collection of supported document languages.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
from esdoc_api.db import models, session



# Set language codes as per ISO 639-1.
_DATA = """aa Afar
ab Abkhazian
af Afrikaans
am Amharic
ar Arabic
as Assamese
ay Aymara
az Azerbaijani
ba Bashkir
be Byelorussian
bg Bulgarian
bh Bihari
bi Bislama
bn Bengali; Bangla
bo Tibetan
br Breton
ca Catalan
co Corsican
cs Czech
cy Welsh
da Danish
de German
dz Bhutani
el Greek
en English
eo Esperanto
es Spanish
et Estonian
eu Basque
fa Persian
fi Finnish
fj Fiji
fo Faroese
fr French
fy Frisian
ga Irish
gd Scots Gaelic
gl Galician
gn Guarani
gu Gujarati
ha Hausa
he Hebrew (formerly iw)
hi Hindi
hr Croatian
hu Hungarian
hy Armenian
ia Interlingua
id Indonesian (formerly in)
ie Interlingue
ik Inupiak
is Icelandic
it Italian
iu Inuktitut
ja Japanese
jw Javanese
ka Georgian
kk Kazakh
kl Greenlandic
km Cambodian
kn Kannada
ko Korean
ks Kashmiri
ku Kurdish
ky Kirghiz
la Latin
ln Lingala
lo Laothian
lt Lithuanian
lv Latvian, Lettish
mg Malagasy
mi Maori
mk Macedonian
ml Malayalam
mn Mongolian
mo Moldavian
mr Marathi
ms Malay
mt Maltese
my Burmese
na Nauru
ne Nepali
nl Dutch
no Norwegian
oc Occitan
om (Afan) Oromo
or Oriya
pa Punjabi
pl Polish
ps Pashto, Pushto
pt Portuguese
qu Quechua
rm Rhaeto-Romance
rn Kirundi
ro Romanian
ru Russian
rw Kinyarwanda
sa Sanskrit
sd Sindhi
sg Sangho
sh Serbo-Croatian
si Sinhalese
sk Slovak
sl Slovenian
sm Samoan
sn Shona
so Somali
sq Albanian
sr Serbian
ss Siswati
st Sesotho
su Sundanese
sv Swedish
sw Swahili
ta Tamil
te Telugu
tg Tajik
th Thai
ti Tigrinya
tk Turkmen
tl Tagalog
tn Setswana
to Tonga
tr Turkish
ts Tsonga
tt Tatar
tw Twi
ug Uighur
uk Ukrainian
ur Urdu
uz Uzbek
vi Vietnamese
vo Volapuk
wo Wolof
xh Xhosa
yi Yiddish (formerly ji)
yo Yoruba
za Zhuang
zh Chinese
zu Zulu"""


def execute():
    """Initializes collection of supported document languages.

    """
    for lang in _DATA.splitlines():
        # Create.
        i = models.DocumentLanguage()
        i.Code = unicode(lang[0:2])
        i.Name = unicode(lang[3:])

        # Persist.
        session.insert(i)
