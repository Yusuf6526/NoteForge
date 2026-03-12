import customtkinter as ctk
import sqlite3

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

conn = sqlite3.connect('notes.db')
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS notlar (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ders TEXT,
    baslik TEXT,
    icerik TEXT
)
""")
conn.commit()

class NoteApp:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Noteforge")
        self.root.geometry("700x700")
        self.root.resizable(False, False)  

        cursor.execute("SELECT DISTINCT ders FROM notlar")
        self.dersler = [row[0] for row in cursor.fetchall() if row[0] is not None]

        self.secili_ders = None
        self.secili_not = None

        self.ui()

    def ui(self):

        # Ders menüsü

        self.ders_menu = ctk.CTkFrame(self.root, width=220)
        self.ders_menu.pack(side="left", fill="y", padx=10, pady=10)

        self.ders_entry = ctk.CTkEntry(self.ders_menu, placeholder_text="Yeni ders adı")
        self.ders_entry.pack(pady=5, padx=5, fill="x")

        self.ders_ekle_btn = ctk.CTkButton(self.ders_menu, text="Ders Ekle", command=self.ders_ekle)
        self.ders_ekle_btn.pack(pady=5, padx=5, fill="x")

        self.ders_buton_frame = ctk.CTkFrame(self.ders_menu)
        self.ders_buton_frame.pack(pady=10, fill="both", expand=True)

        self.guncelle_ders_butonlari()

        self.notlar_frame = ctk.CTkFrame(self.root,width=200)
        self.notlar_frame.pack(side="left", fill="y", padx=10, pady=10)

        self.edit_frame = ctk.CTkFrame(self.root,width=200)
        self.edit_frame.pack(side="left", fill="y", padx=10, pady=10)

        self.msg_label = ctk.CTkLabel(self.edit_frame, text="", text_color="yellow")
        self.msg_label.pack(pady=5, padx=5, fill="x")

        self.baslik = ctk.CTkEntry(self.edit_frame, placeholder_text="Not Başlığı")
        self.baslik.pack(pady=10, padx=10, fill="x")

        self.icerik = ctk.CTkTextbox(self.edit_frame)
        self.icerik.pack(pady=10, padx=10, fill="both", expand=True)

        self.kaydet_btn = ctk.CTkButton(self.edit_frame, text="Kaydet", command=self.not_kaydet)
        self.kaydet_btn.pack(pady=10, padx=10, fill="x")

        self.sil_btn = ctk.CTkButton(self.edit_frame, text="Notu Sil", command=self.not_sil)
        self.sil_btn.pack(pady=10, padx=10, fill="x")

    def mesaj_goster(self, mesaj, renk="yellow"):
        self.msg_label.configure(text=mesaj, text_color=renk)

    # Ders ekleme ve buton yönetimi

    def ders_ekle(self):
        yeni_ders = self.ders_entry.get().strip()
        if yeni_ders and yeni_ders not in self.dersler:
            self.dersler.append(yeni_ders)
            self.guncelle_ders_butonlari()
            self.ders_entry.delete(0, "end")
            self.mesaj_goster(f"Ders eklendi: {yeni_ders}", "green")
        else:
            self.mesaj_goster("Geçersiz veya mevcut ders!", "red")

    def guncelle_ders_butonlari(self):
        for widget in self.ders_buton_frame.winfo_children():
            widget.destroy()

        for ders in self.dersler:
            frame = ctk.CTkFrame(self.ders_buton_frame)
            frame.pack(fill="x", pady=3)

            btn = ctk.CTkButton(frame, text=ders, command=lambda d=ders: self.ders_sec(d))
            btn.pack(side="left", fill="x", expand=True, padx=(0,5))

            sil_btn = ctk.CTkButton(frame, text="X", width=30, command=lambda d=ders: self.ders_sil(d))
            sil_btn.pack(side="right")

    def ders_sil(self, ders):
        if ders in self.dersler:
            cursor.execute("DELETE FROM notlar WHERE ders=?", (ders,))
            conn.commit()
            self.dersler.remove(ders)
            self.guncelle_ders_butonlari()
            if self.secili_ders == ders:
                self.secili_ders = None
                self.secili_not = None
                for widget in self.notlar_frame.winfo_children():
                    widget.destroy()
                self.baslik.delete(0, "end")
                self.icerik.delete("1.0", "end")
            self.mesaj_goster(f"Ders ve notları silindi: {ders}", "red")

    # Ders seçimi

    def ders_sec(self, ders):
        self.secili_ders = ders
        self.secili_not = None
        self.mesaj_goster(f"Ders seçildi: {ders}", "cyan")

        for widget in self.notlar_frame.winfo_children():
            widget.destroy()
        cursor.execute("SELECT id, baslik FROM notlar WHERE ders=?", (ders,))
        for nid, baslik in cursor.fetchall():
            btn = ctk.CTkButton(self.notlar_frame, text=baslik, command=lambda i=nid: self.not_ac(i))
            btn.pack(fill="x", pady=5)

        yeni_btn = ctk.CTkButton(self.notlar_frame, text="+ Yeni Not", command=self.yeni_not)
        yeni_btn.pack(fill="x", pady=5)

    # Not açma

    def not_ac(self, not_id):
        self.secili_not = not_id
        cursor.execute("SELECT baslik, icerik FROM notlar WHERE id=?", (not_id,))
        result = cursor.fetchone()
        if result:
            baslik, icerik = result
            self.baslik.delete(0, "end")
            self.baslik.insert(0, baslik)
            self.icerik.delete("1.0", "end")
            self.icerik.insert("1.0", icerik)
            self.mesaj_goster(f"Seçilen Not: {baslik}", "cyan")

    # Yeni not

    def yeni_not(self, mesaj=None, renk="green"):
        self.secili_not = None
        self.baslik.delete(0, "end")
        self.icerik.delete("1.0", "end")
        if mesaj:
            self.mesaj_goster(mesaj, renk)
        else:
            self.mesaj_goster("Yeni not oluşturuldu.", "green")

    # Not kaydet

    def not_kaydet(self):
        baslik = self.baslik.get()
        icerik = self.icerik.get("1.0", "end").strip()
        if not baslik:
            self.mesaj_goster("Başlık boş olamaz!", "red")
            return
        if self.secili_not:
            cursor.execute("UPDATE notlar SET baslik=?, icerik=? WHERE id=?", (baslik, icerik, self.secili_not))
            self.mesaj_goster("Not güncellendi.", "green")
        else:
            cursor.execute("INSERT INTO notlar (ders, baslik, icerik) VALUES (?, ?, ?)", (self.secili_ders, baslik, icerik))
            self.mesaj_goster("Yeni not kaydedildi.", "green")
        conn.commit()
        self.ders_sec(self.secili_ders)

    # Not sil

    def not_sil(self):
        if self.secili_not:
            cursor.execute("DELETE FROM notlar WHERE id=?", (self.secili_not,))
            conn.commit()
            self.secili_not = None
            self.ders_sec(self.secili_ders)
            self.yeni_not(mesaj="Not silindi.", renk="red")
        else:
            self.mesaj_goster("Silinecek not seçilmedi!", "red")

    def run(self):
        self.root.mainloop()


app = NoteApp()
app.run()

