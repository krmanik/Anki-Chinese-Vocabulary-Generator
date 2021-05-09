import os
import json
import jieba
import shutil
import pinyin
import sqlite3
import platform
import webbrowser
import tkinter as Tkinter
import tkinter.ttk as ttk
from tkinter import messagebox

from gtts import gTTS
from tkinter import *
from hanziconv import HanziConv
from googletrans import Translator
from cedict.pinyin import pinyinize

from tkinter.filedialog import askopenfilename

class VocabGenerator(Tkinter.Frame):

    def __init__(self, parent):
        Tkinter.Frame.__init__(self, parent)
        self.parent=parent
        self.init_ui()

    def init_ui(self):
        self.addAudioFromgTTS = IntVar()
        self.addAudio = IntVar()
        self.addSentence = IntVar()

        self.output_file = ""
        self.ch_sent = ""
        self.ch_sent_pinyin = ""
        self.ch_sent_translate = ""
        
        self.parent.title("Chinese Vocabulary Generator")
        self.parent.grid_rowconfigure(0, weight=1)
        self.parent.grid_columnconfigure(0, weight=1)

        self.menubar = Menu(self.parent)

        self.file = Menu(self.menubar, tearoff=0)
        self.file.add_command(label="Import", command=self.import_file)
        self.file.add_separator()        
        self.file.add_command(label="Save", command=self.save_data)
        self.file.add_separator()
        self.file.add_command(label="Exit", command=self.confirm_exit)

        self.menubar.add_cascade(label="File", menu=self.file)
        
        self.edit = Menu(self.menubar, tearoff=0)
        self.edit.add_command(label="Modify", command=self.edit_data)
        self.edit.add_command(label="Delete", command=self.delete_data)
        self.edit.add_separator()
        self.edit.add_command(label="Add Sentences", command=self.add_sentence)
        
        self.menubar.add_cascade(label="Edit", menu=self.edit)

        self.help = Menu(self.menubar, tearoff=0)
        self.help.add_command(label="About", command=self.about)
        self.help.add_separator()
        self.help.add_command(label="View Docs", command=self.view_docs)
        
        self.menubar.add_cascade(label="Help", menu=self.help)

        self.parent.config(menu=self.menubar)

        self.ch_sim_label = Tkinter.Label(self.parent, text="Simplified")
        self.ch_sim_entry = Tkinter.Entry(self.parent)
        self.ch_sim_label.pack()
        self.ch_sim_entry.pack()

        self.submit_button = Tkinter.Button(self.parent, text="Enter", command=self.insert_data)
        self.submit_button.pack()

        self.con = sqlite3.connect("sen_data.db")
        self.cur = self.con.cursor()

        self.parent.withdraw()
        self.new_data()

        self.init_json()

    def confirm_exit(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.parent.destroy()

    def new_data(self):
        self.new_window = Tkinter.Toplevel(self.parent)
        if 'aarch64' in platform.platform():
            self.new_window.attributes('-fullscreen', True)
        else:
            self.new_window.geometry('600x600')
        
        self.new_window.attributes('-topmost', 'true')
        
        title_label = Tkinter.Label(self.new_window, text="xiehanzi", fg="cornflowerblue", font=("Helvetica", 16))
        title_label.pack(pady="15")
        
        self.options_label = Tkinter.Label(self.new_window, text="Want to add?")
        self.options_label.pack()
    
        addAudioCheckbutton = Checkbutton(self.new_window, text = "Audio      ", variable = self.addAudio, onvalue = 1, offvalue = 0)
        addSentenceCheckbutton = Checkbutton(self.new_window, text = "Sentence", variable = self.addSentence, onvalue = 1, offvalue = 0)
        
        addAudioCheckbutton.pack()
        addSentenceCheckbutton.pack()

        self.ok_button = Tkinter.Button(self.new_window, text="Enter", command=self.draw_table)
        self.ok_button.pack(pady="10")        

    def draw_table(self):
        self.new_window.destroy()
        self.parent.deiconify()

        self.tabel_column1 = ('Traditional', 'Pinyin', 'Meaning')
        self.tabel_column2 = ('Traditional', 'Pinyin', 'Meaning', 'Audio')
        self.tabel_column3 = ('Traditional', 'Pinyin', 'Meaning', 'Sentence', 'S.Traditional', 'S. Pinyin', 'Translation')
        self.tabel_column4 = ('Traditional', 'Pinyin', 'Meaning', 'Audio', 'Sentence', 'S.Traditional', 'S. Pinyin', 'Translation')

        if self.addAudio.get() and self.addSentence.get():
            self.tabel_column = self.tabel_column4
            
            self.tree = ttk.Treeview(self.parent, columns=(self.tabel_column4))
            self.tree.heading('#0', text='Simplified')
            self.tree.heading('#1', text='Traditional')
            self.tree.heading('#2', text='Pinyin')
            self.tree.heading('#3', text='Meaning')
            self.tree.heading('#4', text='Sentence')
            self.tree.heading('#5', text='S.Traditional')
            self.tree.heading('#6', text='S. Pinyin')
            self.tree.heading('#7', text='Translation')
            self.tree.heading('#8', text='Audio')

            self.tree.column('#0', stretch=Tkinter.YES)
            self.tree.column('#1', stretch=Tkinter.YES)
            self.tree.column('#2', stretch=Tkinter.YES)
            self.tree.column('#3', stretch=Tkinter.YES)
            self.tree.column('#4', stretch=Tkinter.YES)
            self.tree.column('#5', stretch=Tkinter.YES)
            self.tree.column('#6', stretch=Tkinter.YES)
            self.tree.column('#7', stretch=Tkinter.YES)
            self.tree.column('#8', stretch=Tkinter.YES)


        else:
            if self.addAudio.get():
                self.edit.entryconfig("Add Sentences", state="disabled")
                self.tabel_column = self.tabel_column2

                self.tree = ttk.Treeview(self.parent, columns=(self.tabel_column2))
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
            
            elif self.addSentence.get():
                self.tabel_column = self.tabel_column3
                self.tree = ttk.Treeview(self.parent, columns=(self.tabel_column3))
                self.tree.heading('#0', text='Simplified')
                self.tree.heading('#1', text='Traditional')
                self.tree.heading('#2', text='Pinyin')
                self.tree.heading('#3', text='Meaning')
                self.tree.heading('#4', text='Sentence')
                self.tree.heading('#5', text='S.Traditional')
                self.tree.heading('#6', text='S. Pinyin')
                self.tree.heading('#7', text='Translation')

                self.tree.column('#0', stretch=Tkinter.YES)
                self.tree.column('#1', stretch=Tkinter.YES)
                self.tree.column('#2', stretch=Tkinter.YES)
                self.tree.column('#3', stretch=Tkinter.YES)
                self.tree.column('#4', stretch=Tkinter.YES)
                self.tree.column('#5', stretch=Tkinter.YES)
                self.tree.column('#6', stretch=Tkinter.YES)
                self.tree.column('#7', stretch=Tkinter.YES)

            else:
                self.edit.entryconfig("Add Sentences", state="disabled")
                self.tabel_column = self.tabel_column1

                self.tree = ttk.Treeview(self.parent, columns=(self.tabel_column1))
                self.tree.heading('#0', text='Simplified')
                self.tree.heading('#1', text='Traditional')
                self.tree.heading('#2', text='Pinyin')
                self.tree.heading('#3', text='Meaning')
                
                self.tree.column('#0', stretch=Tkinter.YES)
                self.tree.column('#1', stretch=Tkinter.YES)
                self.tree.column('#2', stretch=Tkinter.YES)
                self.tree.column('#3', stretch=Tkinter.YES)

        style = ttk.Style(self.parent)
        
        if 'aarch64' in platform.platform():
            style.configure('Treeview', rowheight=60)
        else:
            style.configure('Treeview')
        
        self.tree.pack(padx="10", pady="10", fill=BOTH, expand=1)
        self.treeview = self.tree

    def insert_data(self):
        ch_sim = self.ch_sim_entry.get()
        self.insert_meaning(ch_sim)

    def delete_data(self):
        try:
            selected_item = self.treeview.selection()[0]
            self.treeview.delete(selected_item)
        except:
            print("Select a row to continue")

    def edit_data(self):
        try:
            selected_item = self.treeview.selection()[0]

            window = Tkinter.Toplevel(self.parent)

            if 'aarch64' in platform.platform():
                window.attributes("-fullscreen", True)
            else:
                window.geometry('500x350')

            edit_sim_label = Tkinter.Label(window, text="Simplified")
            edit_sim_label.pack()

            edit_sim_entry = Tkinter.Entry(window)
            edit_sim_entry.pack(fill='x', padx="10")
            edit_sim_entry.insert(0, str(self.treeview.item(selected_item)['text']))
            
            edit_trad_label = Tkinter.Label(window, text="Traditional")
            edit_trad_label.pack()

            edit_trad_entry = Tkinter.Entry(window)
            edit_trad_entry.pack(fill='x', padx="10")
            edit_trad_entry.insert(0, str(self.treeview.item(selected_item)['values'][0]))
            
            edit_pin_label = Tkinter.Label(window, text="Pinyin")
            edit_pin_label.pack()
            
            edit_pin_entry = Tkinter.Entry(window)
            edit_pin_entry.pack(fill='x', padx="10")
            edit_pin_entry.insert(0, str(self.treeview.item(selected_item)['values'][1]))

            edit_mean_label = Tkinter.Label(window, text="Meaning")
            edit_mean_label.pack()
            
            edit_mean_entry = Tkinter.Entry(window)
            edit_mean_entry.pack(fill='x', padx="10")
            edit_mean_entry.insert(0, str(self.treeview.item(selected_item)['values'][2]))

            if self.addSentence.get():
                edit_sent_label = Tkinter.Label(window, text="Sentence")
                edit_sent_label.pack()

                edit_sent_entry = Tkinter.Entry(window)
                edit_sent_entry.pack(fill='x', padx="10")
                edit_sent_entry.insert(0, str(self.treeview.item(selected_item)['values'][3]))

                edit_sent_trad_label = Tkinter.Label(window, text="Sentence Traditional")
                edit_sent_trad_label.pack()

                edit_sent_trad_entry = Tkinter.Entry(window)
                edit_sent_trad_entry.pack(fill='x', padx="10")
                edit_sent_trad_entry.insert(0, str(self.treeview.item(selected_item)['values'][4]))

                edit_sent_pinyin_label = Tkinter.Label(window, text="Sentence Pinyin")
                edit_sent_pinyin_label.pack()

                edit_sent_pinyin_entry = Tkinter.Entry(window)
                edit_sent_pinyin_entry.pack(fill='x', padx="10")
                edit_sent_pinyin_entry.insert(0, str(self.treeview.item(selected_item)['values'][5]))

                edit_sent_translate_label = Tkinter.Label(window, text="Translation")
                edit_sent_translate_label.pack()

                edit_sent_translate_entry = Tkinter.Entry(window)
                edit_sent_translate_entry.pack(fill='x', padx="10")
                edit_sent_translate_entry.insert(0, str(self.treeview.item(selected_item)['values'][6]))

            def ok():
                try:
                    selected_item = self.treeview.selection()[0]
                    
                    ch_audio = "[sound:/xiehanzi/cmn-" + edit_sim_entry.get() + ".mp3]"
                    
                    if edit_sim_entry.get() == str(self.treeview.item(selected_item)['text']):
                        self.treeview.set(selected_item, '#1', edit_trad_entry.get())
                        self.treeview.set(selected_item, '#2', edit_pin_entry.get())
                        self.treeview.set(selected_item, '#3', edit_mean_entry.get())

                        if self.addSentence.get():
                            self.treeview.set(selected_item, '#4', edit_sent_entry.get())
                            self.treeview.set(selected_item, '#5', edit_sent_trad_entry.get())
                            self.treeview.set(selected_item, '#6', edit_sent_pinyin_entry.get())
                            self.treeview.set(selected_item, '#7', edit_sent_translate_entry.get())

                    else:
                        self.treeview.delete(selected_item)

                        if self.addAudio.get() and self.addSentence.get():
                            self.treeview.insert('', 'end', text=edit_sim_entry.get(), values=(edit_trad_entry.get(), edit_pin_entry.get(), edit_mean_entry.get(), edit_sent_entry.get(), edit_sent_trad_entry, edit_sent_pinyin_entry.get(), edit_sent_translate_entry.get(), ch_audio))
                            
                        else:
                            if self.addSentence.get():
                                self.treeview.insert('', 'end', text=edit_sim_entry.get(), values=(edit_trad_entry.get(), edit_pin_entry.get(), edit_mean_entry.get(), edit_sent_entry.get(), edit_sent_trad_entry, edit_sent_pinyin_entry.get(), edit_sent_translate_entry.get()))
                            elif self.addAudio.get():
                                self.treeview.insert('', 'end', text=edit_sim_entry.get(), values=(edit_trad_entry.get(), edit_pin_entry.get(), edit_mean_entry.get(), ch_audio))
                                self.save_audio(edit_sim_entry.get())
                            else:
                                self.treeview.insert('', 'end', text=edit_sim_entry.get(), values=(edit_trad_entry.get(), edit_pin_entry.get(), edit_mean_entry.get()))
                
                except:
                    print("Update Error")

                window.destroy()

            ok_button = Tkinter.Button(window, text="OK", command=ok)
            ok_button.pack(pady="5")
                
        except:
            print("Edit Error")
        
    def save_data(self):
        with open('output.txt','w', encoding='utf8') as f:
            for child in self.treeview.get_children():
                sim = self.treeview.item(child)["text"]
                trad = self.treeview.item(child)["values"][0]
                pin = self.treeview.item(child)["values"][1]
                mean = self.treeview.item(child)["values"][2]

                line = sim + "\t" + trad + "\t" + pin + "\t" + mean

                if self.addAudio.get() and self.addSentence.get():
                    sen = self.treeview.item(child)["values"][3]
                    s_trad = self.treeview.item(child)["values"][4]
                    s_pin = self.treeview.item(child)["values"][5]
                    s_tr = self.treeview.item(child)["values"][6]
                    aud = self.treeview.item(child)["values"][7]
                    
                    line += "\t" + sen + "\t" + s_trad + "\t" + s_pin + "\t" + s_tr + "\t" + aud
            
                else:
                    if self.addSentence.get():
                        sen = self.treeview.item(child)["values"][3]
                        s_trad = self.treeview.item(child)["values"][4]
                        s_pin = self.treeview.item(child)["values"][5]
                        s_tr = self.treeview.item(child)["values"][6]
                        line += "\t"  + sen + "\t" + s_trad + "\t" + s_pin + "\t" + s_tr
            
                    elif self.addAudio.get():
                        aud = self.treeview.item(child)["values"][3]
                        line += "\t" + aud
                        self.save_audio(sim)
                    
                print(line)
                
                to_save = str(line + "\n")
                f.write(to_save)

    def change_tts(self):
        self.t_status = not self.t_status

    def save_audio(self, ch_sim):
        if not os.path.exists('xiehanzi'):
            os.makedirs('xiehanzi')
        fname = "cmn-" + ch_sim + ".mp3"

        found = False
        try:
            h = "audio_data/cmn-" + ch_sim + ".mp3"
            g = "xiehanzi/cmn-" + ch_sim + ".mp3"
            if os.path.exists(h):
                shutil.copy(h, 'xiehanzi/')
                found = True
            elif os.path.exists(g):
                found = True
        except:
            print('Audio not found in data folder, fetching online')

        if not found:
            if self.addAudioFromgTTS:
                t = gTTS(ch_sim, lang="zh-cn")
                t.save('xiehanzi/'+ fname)

    def contains_digit(s):
        isdigit = str.isdigit
        return any(map(isdigit,s))

    def add_sentence(self):
        try:
            selected_item = self.treeview.selection()[0]
            sim_entry = self.treeview.item(selected_item)['text']

            window = Tkinter.Tk()
            if 'aarch64' in platform.platform():
                window.attributes("-fullscreen", True)
            else:
                window.geometry('400x400')
            window.title("Add Sentence")

            frame = Frame(window)
            frame.pack(side="top", anchor=N, fill="both", expand=True, padx="10", pady="10")

            scrollbar = Scrollbar(frame)
            scrollbar.pack(side="right", fill="y")

            sen_list = Listbox(frame, font=("Helvetica", 16))
            sen_list.pack(side="left", fill="both", expand=True)
            
            sql = "Select simplified from examples where simplified like " + "'%" + sim_entry + "%'"
            sql2 = "Select simplified, traditional, pinyin, english from examples where simplified like " + "'%" + sim_entry + "%'"
            
            self.cur.execute(sql)
            sent = self.cur.fetchall()

            self.cur.execute(sql2)
            sent2 = self.cur.fetchall()

            for i in range(len(sent)):
                sen_list.insert(i, sent[i])

            def sent_add_to_table():
                selection = sen_list.curselection()[0]

                s = ''.join(sen_list.get(ACTIVE))
                s = HanziConv.toSimplified(s)
                
                self.ch_sent += ''.join(s)
                self.treeview.set(selected_item, '#4', self.ch_sent)

                self.ch_sent_pinyin = sent2[selection][1]
                self.treeview.set(selected_item, '#5', self.ch_sent_pinyin)

                self.ch_sent_pinyin = sent2[selection][2]
                self.treeview.set(selected_item, '#6', self.ch_sent_pinyin)

                self.ch_sent_translate = sent2[selection][3]
                self.treeview.set(selected_item, '#7', self.ch_sent_translate)

            scrollbar.config(command=sen_list.yview)
            sen_list.config(yscrollcommand=scrollbar.set)
            
            add_sent_button = Button(window, text="Add", command=sent_add_to_table)
            add_sent_button.pack(anchor=N, fill="x", padx="30", pady="5")
            
        except:
            print('Error Adding Sentences')

    def view_docs(self):
        try:
            webbrowser.open_new("https://github.com/infinyte7/Anki-Chinese-Vocabulary-Generator")
        except:
            messagebox.showinfo("Open in browser", "https://github.com/infinyte7\n/Anki-Chinese-Vocabulary-Generator")

    def about(self):
        window = Tkinter.Tk()
        window.title("About")

        title_label = Tkinter.Label(window, text="xiehanzi", fg="cornflowerblue", font=("Helvetica", 26))
        title_label.pack()

        sub_label = Tkinter.Label(window, text="Chinese Vocabulary Generator")
        sub_label.pack()
        
        v_label = Tkinter.Label(window, text="V 1.5")
        v_label.pack()

        m_label = Tkinter.Label(window, text="Infinyte7")
        m_label.pack()

        def open_l():
            try:
                webbrowser.open_new("https://github.com/infinyte7/Anki-Chinese-Vocabulary-Generator/blob/master/License.md")
            except:
                messagebox.showinfo("Open in browser", "https://github.com/infinyte7/\nAnki-Chinese-Vocabulary-Generator/\nblob/master/License.md")

        l_button = Tkinter.Button(window, text="View License", command=open_l)
        l_button.pack(pady="5")

    def import_file(self):              
        Tk().withdraw()
        filename = askopenfilename()
        with open(filename, "r", encoding="utf-8") as f:
            lines = f.readlines()
            for l in lines:
                self.insert_meaning(l.strip())

    def insert_meaning(self, word):
        ch_sim = word
        self.simp = ch_sim
        self.ch_sim_entry.delete(0, 'end')

        ch_pin=""
        ch_mean = ""
        ch_trad = HanziConv.toTraditional(ch_sim)
        ch_audio = "[sound:xiehanzi/cmn-" + ch_sim + ".mp3]"
        
        found = False

        try:
            # when pinyin present in json file, fetch from there as pinyin library provide incorrect pinyin
            ch_pin = ""
            for p in self.cedict_json_data[ch_sim]["pinyin"]:
                ch_pin += pinyinize(p) + ", "
            ch_pin = ch_pin.strip().rstrip(",")

            for d in self.cedict_json_data[ch_sim]["definitions"]:
                print(self.cedict_json_data[ch_sim]["definitions"][d])    
                ch_mean += self.cedict_json_data[ch_sim]["definitions"][d] + " "
            found = True
        except:
            self.not_found = open("not_found.txt", "a", encoding="utf-8")
            ln = ch_sim+"\n"
            self.not_found.write(ln)
            self.not_found.close()            
            print("json not found in data folder, fetching online")

        if not found and len(ch_sim) > 0:
            ch_pin = pinyin.get(ch_sim)
            
            translator = Translator()
            t = translator.translate(ch_sim, src='zh-cn', dest="en")
            ch_mean = t.text

        self.ch_sent=""
        self.ch_sent_trad=""
        self.ch_sent_pinyin = ""
        self.ch_sent_translate = ""

        if len(ch_sim) > 0:
            try:
                if self.addAudio.get() and self.addSentence.get():
                    self.treeview.insert('', 'end', text=ch_sim, values=(ch_trad, ch_pin, ch_mean, self.ch_sent, self.ch_sent_trad, self.ch_sent_pinyin, self.ch_sent_translate, ch_audio))
                    self.save_audio(ch_sim)
                else:
                    if self.addAudio.get():
                        self.treeview.insert('', 'end', text=ch_sim, values=(ch_trad, ch_pin, ch_mean, ch_audio))
                        self.save_audio(ch_sim)
                    elif self.addSentence.get():
                        self.treeview.insert('', 'end', text=ch_sim, values=(ch_trad, ch_pin, ch_mean, self.ch_sent, self.ch_sent_trad, self.ch_sent_pinyin, self.ch_sent_translate))
                    else:
                        self.treeview.insert('', 'end', text=ch_sim, values=(ch_trad, ch_pin, ch_mean))

            except:
                print("Insert Error")
                traceback.print_exc()
    
    def init_json(self):
        with open("json_data/all_cedict.json", "r", encoding="utf-8") as f:
            self.cedict_json_data = json.load(f)

def main():
    def confirm_exit_main():
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            root.destroy()

    root=Tkinter.Tk()
    d=VocabGenerator(root)
    if 'aarch64' in platform.platform():
    	root.attributes("-fullscreen", True)
    root.protocol("WM_DELETE_WINDOW", confirm_exit_main)
    root.mainloop()


if __name__=="__main__":
    main()
