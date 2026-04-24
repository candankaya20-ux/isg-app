# -*- coding: utf-8 -*-
import json
from pathlib import Path

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.scrollview import ScrollView

Window.clearcolor = (0.02, 0.05, 0.10, 1)

APP_TITLE = "İSG MEGA AKADEMİ"
DATA_FILE = Path(__file__).with_name("data.json")


def load_data():
    if not DATA_FILE.exists():
        return {}
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


veriler = load_data()


def make_label(text="", font_size=18, height=None, bold=False):
    label = Label(
        text=text,
        font_size=font_size,
        bold=bold,
        halign="center",
        valign="middle",
        markup=True,
    )
    if height:
        label.size_hint_y = None
        label.height = height
    label.bind(size=lambda instance, value: setattr(instance, "text_size", value))
    return label


def make_button(text, height=58, color=(0.12, 0.24, 0.42, 1), font_size=17):
    return Button(
        text=text,
        font_size=font_size,
        size_hint_y=None,
        height=height,
        background_color=color,
        halign="center",
        valign="middle",
    )


class AnaMenu(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        root = BoxLayout(orientation="vertical", padding=10, spacing=10)
        root.add_widget(make_label(f"[b]{APP_TITLE}[/b]\nB Sınıfı İSG Sınav Hazırlık", 23, 80, True))

        scroll = ScrollView()
        liste = BoxLayout(orientation="vertical", spacing=8, size_hint_y=None)
        liste.bind(minimum_height=liste.setter("height"))

        for konu in veriler.keys():
            btn = make_button(konu, 60, (0.08, 0.22, 0.40, 1), 16)
            btn.bind(on_press=lambda x, k=konu: self.konu_ac(k))
            liste.add_widget(btn)

        scroll.add_widget(liste)
        root.add_widget(scroll)
        self.add_widget(root)

    def konu_ac(self, konu):
        self.manager.get_screen("konu").yukle(konu)
        self.manager.current = "konu"


class KonuEkrani(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.konu = ""
        root = BoxLayout(orientation="vertical", padding=12, spacing=12)
        self.baslik = make_label("", 21, 100, True)
        root.add_widget(self.baslik)

        btn_kart = make_button("🧠 EZBER KARTLARI", 70, (0.12, 0.45, 0.30, 1), 20)
        btn_kart.bind(on_press=self.kartlara_git)
        root.add_widget(btn_kart)

        btn_test = make_button("✅ TEST ÇÖZ", 70, (0.45, 0.25, 0.10, 1), 20)
        btn_test.bind(on_press=self.teste_git)
        root.add_widget(btn_test)

        btn_geri = make_button("⬅ ANA MENÜ", 62, (0.25, 0.25, 0.32, 1), 18)
        btn_geri.bind(on_press=lambda x: setattr(self.manager, "current", "ana"))
        root.add_widget(btn_geri)
        self.add_widget(root)

    def yukle(self, konu):
        self.konu = konu
        kart_sayisi = len(veriler[konu].get("kartlar", []))
        soru_sayisi = len(veriler[konu].get("sorular", []))
        self.baslik.text = f"[b]{konu}[/b]\nKart: {kart_sayisi} | Soru: {soru_sayisi}"

    def kartlara_git(self, instance):
        self.manager.get_screen("kart").yukle(self.konu)
        self.manager.current = "kart"

    def teste_git(self, instance):
        self.manager.get_screen("test").yukle(self.konu)
        self.manager.current = "test"


class KartEkrani(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.konu = ""
        self.kartlar = []
        self.i = 0
        root = BoxLayout(orientation="vertical", padding=12, spacing=10)
        self.sayac = make_label("", 16, 35)
        root.add_widget(self.sayac)
        self.soru = make_label("", 22)
        root.add_widget(self.soru)
        self.cevap = make_label("", 20)
        root.add_widget(self.cevap)
        btn_goster = make_button("KONTROL ET", 60, (0.12, 0.45, 0.30, 1), 20)
        btn_goster.bind(on_press=self.cevap_goster)
        root.add_widget(btn_goster)
        nav = BoxLayout(size_hint_y=None, height=60, spacing=8)
        btn_onceki = make_button("⬅ ÖNCEKİ", 60, (0.20, 0.22, 0.35, 1), 17)
        btn_onceki.bind(on_press=self.onceki)
        btn_sonraki = make_button("SONRAKİ ➡", 60, (0.20, 0.22, 0.35, 1), 17)
        btn_sonraki.bind(on_press=self.sonraki)
        nav.add_widget(btn_onceki)
        nav.add_widget(btn_sonraki)
        root.add_widget(nav)
        btn_geri = make_button("⬅ KONUYA DÖN", 58, (0.25, 0.25, 0.32, 1), 17)
        btn_geri.bind(on_press=lambda x: setattr(self.manager, "current", "konu"))
        root.add_widget(btn_geri)
        self.add_widget(root)

    def yukle(self, konu):
        self.konu = konu
        self.kartlar = veriler[konu].get("kartlar", [])
        self.i = 0
        self.yenile()

    def yenile(self):
        if not self.kartlar:
            self.sayac.text = "0/0"
            self.soru.text = "Bu konuya henüz kart eklenmedi."
            self.cevap.text = ""
            return
        kart = self.kartlar[self.i]
        self.sayac.text = f"Kart {self.i + 1}/{len(self.kartlar)}"
        self.soru.text = kart.get("soru", "")
        self.cevap.text = ""

    def cevap_goster(self, instance):
        if self.kartlar:
            self.cevap.text = "✅ " + self.kartlar[self.i].get("cevap", "")

    def sonraki(self, instance):
        if self.kartlar:
            self.i = (self.i + 1) % len(self.kartlar)
            self.yenile()

    def onceki(self, instance):
        if self.kartlar:
            self.i = (self.i - 1) % len(self.kartlar)
            self.yenile()


class TestEkrani(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.konu = ""
        self.sorular = []
        self.i = 0
        self.btnler = []
        self.dogru_sayisi = 0
        self.cevaplandi = False

        root = BoxLayout(orientation="vertical", padding=10, spacing=8)
        self.sayac = make_label("", 16, 35)
        root.add_widget(self.sayac)
        self.soru = make_label("", 19)
        root.add_widget(self.soru)

        self.sec_scroll = ScrollView(size_hint_y=0.48)
        self.sec = BoxLayout(orientation="vertical", spacing=8, size_hint_y=None)
        self.sec.bind(minimum_height=self.sec.setter("height"))
        self.sec_scroll.add_widget(self.sec)
        root.add_widget(self.sec_scroll)

        self.sonuc = make_label("", 17, 80)
        root.add_widget(self.sonuc)

        nav = BoxLayout(size_hint_y=None, height=58, spacing=8)
        btn_geri_soru = make_button("⬅ ÖNCEKİ", 58, (0.20, 0.22, 0.35, 1), 16)
        btn_geri_soru.bind(on_press=self.onceki)
        btn_sonraki = make_button("SONRAKİ ➡", 58, (0.20, 0.22, 0.35, 1), 16)
        btn_sonraki.bind(on_press=self.sonraki)
        nav.add_widget(btn_geri_soru)
        nav.add_widget(btn_sonraki)
        root.add_widget(nav)

        btn_konu = make_button("⬅ KONUYA DÖN", 54, (0.25, 0.25, 0.32, 1), 16)
        btn_konu.bind(on_press=lambda x: setattr(self.manager, "current", "konu"))
        root.add_widget(btn_konu)
        self.add_widget(root)

    def yukle(self, konu):
        self.konu = konu
        self.sorular = veriler[konu].get("sorular", [])
        self.i = 0
        self.dogru_sayisi = 0
        self.yenile()

    def yenile(self):
        self.sec.clear_widgets()
        self.btnler = []
        self.sonuc.text = ""
        self.cevaplandi = False
        if not self.sorular:
            self.sayac.text = "0/0"
            self.soru.text = "Bu konuya henüz soru eklenmedi."
            return
        s = self.sorular[self.i]
        self.sayac.text = f"Soru {self.i + 1}/{len(self.sorular)} | Doğru: {self.dogru_sayisi}"
        self.soru.text = f"[b]{self.i + 1})[/b] {s.get('soru', '')}"
        for harf, metin in s.get("secenekler", {}).items():
            btn = make_button(f"{harf}) {metin}", 58, (0.18, 0.18, 0.25, 1), 16)
            btn.bind(on_press=lambda x, h=harf: self.kontrol(h))
            self.btnler.append((btn, harf))
            self.sec.add_widget(btn)

    def kontrol(self, secilen):
        if not self.sorular or self.cevaplandi:
            return
        self.cevaplandi = True
        s = self.sorular[self.i]
        dogru = s.get("cevap", "")
        if secilen == dogru:
            self.dogru_sayisi += 1
        for btn, harf in self.btnler:
            if harf == dogru:
                btn.background_color = (0, 0.60, 0, 1)
            elif harf == secilen:
                btn.background_color = (0.75, 0, 0, 1)
        aciklama = s.get("aciklama", "")
        self.sonuc.text = ("✅ Doğru!" if secilen == dogru else f"❌ Yanlış! Doğru cevap: {dogru}") + (f"\n{aciklama}" if aciklama else "")
        self.sayac.text = f"Soru {self.i + 1}/{len(self.sorular)} | Doğru: {self.dogru_sayisi}"

    def sonraki(self, instance):
        if self.sorular:
            self.i = (self.i + 1) % len(self.sorular)
            self.yenile()

    def onceki(self, instance):
        if self.sorular:
            self.i = (self.i - 1) % len(self.sorular)
            self.yenile()


class ISGMegaAkademi(App):
    def build(self):
        self.title = APP_TITLE
        sm = ScreenManager()
        sm.add_widget(AnaMenu(name="ana"))
        sm.add_widget(KonuEkrani(name="konu"))
        sm.add_widget(KartEkrani(name="kart"))
        sm.add_widget(TestEkrani(name="test"))
        return sm


if __name__ == "__main__":
    ISGMegaAkademi().run()
