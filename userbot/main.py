# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Raphielscape Public License, Version 1.c ("Lisans") altında lisanslanmıştır;
# Lisans ile uyumlu olmadıkça bu dosyayı kullanamazsınız.
#

# AzeUserBot - Vusal Mzade

""" UserBot başlangıç noktası """
import importlib
from importlib import import_module
from sqlite3 import connect
import os
import requests
from telethon.tl.types import InputMessagesFilterDocument
from telethon.errors.rpcerrorlist import PhoneNumberInvalidError
from telethon.tl.functions.channels import GetMessagesRequest
from . import BRAIN_CHECKER, LOGS, bot, PLUGIN_CHANNEL_ID, CMD_HELP, LANGUAGE, ASENA_VERSION, PATTERNS
from .modules import ALL_MODULES
import userbot.modules.sql_helper.mesaj_sql as MSJ_SQL
import userbot.modules.sql_helper.galeri_sql as GALERI_SQL
from pySmartDL import SmartDL
from telethon.tl import functions

from random import choice
import chromedriver_autoinstaller
from json import loads, JSONDecodeError
import re
import userbot.cmdhelp

DIZCILIK_STR = [
    "Çıkartmayı hazırlıyır...",
    "Yaşasın hazırlık...",
    "Bu stikeri paketimə dəvət edirəm...",
    "Bunu hazırlamam lazım...",
    "Hey bu güzel bir çıkartma!\nHemen hazırlıyorum...",
    "Çıkartmanı hazırlıyorum\nhahaha.",
    "Hey şuraya bak. (☉｡☉)!→\nBen bunu dızlarken...",
    "Güller qırmızı menekşeler mavi, bu çıkartmayı paketime hazırlıyorum havalı olacağım...",
    "Çıkartma hapsediliyor...",
    "Bay hazırlayıcı bu çıkartmayı hazırlıyor... ",
]

AFKSTR = [
    "İşim Var Gələcəm.",
    "Allah Məni Qorusun.",
    "Az Bir Vaxta Buralarda Olaram",
    "Allahqı Gələcəm(Ölməsəy Qalsağ İnşallah)",
    "Yazacamdaaaaaaaa Nə Dırha Dırrrrrrr Salmısan!",
]

UNAPPROVED_MSG = ("`Hey,` {mention}`! Bu Bir Botdur.\n\n`"
                  "`Sahibim Sənə İcazə Vermedi. `"
                  "`Xaiş edirem Sahibimi Gözləyin.\n\n`"
                  "`Bildiyimə Görə Sahibim Dəlilərə İcazə Vermir`")

DB = connect("learning-data-root.check")
CURSOR = DB.cursor()
CURSOR.execute("""SELECT * FROM BRAIN1""")
ALL_ROWS = CURSOR.fetchall()
INVALID_PH = '\nHATA: Girilen telefon numarası geçersiz' \
             '\n  Ipucu: Ülke kodunu kullanarak numaranı gir' \
             '\n       Telefon numaranızı tekrar kontrol edin'

for i in ALL_ROWS:
    BRAIN_CHECKER.append(i[0])
connect("learning-data-root.check").close()

def extractCommands(file):
    FileRead = open(file, 'r').read()
    
    if '/' in file:
        file = file.split('/')[-1]

    Pattern = re.findall(r"@register\(.*pattern=(r|)\"(.*)\".*\)", FileRead)
    Komutlar = []

    if re.search(r'CmdHelp\(.*\)', FileRead):
        pass
    else:
        dosyaAdi = file.replace('.py', '')
        CmdHelp = userbot.cmdhelp.CmdHelp(dosyaAdi, False)

        # Komutları Alıyoruz #
        for Command in Pattern:
            Command = Command[1]
            if Command == '' or len(Command) <= 1:
                continue
            Komut = re.findall("(^.*[a-zA-Z0-9şğüöçı]\w)", Command)
            if (len(Komut) >= 1) and (not Komut[0] == ''):
                Komut = Komut[0]
                if Komut[0] == '^':
                    KomutStr = Komut[1:]
                    if KomutStr[0] == '.':
                        KomutStr = KomutStr[1:]
                    Komutlar.append(KomutStr)
                else:
                    if Command[0] == '^':
                        KomutStr = Command[1:]
                        if KomutStr[0] == '.':
                            KomutStr = KomutStr[1:]
                        else:
                            KomutStr = Command
                        Komutlar.append(KomutStr)

            # AzeUserBotPY
            AzeUserBotpy = re.search('\"\"\"AZEUSERBOTPY(.*)\"\"\"', FileRead, re.DOTALL)
            if not AzeUserBotpy == None:
                AzeUserBotpy = AzeUserBotpy.group(0)
                for Satir in AzeUserBotpy.splitlines():
                    if (not '"""' in Satir) and (':' in Satir):
                        Satir = Satir.split(':')
                        Isim = Satir[0]
                        Deger = Satir[1][1:]
                                
                        if Isim == 'INFO':
                            CmdHelp.add_info(Deger)
                        elif Isim == 'WARN':
                            CmdHelp.add_warning(Deger)
                        else:
                            CmdHelp.set_file_info(Isim, Deger)
            for Komut in Komutlar:
                # if re.search('\[(\w*)\]', Komut):
                    # Komut = re.sub('(?<=\[.)[A-Za-z0-9_]*\]', '', Komut).replace('[', '')
                CmdHelp.add_command(Komut, None, 'Bu Plugin Haqqında Məlumat Yoxdur.')
            CmdHelp.add()

try:
    bot.start()
    idim = bot.get_me().id
    asenabl = requests.get('https://gitlab.com/vusal_memmedzade/azeuser/-/blob/master/aze.json').json()
    if idim in asenabl:
        bot.disconnect()

    # ChromeDriver'ı Ayarlayalım #
    try:
        chromedriver_autoinstaller.install()
    except:
        pass
    
    # Galeri için değerler
    GALERI = {}

    # PLUGIN MESAJLARI AYARLIYORUZ
    PLUGIN_MESAJLAR = {}
    ORJ_PLUGIN_MESAJLAR = {"alive": "`🐺Şəhid`lər Ölməz Vətən Bölünməz.🐺` `AzeUserBot İşləyir.`", "afk": f"`{str(choice(AFKSTR))}`", "kickme": "`Varlığım size bir ödülse yoklugumu size hediyye ediyorum.`🥳🚭", "pm": UNAPPROVED_MSG, "dızcı": str(choice(DIZCILIK_STR)), "ban": "{mention}`, Əngəlləndin!`", "mute": "{mention}`, Susturuldun!`", "approve": "{mention}`, Mənə Mesaj Göndərə Bilərsən!`", "disapprove": "{mention}`, Sahibim Icazə Vermir Mesaj Göndərməyə`", "block": "{mention}`, Əngəlləndin`"}

    PLUGIN_MESAJLAR_TURLER = ["alive", "afk", "kickme", "pm", "dızcı", "ban", "mute", "approve", "disapprove", "block"]
    for mesaj in PLUGIN_MESAJLAR_TURLER:
        dmsj = MSJ_SQL.getir_mesaj(mesaj)
        if dmsj == False:
            PLUGIN_MESAJLAR[mesaj] = ORJ_PLUGIN_MESAJLAR[mesaj]
        else:
            if dmsj.startswith("MEDYA_"):
                medya = int(dmsj.split("MEDYA_")[1])
                medya = bot.get_messages(PLUGIN_CHANNEL_ID, ids=medya)

                PLUGIN_MESAJLAR[mesaj] = medya
            else:
                PLUGIN_MESAJLAR[mesaj] = dmsj
    if not PLUGIN_CHANNEL_ID == None:
        LOGS.info("Pluginler Yükleniyor")
        try:
            KanalId = bot.get_entity(PLUGIN_CHANNEL_ID)
        except:
            KanalId = "me"

        for plugin in bot.iter_messages(KanalId, filter=InputMessagesFilterDocument):
            if plugin.file.name and (len(plugin.file.name.split('.')) > 1) \
                and plugin.file.name.split('.')[-1] == 'py':
                Split = plugin.file.name.split('.')

                if not os.path.exists("./userbot/modules/" + plugin.file.name):
                    dosya = bot.download_media(plugin, "./userbot/modules/")
                else:
                    LOGS.info("Bu Plugin Zaten Yüklü " + plugin.file.name)
                    extractCommands('./userbot/modules/' + plugin.file.name)
                    dosya = plugin.file.name
                    continue 
                
                try:
                    spec = importlib.util.spec_from_file_location("userbot.modules." + Split[0], dosya)
                    mod = importlib.util.module_from_spec(spec)

                    spec.loader.exec_module(mod)
                except Exception as e:
                    LOGS.info(f"`Yükleme başarısız! Plugin hatalı.\n\nHata: {e}`")

                    try:
                        plugin.delete()
                    except:
                        pass

                    if os.path.exists("./userbot/modules/" + plugin.file.name):
                        os.remove("./userbot/modules/" + plugin.file.name)
                    continue
                extractCommands('./userbot/modules/' + plugin.file.name)
    else:
        bot.send_message("me", f"`Plugin_Channel_Id'iniz geçersiz. Pluginler Qalıcı Olmuyacaq.`")
except PhoneNumberInvalidError:
    print(INVALID_PH)
    exit(1)

async def FotoDegistir (foto):
    FOTOURL = GALERI_SQL.TUM_GALERI[foto].foto
    r = requests.get(FOTOURL)

    with open(str(foto) + ".jpg", 'wb') as f:
        f.write(r.content)    
    file = await bot.upload_file(str(foto) + ".jpg")
    try:
        await bot(functions.photos.UploadProfilePhotoRequest(
            file
        ))
        return True
    except:
        return False

for module_name in ALL_MODULES:
    imported_module = import_module("userbot.modules." + module_name)

LOGS.info("Botunuz İşlək Vəziyyətdə Hər Hansı Söhbətə .alive Yazaraq Test Edin."
          " Köməyə Ehtiyacınız Varsa, Kömək Qrupumuza Gəlin https://t.me/azeuserbotsupport")
LOGS.info(f"Bot Versiyası: AzeUserBot {AzeUserBot_VERSION}")

"""
if len(argv) not in (1, 3, 4):
    bot.disconnect()
else:
"""
bot.run_until_disconnected()