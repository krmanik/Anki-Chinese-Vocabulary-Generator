import os
import json
import pinyin
import tts.sapi
import tkinter as Tkinter
import tkinter.ttk as ttk

from gtts import gTTS
from hanziconv import HanziConv
from googletrans import Translator

class VocabGenerator(Tkinter.Frame):

    def __init__(self, parent):
        Tkinter.Frame.__init__(self, parent)
        self.parent=parent
        self.init_ui()

    def init_ui(self):
        
        self.parent.title("Chinese Vocabulary Generator")
        self.parent.grid_rowconfigure(0, weight=1)
        self.parent.grid_columnconfigure(0, weight=1)

        self.ch_sim_label = Tkinter.Label(self.parent, text="Simplified")
        self.ch_sim_entry = Tkinter.Entry(self.parent)
        self.ch_sim_label.grid(row=0, pady="5")
        self.ch_sim_entry.grid(row=1, pady="5")

        self.submit_button = Tkinter.Button(self.parent, text="Enter", command=self.insert_data)
        self.submit_button.grid(row=2, pady="5")

        self.submit_button = Tkinter.Button(self.parent, text="Save", command=self.save)
        self.submit_button.grid(row=3, column=0, pady="5", sticky=Tkinter.W)

        self.t_status = False
        self.tts_button = ttk.Checkbutton(self.parent, text="gTTS", variable=self.t_status, command=self.change_tts)
        self.tts_button.grid(row=3, column=1, pady="5", sticky=Tkinter.W)

        self.tree = ttk.Treeview(self.parent, columns=('Traditional', 'Pinyin', 'Meaning', 'Audio'))
        self.tree.heading('#0', text='Simplified')
        self.tree.heading('#1', text='Traditional')
        self.tree.heading('#2', text='Pinyin')
        self.tree.heading('#3', text='Meaning')
        self.tree.heading('#4', text='Audio')

        self.tree.column('#0', stretch=Tkinter.YES)
        self.tree.column('#1', stretch=Tkinter.YES)
        self.tree.column('#2', stretch=Tkinter.YES)
        self.tree.column('#3', stretch=Tkinter.YES)
        self.tree.column('#4', stretch=Tkinter.YES)
        
        self.tree.grid(row=4, columnspan=4, sticky='nsew', padx="10", pady="10")
        self.treeview = self.tree

        self.submit_button = Tkinter.Button(self.parent, text="Edit", command=self.edit)
        self.submit_button.grid(row=5, column=0, pady="5", sticky=Tkinter.W)

        self.submit_button = Tkinter.Button(self.parent, text="Delete", command=self.delete)
        self.submit_button.grid(row=5, column=1, pady="5", sticky=Tkinter.W)

    def insert_data(self):
        ch_sim = self.ch_sim_entry.get()
        self.ch_sim_entry.delete(0, 'end')

        ch_trad = HanziConv.toTraditional(ch_sim)
        ch_pin = pinyin.get(ch_sim)
        ch_audio = "[sound:xiehanzi/cmn-" + ch_sim + ".mp3]"
        ch_mean = ""
        
        found = False

        try:
            j = "data/" + ch_sim + ".json"
            f = open(j, encoding="utf-8")
            d = json.load(f)

            i=0
            for i in range(len(d['definitions'])):
                ch_mean += str(d["definitions"][i]) + ", "
                

            ch_mean = ch_mean.rstrip(', ')
            
            found = True
        except:
            print("Not found")

        if not found:
            translator = Translator()
            t = translator.translate(ch_sim, src='zh-cn', dest="en")
            ch_mean = t.text
        
        if len(ch_sim) > 0:
            self.treeview.insert('', 'end', text=ch_sim, values=(ch_trad, ch_pin, ch_mean, ch_audio))
            self.save_audio(ch_sim)


    def delete(self):
        try:
            selected_item = self.treeview.selection()[0]
            self.treeview.delete(selected_item)
        except:
            print("Not Selected any row")

    def edit(self):
        try:
            selected_item = self.treeview.selection()[0]

            window = Tkinter.Toplevel(self.parent)
            window.geometry('400x250')

            edit_sim_label = Tkinter.Label(window, text="Simplified")
            edit_sim_label.pack()

            edit_sim_entry = Tkinter.Entry(window)
            edit_sim_entry.pack(fill='x')
            edit_sim_entry.insert(0, str(self.treeview.item(selected_item)['text']))
            
            edit_trad_label = Tkinter.Label(window, text="Traditional")
            edit_trad_label.pack()

            edit_trad_entry = Tkinter.Entry(window)
            edit_trad_entry.pack(fill='x')
            edit_trad_entry.insert(0, str(self.treeview.item(selected_item)['values'][0]))
            
            edit_pin_label = Tkinter.Label(window, text="Pinyin")
            edit_pin_label.pack()
            
            edit_pin_entry = Tkinter.Entry(window)
            edit_pin_entry.pack(fill='x')
            edit_pin_entry.insert(0, str(self.treeview.item(selected_item)['values'][1]))

            edit_mean_label = Tkinter.Label(window, text="Meaning")
            edit_mean_label.pack()
            
            edit_mean_entry = Tkinter.Entry(window)
            edit_mean_entry.pack(fill='x')
            edit_mean_entry.insert(0, str(self.treeview.item(selected_item)['values'][2]))
            
##            edit_audio_label = Tkinter.Label(window, text="Audio")
##            edit_audio_label.pack()
##            
##            edit_audio_entry = Tkinter.Entry(window)
##            edit_audio_entry.pack(fill='x')
##            edit_audio_entry.insert(0, str(self.treeview.item(selected_item)['values'][3]))

            def ok():
                try:
                    selected_item = self.treeview.selection()[0]
                    self.treeview.delete(selected_item)
                    ch_audio = "[sound:/xiehanzi/cmn-" + edit_sim_entry.get() + ".mp3]"
                    self.treeview.insert('', 'end', text=edit_sim_entry.get(), values=(edit_trad_entry.get(), edit_pin_entry.get(), edit_mean_entry.get(), ch_audio))
                    self.save_audio(edit_sim_entry.get())
                except:
                    print("Not Selected any row")
                window.destroy()

            ok_button = Tkinter.Button(window, text="OK", command=ok)
            ok_button.pack()
        except:
            print("Not Selected any row")
        
    def save(self):
        with open('xiehanzi.txt','w', encoding='utf8') as f:
            for child in self.treeview.get_children():
                sim = self.treeview.item(child)["text"]
                trad = self.treeview.item(child)["values"][0]
                pin = self.treeview.item(child)["values"][1]
                mean = self.treeview.item(child)["values"][2]
                aud = self.treeview.item(child)["values"][3]
                
                print(sim, "\t", trad, "\t", pin, "\t", mean, "\t", aud)
            
                to_save = str(sim + "\t" + trad + "\t" + pin + "\t" + mean + "\t" + aud + "\n")
                f.write(to_save)

    def change_tts(self):
        self.t_status = not self.t_status

    def save_audio(self, ch_sim):
        if not os.path.exists('xiehanzi'):
            os.makedirs('xiehanzi')
        fname = "cmn-" + ch_sim + ".mp3"
        if self.t_status:
            t = gTTS(ch_sim, lang="zh-cn")
            t.save('xiehanzi/'+ fname)
        else:
            voice = tts.sapi.Sapi()
            voice.create_recording('xiehanzi/'+ fname, ch_sim)
        
def main():
    root=Tkinter.Tk()
    d=VocabGenerator(root)
    root.mainloop()

if __name__=="__main__":
    main()
