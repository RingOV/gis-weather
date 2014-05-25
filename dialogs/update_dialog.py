#!/usr/bin/env python3

from gi.repository import Gtk, GdkPixbuf
from urllib.request import urlretrieve
from utils import localization

import os
import subprocess
import shlex
import sys
import time
if sys.platform.startswith("win"):
    WIN = True
else:
    WIN = False

label_updating_step1 = None
APP_PATH1 = None
dialog = None
linkbutton_send = None
percent = 0

def dlProgress(count, blockSize, totalSize):
    global updating_step1, percent
    percent = int(count*blockSize*100/totalSize)
    total = str(round(totalSize/1024/1024.0*10)/10.0)
    label_updating_step1.set_text(_('Downloading')+" (%s Мб)... %d%%" %(total, percent))
    # перерисовка окна
    while Gtk.events_pending():
        Gtk.main_iteration_do(True)

def restart(widget):
    if WIN:
        pass
    if os.path.exists(APP_PATH1):
        subprocess.Popen(['python3', os.path.join(APP_PATH1, 'gis-weather.py')], stdout=subprocess.PIPE)
        dialog.hide()
        Gtk.main_quit() 

def set_message_subject(widget, subject):
    if widget.get_active():
        linkbutton_send.set_uri("mailto:ringov.gisweather@gmail.com?subject="+subject)

def create(v, new_ver, CONFIG_PATH, APP_PATH, update_link, file_name, package):
    global APP_PATH1, dialog, linkbutton_send
    APP_PATH1 = APP_PATH
    ui = Gtk.Builder()
    ui.add_from_file(os.path.join(APP_PATH, "dialogs","update_dialog.ui"))
    dialog = ui.get_object('dialog1')
    dialog.set_icon_from_file(os.path.join(APP_PATH, "icon.png"))

    list_o = ui.get_objects()
    dict_o = {}
    dict_o = localization.translate_ui(list_o, dict_o)
    dialog.set_title('Gis Weather: '+_('Update'))

    label = ui.get_object('label')
    image_logo = ui.get_object('image_logo')
    label_cur_ver = ui.get_object('label_cur_ver')
    label_new_ver = ui.get_object('label_new_ver')
    infobar = ui.get_object('infobar')
    infobar_success = ui.get_object('infobar_success')
    infobar_error = ui.get_object('infobar_error')
    global label_updating_step1
    label_updating_step1 = ui.get_object('label_updating_step1')
    button_restart = ui.get_object('button_restart')
    button_update = ui.get_object('button_update')
    button_try_again = ui.get_object('button_try_again')
    pic_step1 = ui.get_object('pic_step1')
    pic_step2 = ui.get_object('pic_step2')
    pic_step3 = ui.get_object('pic_step3')
    radiobutton1 = ui.get_object('radiobutton1')
    radiobutton2 = ui.get_object('radiobutton2')
    radiobutton3 = ui.get_object('radiobutton3')
    radiobutton4 = ui.get_object('radiobutton4')
    linkbutton_send = ui.get_object('linkbutton_send')

    radiobutton1.connect("toggled", set_message_subject, "Bug")
    radiobutton2.connect("toggled", set_message_subject, "Localization")
    radiobutton3.connect("toggled", set_message_subject, "Question")
    radiobutton4.connect("toggled", set_message_subject, "Suggestion")

    label_cur_ver.set_markup("<small>"+_("Current version")+": "+v+"</small>")
    label_new_ver.set_markup("<big><b>"+_("Available new version")+": "+"%s</b></big>"%new_ver)
    label.set_markup("<span size='xx-large'>Gis Weather</span>")
    button_restart.connect("clicked", restart)

    image_logo.set_from_pixbuf(GdkPixbuf.Pixbuf.new_from_file_at_size(os.path.join(APP_PATH, 'icon.png'), 128, 128))
    pix_loading = GdkPixbuf.PixbufAnimation.new_from_file(os.path.join(APP_PATH, 'themes', 'loading.gif'))

    response = dialog.run()

    while response == Gtk.ResponseType.OK:
        button_update.set_sensitive(False)
        infobar.show()
        pic_step1.set_from_animation(pix_loading)
        pic_step2.clear()
        pic_step3.clear()
        infobar_error.hide()
        # перерисовка окна
        #while Gtk.events_pending():
        #    Gtk.main_iteration_do(True)
        url = update_link
        _file = os.path.join(CONFIG_PATH, file_name)
        
        try:
            urlretrieve(url, _file, reporthook=dlProgress)
            pic_step1.set_from_stock(Gtk.STOCK_OK, 4)
        except:
            print ('[!] '+_('Error downloading updates'))
            pic_step1.set_from_stock(Gtk.STOCK_DIALOG_ERROR, 4)
            infobar_error.show()
        else:
            pic_step2.set_from_animation(pix_loading)
            # перерисовка окна
            while Gtk.events_pending():
                Gtk.main_iteration_do(True)
            if package == 'gz':
                # cmd_line = 'tar -xzf "%s" -C "%s" --strip=1'%(_file, APP_PATH)
                # args = shlex.split(cmd_line)
                # p = subprocess.Popen(args, stdout=subprocess.PIPE)
                # out, err = p.communicate()
                # out = 'OK'
                out = 'OK'
                err = 'None'
                print ("GZ")
            else:
                if package == 'deb':
                    p = subprocess.Popen(['pkexec', 'dpkg -i "%s"' %_file], stdout=subprocess.PIPE)
                    out, err = p.communicate()
                else:
                    if package == 'rpm':
                        pass
                    else:
                        if package == 'exe':
                            out = 'OK'
                            err = 'None'
                            try:
                                os.startfile(_file,'runas')
                            except:
                                out = 'None'
                                err = 'True'
                            exit()
                                
            if (out == '' or out == 'None') and err != 'None':
                print ('[!] '+_('Error installing updates'))
                pic_step2.set_from_stock(Gtk.STOCK_DIALOG_ERROR, 4)
                infobar_error.show()
            else:
                print ('> '+_('Installation')+':')
                print (out)
                pic_step2.set_from_stock(Gtk.STOCK_OK, 4)
                pic_step3.set_from_animation(pix_loading)
                try:
                    os.remove(_file)
                    pic_step3.set_from_stock(Gtk.STOCK_OK, 4)
                except:
                    print ('[!] '+_('Error removing'))
                    pic_step3.set_from_stock(Gtk.STOCK_DIALOG_ERROR, 4)
                    infobar_error.show()
                else:
                    infobar_success.show()
        button_update.set_sensitive(True)
        response = dialog.run()

    dialog.hide()
