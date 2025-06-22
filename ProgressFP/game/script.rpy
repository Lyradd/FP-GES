# =================================================================
# BAGIAN INISIALISASI & DEFINISI AWAL
# =================================================================

# Bagian Python untuk mendefinisikan Class Item (saat ini belum diaktifkan)
init python:
    # Setiap item akan memiliki nama, deskripsi, gambar ikon, dan efek jika bisa digunakan.
    class Item(object):
        def __init__(self, name, description, image_path, effect=None, is_key_item=False):
            self.name = name
            self.description = description
            self.image_path = image_path # Path ke gambar ikon item
            self.effect = effect # Fungsi yang akan dipanggil saat item digunakan
            self.is_key_item = is_key_item # Tandai jika ini adalah item penting (tidak bisa dibuang/dijual)

        # Fungsi untuk menggunakan item
        def use_item(self):
            if self.effect:
                # Jika item punya efek, panggil fungsinya
                return self.effect()
            # Jika tidak, kembalikan pesan bahwa item tidak bisa digunakan
            renpy.say(player, "Sepertinya ini tidak bisa digunakan sekarang.")
            return False

    # Ini adalah fungsi yang akan dijalankan saat item "Kopi Jahe" digunakan.
    def effect_kopi_jahe():
        # Memulihkan 20 energi, maksimum 100.
        store.energy = min(store.energy + 20, 100)
        # Hapus item dari inventaris setelah digunakan.
        # inventory.remove(kopi_jahe) # Anda perlu mendefinisikan 'inventory' dan 'kopi_jahe'
        # Tampilkan pesan ke pemain.
        renpy.say(player, "Ah... Wedang jahe buatan Nenek memang yang terbaik! Aku merasa lebih berenergi.")
        return True

# Definisi gambar splash screen
image splash = "splash.png"

# ============================
# === VARIABEL GAME & EKONOMI ===
# ============================
default day = 1
default reputation = 40
default happiness = 50
default energy = 100
default books = 20
default cash = 100000
default player_name = ""
default current_location = "perpustakaan"

# Variabel Hubungan & Status
default relationship_sari = 30
default reputation_desa = 0

# Variabel Status Harian
default daily_morning_event_done = False
default help_visitors_done_today = False
default organize_books_done_today = False
default education_program_done_today = False
default rest_done_today = False
default talk_grandparents_done_today = False

# Variabel Upgrade Ekonomi
default shelves_upgraded = False
default tables_upgraded = False
default daily_donation = 0

# Variabel Pengunjung
default student1_state = "browsing"
default student2_state = "reading"
default teacher_state = "researching"
default child_state = "storytime"

# Variabel Kondisi Buku
default fiction_condition = "good"
default science_condition = "good"
default history_condition = "good"

# Variabel Kondisi Game
default game_over = False
default victory = False


# ========================
# === SCREENS (UI) ===
# ========================

# Screen untuk menampilkan status harian
screen daily_status():
    modal True
    frame:
        xalign 0.5 yalign 0.5
        xpadding 30 ypadding 20
        vbox:
            spacing 10
            text "Laporan Status" size 28 xalign 0.5
            null height 10

            text "Hari ke-[day]" size 24
            hbox:
                spacing 20
                vbox:
                    text "Reputasi: [reputation]/100"
                    bar value reputation range 100 xmaximum 200
                vbox:
                    text "Kebahagiaan: [happiness]/100"
                    bar value happiness range 100 xmaximum 200
            hbox:
                spacing 20
                vbox:
                    text "Energi: [energy]/100"
                    bar value energy range 100 xmaximum 200
                vbox:
                    text "Jumlah Buku: [books]"
            hbox:
                spacing 20
                vbox:
                    text "Hubungan Sari: [relationship_sari]/100"
                    bar value relationship_sari range 100 xmaximum 200
                vbox:
                    text "Reputasi Desa: [reputation_desa]/50"
                    bar value reputation_desa range 40 xmaximum 200
            hbox:
                spacing 20
                vbox:
                    text "Kas: Rp[cash:,]"
                    if daily_donation > 0:
                        text "Donasi Hari Ini: Rp[daily_donation:,]"

            null height 15
            textbutton "Tutup" action Hide("daily_status") xalign 0.5

# Screen untuk aksi di perpustakaan
screen library_actions():
    modal True
    frame:
        xalign 0.5 yalign 0.5
        xpadding 30 ypadding 20
        vbox:
            spacing 15
            text "Aktivitas di Perpustakaan" size 24

            if energy >= 20 and not help_visitors_done_today:
                textbutton "Bantu Pengunjung (-20 Energi)" action [SetVariable("energy", energy - 20), Jump("help_visitors")]
            else:
                textbutton "Bantu Pengunjung (Selesai/Energi Kurang)" sensitive False

            if energy >= 15 and not organize_books_done_today:
                textbutton "Atur Buku (-15 Energi)" action [SetVariable("energy", energy - 15), Jump("organize_books")]
            else:
                textbutton "Atur Buku (Selesai/Energi Kurang)" sensitive False
            
            if energy >= 30 and not education_program_done_today:
                textbutton "Program Edukasi (-30 Energi)" action [SetVariable("energy", energy - 30), Jump("education_program")]
            else:
                textbutton "Program Edukasi (Selesai/Energi Kurang)" sensitive False

            textbutton "Manajemen Perpustakaan" action [Hide("library_actions"), Show("management_actions")]
            textbutton "Lihat Laporan Harian" action Jump("daily_report")
            textbutton "Tutup" action Hide("library_actions")

# Screen untuk manajemen ekonomi (gabungan upgrade dan beli buku)
screen management_actions():
    modal True
    frame:
        xalign 0.5 yalign 0.5
        xpadding 30 ypadding 20
        vbox:
            spacing 15
            text "Manajemen Perpustakaan" size 24
            
            text "Upgrade Fasilitas:"
            # Opsi Upgrade Rak Buku
            if not shelves_upgraded:
                if cash >= 150000:
                    textbutton "Perbaiki Rak Buku (Rp 150.000)" action [SetVariable("cash", cash - 150000), Jump("upgrade_shelves")]
                else:
                    textbutton "Perbaiki Rak Buku (Rp 150.000) - Uang tidak cukup" sensitive False
            else:
                textbutton "Rak Buku Sudah Diperbaiki" sensitive False

            # Opsi Upgrade Meja & Kursi
            if not tables_upgraded:
                if cash >= 100000:
                    textbutton "Beli Meja & Kursi Baru (Rp 100.000)" action [SetVariable("cash", cash - 100000), Jump("upgrade_tables")]
                else:
                    textbutton "Beli Meja & Kursi Baru (Rp 100.000) - Uang tidak cukup" sensitive False
            else:
                textbutton "Meja & Kursi Sudah Baru" sensitive False
            
            null height 10
            text "Pengadaan Buku:"
            if cash >= 50000:
                textbutton "Beli 5 Buku Fiksi (Rp 50.000)" action [SetVariable("cash", cash - 50000), SetVariable("books", books + 5), SetVariable("reputation", reputation + 1), Hide("management_actions")]
            else:
                textbutton "Beli 5 Buku Fiksi (Uang Kurang)" sensitive False

            if cash >= 75000:
                textbutton "Beli 5 Buku Sains (Rp 75.000)" action [SetVariable("cash", cash - 75000), SetVariable("books", books + 5), SetVariable("reputation", reputation + 2), Hide("management_actions")]
            else:
                textbutton "Beli 5 Buku Sains (Uang Kurang)" sensitive False

            null height 10
            textbutton "Kembali" action Hide("management_actions")

# Screen untuk aksi di rumah
screen home_actions():
    modal True
    frame:
        xalign 0.5 yalign 0.5 xpadding 30 ypadding 20
        vbox:
            spacing 15
            text "Aktivitas di Rumah" size 24

            if not rest_done_today:
                textbutton "Istirahat (+40 Energi)" action [SetVariable("energy", min(energy + 40, 100)), SetVariable("rest_done_today", True), Hide("home_actions"), Jump("rest")]
            else:
                textbutton "Istirahat (Sudah)" sensitive False
            
            if not talk_grandparents_done_today:
                textbutton "Mengobrol dengan Kakek & Nenek" action Jump("talk_grandparents")
            else:
                textbutton "Mengobrol (Sudah)" sensitive False

            textbutton "Akhiri Hari dan Tidur" action [Hide("home_actions"), Jump("go_to_sleep")]
            textbutton "Tutup" action Hide("home_actions")

# Screen UI Icons (Kembali ke sistem original Anda)
screen top_right_icons():
    zorder 100 
    hbox:
        align (0.98, 0.03)
        spacing 15
        imagebutton:
            idle Transform("images/ui/icon_status.png", zoom=0.2)
            focus_mask True
            action ToggleScreen("daily_status")

screen top_left_icons():
    zorder 100
    hbox:
        align (0.02, 0.03)
        spacing 15 
        # Tombol aksi akan berubah tergantung lokasi
        if current_location == "perpustakaan":
            imagebutton:
                idle Transform("images/ui/icon_todolist.png", zoom=0.2)
                focus_mask True
                action ToggleScreen("library_actions")
        elif current_location == "rumah":
            imagebutton:
                idle Transform("images/ui/icon_home_action.png", zoom=0.2)
                focus_mask True
                action ToggleScreen("home_actions")

screen top_center_icons():
    zorder 100
    hbox:
        align (0.5, 0.03)
        spacing 50
        textbutton "Perpustakaan" action Jump("go_to_library") sensitive current_location != "perpustakaan" and energy >= 5
        textbutton "Rumah" action Jump("go_home") sensitive current_location != "rumah"

# Screen untuk menampilkan Good Ending
screen good_ending_screen():
    modal True
    zorder 100
    frame:
        align (0.5, 0.5)
        background "#6d4c41" 
        xpadding 60
        ypadding 40
        vbox:
            spacing 15 
            text "GOOD ENDING" size 42 color "#FFFFFF" xalign 0.5
            text "Perpustakaan Berjaya\n& Cinta Bersemi" size 26 color "#FFFFFF" xalign 0.5

# ========================
# === GAME START & PROLOGUE ===
# ========================

label splashscreen:
    scene black
    pause 1.0
    show splash with dissolve
    pause 2.0
    scene black with dissolve
    hide splash
    return

label start:
    call splashscreen
    scene black
    "Selamat datang di Simulasi Pustakawan Desa Welasari"
    
    python:
        player_name = renpy.input("Masukkan nama karakter utama:", default="Aditya", length=20).strip()
        if not player_name:
            player_name = "Aditya"
        
        confirmed = False
        while not confirmed:
            confirm = renpy.input(f"Nama kamu adalah {player_name}. Benar? (ya/tidak)", default="ya", length=5)
            if confirm.lower() in ["ya", "y", "yes", "iya", "oke", "ok", "benar", "betul"]:
                confirmed = True
            else:
                player_name = renpy.input("Masukkan nama baru:", default=player_name, length=20).strip()
                if not player_name:
                    player_name = "Aditya"

    scene bg city with fade
    play music "audio/melancholy.wav" fadeout 1.0
    
    "Kota ini tak pernah tidur."
    "Gedung-gedung tinggi menjulang, lampu terang yang tak pernah padam, dan suara klakson yang menjadi lagu pengantar tidur."
    "Sudah dua tahun [player_name] bekerja di sini sebagai copywriter di sebuah agensi periklanan."
    "Rutinitas yang tak berujung: rapat pagi, meeting siang, revisi tanpa akhir, lalu pulang larut malam."

    show mc tired at right with dissolve
    player "Jangankan tenang, tidur nyenyak saja gabisa."
    player "Setiap pagi, aku terbangun dengan perasaan hampa. Bukan karena pekerjaanku buruk, tapi... ada sesuatu yang hilang."

    "Hingga suatu malam, setelah lembur sampai larut, aku menerima telepon dari Kakek."

    show mc idle at left with moveinleft
    player "Halo?"
    kakek "..."
    kakek "[player_name]... ini Kakek."

    player "Kakek? Ada apa menelepon selarut ini? Apa semuanya baik-baik saja?"
    "Suaranya terdengar lelah, tidak seperti biasanya."

    kakek "Kakek baik-baik saja, Nak. Maaf mengganggu malam-malam. Kakek hanya... terpikir sesuatu."
    kakek "Umur tidak bisa bohong, kakek tidak bisa mengurusi perpustakaan kita sendirian lagi."

    player "Perpustakaan? Maksud Kakek yang di desa Welasari itu?"
    kakek "Iya, Nak. Perpustakaan kecil itu. Tempat yang sudah menjadi bagian dari keluarga kita sejak lama."

    kakek "Kakek sudah berusaha merawatnya, tapi semakin hari semakin sulit."
    kakek "Kakek tidak ingin tempat itu ditutup begitu saja."
    kakek "Kakek ingin kamu kembali ke desa, membantu Kakek mengurus perpustakaan itu."

    menu:
        "Tapi... pekerjaanku di sini, Kek. Aku tidak bisa meninggalkannya begitu saja.":
            player "Tapi... pekerjaanku di sini, Kek. Aku tidak bisa meninggalkannya begitu saja."
            kakek "Kakek mengerti, Nak. Kakek hanya... berharap ada yang bisa meneruskan perpustakaan ini"
        
        "Aku akan memikirkannya, Kek.":
            player "Aku akan memikirkannya, Kek. Beri aku waktu."
            kakek "Tentu, Nak. Pikirkanlah baik-baik."

    kakek "Tempat itu bukan hanya tumpukan kertas, [player_name]. Itu adalah peninggalan orang tuamu, kenangan terakhir dari mereka."
    kakek "Kakek hanya tidak ingin kenangan itu memudar."
    kakek "Sudah dulu, ya. Jaga dirimu baik-baik di sana."

    "Telepon ditutup. Aku termangu di kamarku yang sempit, dikelilingi gemerlap lampu kota yang terasa dingin."
    "Kata-kata Kakek terus terngiang, menusuk langsung ke perasaan hampa yang selama ini kurasakan."
    
    player "Peninggalan orang tuaku... Kenangan terakhir dari mereka."
    player "Apa yang sebenarnya aku cari di sini?"
    
    "Malam itu juga, tanpa pikir panjang, aku memesan tiket kereta untuk pulang."

    scene bg train with fade
    
    "Aku duduk di dalam kereta, menatap keluar jendela."
    "Kereta diisi oleh orang-orang yang sibuk dengan gadget mereka, tapi pikiranku melayang jauh ke masa lalu."
    "Perjalanan ini terasa seperti perjalanan kembali ke rumah, meskipun rumah itu sudah lama kutinggalkan."
    
    scene black with fade
    pause 2.0
 
    player "Aku tertidur... Ketika terbangun, waktu sudah menunjukkan pagi dan kereta sudah memasuki stasiun kecil di desa Welasari."

    scene bg stasiun with fade
    "Ketika aku membuka mata, hari sudah pagi dan pemandangan di luar jendela telah berubah total."
    "Perjalanan kereta cukup panjang, tapi sama sekali tidak terasa karena aku menikmatinya."

    show mc idle at left with moveinleft
    player "Akhirnya aku sampai di desa Welasari. stasiun ini masih sama seperti yang kuingat."
    hide mc with dissolve
    show kakek smile at right with moveinright
    kakek "[player_name], kakek ada di sini!"
    hide kakek with dissolve

    "Kakek sudah menunggu di stasiun, aku langusng menghampirinya dan memeluknya erat."

    scene bg village with fade
    play music "audio/nostalgia.mp3" fadeout 1.0

    "Desa Welasari masih sama seperti yang kuingat."
    "Udara segar, sawah menghijau, dan senyum hangat warga yang saling menyapa."
    "Kakek menjemputku di stasiun dengan mobil tuanya. Wajahnya berkeriput tapi matanya masih berbinar."

    show bg house with fade
    show kakek smile at right
    show nenek smile at left
    with dissolve
    kakek "Selamat datang di rumah, [player_name]. Nenek sudah menyiapkan wedang jahe spesial untukmu."
    nenek "Duduklah nak, kau pasti lelah setelah perjalanan jauh."

    menu:
        "Kakek, walaupun sudah lama meninggalkan desa, rasanya lega sekali pulang.":
            $ reputation_desa += 2
            kakek "Rumah akan selalu menantimu, Nak."
        "Nenek, masakan rumah terasa hangat di hati.":
            $ happiness += 3
            nenek "Sudah lama nenek tidak masak untukmu, [player_name]."

    scene bg library outside with fade
    "Perpustakaan kecil itu masih berdiri di ujung jalan setapak."
    "Terlihat dari jauh, catnya telah mengelupas, tapi bangunannya masih bagus dan kokoh."

    "Kamu dan Kakek berjalan menyusuri jalan setapak hingga tiba di depan bangunan yang sudah usang namun familier."

    show kakek smile at right with moveinright
    kakek "Inilah dia, Nak. Tempat bagi ratusan cerita yang menunggu untuk dibaca kembali."
    show mc idle at left with moveinleft
    player "Kondisinya... lebih buruk dari yang kuingat, Kek."

    hide kakek with moveoutright

    "Saat kamu sedang mengamati cat yang mengelupas, seorang gadis sebayanya yang sedang menyapu dedaunan kering di dekatnya menoleh."
    
    show sari happy at right with moveinright

    s "[player_name]? Kamu kah itu? Wah, akhirnya kamu pulang!" with hpunch
    player "Sari? Kamu masih ingat aku? Sudah lama sekali, ya."
    s "Tentu saja! Aku senang sekali melihatmu kembali. Selamat datang, [player_name]."
    
    show kakek smile at center with moveinleft
    with dissolve

    kakek "Sari ini salah satu pengunjung paling setia, bahkan saat sepi sekalipun."
    s "Aku hanya tidak ingin tempat ini benar-benar dilupakan. Sekarang kamu sudah di sini, aku yakin semuanya akan jadi lebih baik!"
    
    $ relationship_sari += 5

    player "Aku akan berusaha sebaik mungkin."
    kakek "Baiklah, mari kita masuk. Ada banyak hal yang perlu kita bicarakan dan kerjakan."

    hide kakek
    hide sari
    hide mc

    scene bg library inside with fade
    "Aroma kertas tua yang khas langsung menyambutku."
    "Rak-rak buku yang berdebu dan tumpukan yang tak teratur menjadi pemandangan pertama."

    show kakek serious at right with moveinright
    kakek "Seperti yang kamu lihat... Sudah setahun terakhir ini Kakek kesulitan merawatnya sendirian."
    kakek "Buku-buku mulai rusak, pengunjung berkurang, dan dana operasional hampir habis."
    kakek "Tapi Kakek yakin, dengan bantuanmu, kita bisa menghidupkan kembali tempat ini."
    show mc idle at left with moveinleft
    player "Aku mengerti, Kek. Mari kita mulai bekerja."
    
    jump prologue_mission

# ========================
# PROLOGUE MISSION
# ========================
label prologue_mission:
    scene bg library 2 with fade
    show kakek at right with dissolve
    
    "Kakek memandu keliling perpustakaan. Kondisinya lebih buruk dari yang kubayangkan:"
    "- Rak buku berdebu dan beberapa lapuk."
    "- Buku-buku berserakan tanpa katalog yang jelas."
    "- Beberapa koleksi bahkan rusak dimakan rayap."

    kakek "Untuk awal, bagaimana kalau kita fokus membersihkan rak utama dan membuat daftar katalog sederhana?"

    menu:
        "Kumpulkan 10 buku rusak ringan untuk diperbaiki hari ini.":
            $ fiction_condition = "fair"
            $ science_condition = "fair"
            $ history_condition = "fair"
            kakek "Pilihan bijak. Memperbaiki buku adalah dasar dari perpustakaan yang baik."
        "Susun ulang rak sesuai abjad nama pengarang.":
            kakek "Sistem yang rapi akan memudahkan pengunjung mencari buku."

    menu:
        "Tolong ajarkan cara mencatat katalog dengan rapi.":
            kakek "Dengan senang hati. Lihat, begini cara Kakek mengorganisirnya..."
            "Kakek dengan sabar mengajariku sistem klasifikasi sederhana."
            "Aku belajar membedakan kategori fiksi, non-fiksi, dan referensi."
        "Saya coba belajar sendiri, Kek.":
            $ energy -= 15
            $ reputation += 2
            "Aku mencoba memahami sistem katalog sendiri."
            "Butuh waktu lebih lama, tapi akhirnya aku menemukan polanya."

    scene bg rak with fade
    "Hari pertama berakhir dengan capaian kecil tapi berarti."
    "Beberapa rak sudah lebih rapi, daftar katalog mulai terbentuk, dan Kakek terlihat lega."
    
    $ day += 1
    jump tutorial

# =================================================================
# TUTORIAL - Penjelasan Mekanika Game oleh Kakek
# =================================================================
label tutorial:
    scene bg library desk with fade
    show kakek smile at right with dissolve

    kakek "Kerja yang bagus untuk hari pertama, [player_name]. Kakek terkesan dengan semangatmu."
    kakek "Sebelum kamu benar-benar mulai mengelola perpustakaan ini sendirian, ada beberapa hal penting yang perlu kamu pahami."

    player "Hal penting apa, Kek?"

    kakek "Mengelola perpustakaan ini bukan hanya soal menata buku. Ini tentang membangun kembali jiwanya."
    kakek "Ada beberapa hal yang harus kamu jaga keseimbangannya."

    label tutorial_menu:
        menu:
            "Jelaskan tentang Reputasi dan Kebahagiaan.":
                kakek "Tentu. Reputasi adalah pandangan warga desa terhadap perpustakaan kita. Semakin sering kamu membantu pengunjung, reputasi akan naik."
                kakek "Sementara Kebahagiaan adalah cerminan semangatmu sendiri. Kalau kamu merasa senang, kamu akan lebih produktif."
                player "Jadi, aku harus menjaga keduanya tetap tinggi."
                kakek "Tepat sekali."
                jump tutorial_menu

            "Untuk apa gunanya Energi?":
                kakek "Energi itu tenagamu. Setiap aktivitas di perpustakaan akan menguras energimu. Jika habis, kamu harus pulang untuk istirahat."
                player "Bagaimana cara memulihkannya, Kek?"
                kakek "Istirahat di rumah, atau tidur di malam hari akan memulihkan energimu sepenuhnya. Ingat, jangan memaksakan diri."
                jump tutorial_menu

            "Bagaimana dengan Hubungan dan Reputasi Desa?":
                kakek "Hubungan dengan Sari akan meningkat seiring interaksimu dengannya. Siapa tahu, persahabatan kalian bisa menjadi lebih..."
                kakek "Reputasi Desa adalah bagaimana desa secara keseluruhan memandangmu. Keputusan-keputusan besar bisa memengaruhinya."
                player "Jadi ini lebih tentang hubungan sosialku ya, Kek."
                kakek "Benar. Desa ini kecil, hubungan antar warganya sangat berarti."
                jump tutorial_menu
            
            "Lalu, Kas ini untuk apa?":
                kakek "Itu adalah dana operasional kita. Kamu bisa menggunakannya untuk membeli buku baru atau memperbaiki fasilitas."
                kakek "Terkadang, akan ada donasi atau dana dari desa jika mereka puas dengan kinerjamu."
                player "Aku harus bijak menggunakannya."
                kakek "Tentu saja."
                jump tutorial_menu

            "Aku sudah mengerti, Kek. Aku siap untuk besok!":
                pass

    kakek "Bagus. Kakek percaya padamu, [player_name]. Ingatlah semua itu baik-baik."
    kakek "Sekarang, pulang dan istirahatlah. Petualanganmu yang sesungguhnya dimulai besok."

    hide kakek with dissolve
    scene bg kamar with fade
    show mc idle at right with moveinright
    player "Aku harus beristirahat. Besok akan menjadi hari yang panjang dan penuh tantangan."
    hide mc idle at right with moveoutright
    
    scene bg house with fade
    show mc idle at center with moveinbottom
    player "Kakek, Nenek, aku pergi ke perpustakaan dulu ya!"
    show kakek smile at right with moveinright
    kakek "Baik, [player_name]. Semoga harimu menyenangkan!"
    show nenek smile at left with moveinleft
    nenek "Jangan memaksakan diri, ya. Istirahatlah jika lelah."
    hide kakek smile with moveoutright
    hide nenek smile with moveoutleft
    player "Iya, Nek. Aku akan berhati-hati."
    hide mc idle with moveoutbottom

    jump daily_routine


# ========================
# === MAIN GAME LOOP ===
# ========================
label daily_routine:
    # Event pagi hari
    if not daily_morning_event_done:
        $ daily_morning_event_done = True
        if day == 2:
            scene bg library outside with fade
            "Saat aku hendak membuka pintu perpustakaan, seseorang sudah menungguku di depan."
            show sari happy at right with moveinright
            s "Selamat pagi, [player_name]! Semangat untuk hari pertamanya, ya!"
            show mc idle at left with moveinleft
            player "Sari! Pagi. Kamu sengaja datang pagi-pagi sekali?"
            s "Tentu saja. Aku hanya ingin memberimu ini."
            "Sari menyodorkan sebuah kotak bekal kecil."
            s "Ini kue jahe buatan ibuku, katanya bagus untuk menambah energi. Anggap saja sebagai dukungan dariku."
            player "Wah... Terima kasih banyak, Sari. Ini sangat berarti bagiku."
            $ happiness += 3
            $ relationship_sari += 5
            s "Sama-sama! Kalau begitu aku tinggal dulu, ya. Semangat!"
            hide sari with moveoutleft
            hide mc with moveoutright
            player "Pagi ini dimulai dengan sangat baik."
        else:
            $ random_event = renpy.random.randint(1, 4)
            if random_event == 1:
                $ books += 5
                $ reputation = min(reputation + 5, 100)
                show donor at right with dissolve
                "Warga" "Kami ingin menyumbangkan beberapa buku untuk perpustakaan."
                player "Terima kasih banyak atas donasinya!"
                hide donor with dissolve
            elif random_event == 2:
                $ happiness = min(happiness + 10, 100)
                $ reputation = min(reputation + 8, 100)
                show vip at right with dissolve
                "Tamu" "Saya mendengar perpustakaan ini sangat bagus. Saya salah satu penulis dan ingin mengadakan workshop di sini."
                player "Wow! Ini kehormatan bagi kami!"
                hide vip with dissolve
            elif random_event == 3:
                $ energy = max(energy - 20, 0)
                $ reputation = min(reputation + 3, 100)
                show technician at right with dissolve
                "Teknisi" "Kami dari tim maintenance datang untuk memeriksa sistem AC."
                player "Baik, silakan. Perpustakaan akan sedikit berisik hari ini."
                hide technician with dissolve
            elif random_event == 4 and relationship_sari < 80:
                show sari happy at center with dissolve
                s "Pagi, [player_name]! Aku membawakan beberapa kue buatan ibuku. Untukmu semangat bekerja."
                menu:
                    "Wah, terima kasih banyak, Sari! Ini sangat berarti.":
                        player "Wah, terima kasih banyak, Sari! Ini sangat berarti."
                        $ happiness += 5
                        $ relationship_sari += 3
                        s "Sama-sama! Habiskan, ya!"
                    "Terima kasih, tapi seharusnya tidak perlu repot-repot.":
                        player "Terima kasih, tapi seharusnya tidak perlu repot-repot."
                        $ relationship_sari += 1
                        s "Tidak apa-apa, kok. Anggap saja dukungan dariku."
                hide sari with dissolve
            else:
                "Hari yang tenang di perpustakaan..."
    
    # Cek kondisi menang/kalah
    if reputation <= 0 or happiness <= 0 or day > 30:
        jump game_over
    if reputation >= 100 and happiness >= 80:
        jump victory
    if energy <= 10 and current_location != "rumah":
        player "Aku terlalu lelah... sebaiknya aku pulang untuk istirahat."
        jump force_end_day

    # Loop berdasarkan lokasi
    if current_location == "perpustakaan":
        jump library_loop
    elif current_location == "rumah":
        jump home_loop

label library_loop:
    scene bg library
    show screen top_right_icons
    show screen top_left_icons
    show screen top_center_icons
    $ renpy.ui.interact()

label home_loop:
    scene bg house
    show screen top_right_icons
    show screen top_left_icons
    show screen top_center_icons
    $ renpy.ui.interact()


# ========================
# === NAVIGASI & LOKASI ===
# ========================
label go_to_library:
    $ energy -= 5
    player "Oke, aku akan pergi ke perpustakaan. (-5 Energi)"
    $ current_location = "perpustakaan"
    jump daily_routine

label go_home:
    $ energy -= 5
    player "Aku akan pulang ke rumah. (-5 Energi)"
    $ current_location = "rumah"
    jump daily_routine

# ========================
# === AKSI & EVENT ===
# ========================

# Aksi di Perpustakaan
label help_visitors:
    hide screen library_actions
    $ help_visitors_done_today = True
    
    scene bg library with dissolve
    $ visitor_choice = renpy.random.randint(1, 4)
 
    if visitor_choice == 1:
        $ current_visitor = "siswa"
        $ student1_state = "asking_help"
        show student at right with moveinright
        "Siswa" "Maaf, bisakah Anda membantu saya menemukan buku tentang fisika?"
        menu:
            "Tentu, mari kita cari bersama.":
                player "Tentu, mari kita cari bersama. Bagian sains ada di sebelah sini."
                scene bg_library_physics with dissolve
                show mc idle at left with moveinleft
                player "Nah, ini dia rak untuk buku-buku fisika. Kamu cari tentang topik spesifik?"
                show student at right with moveinright
                "Siswa" "Tentang mekanika kuantum, kak. Wah, koleksinya lumayan lengkap juga, ya!"
                $ student1_state = "satisfied"
                $ happiness = min(happiness + 3, 100)
                $ reputation = min(reputation + 2, 100)
                "Siswa" "Ini buku yang kucari! Terima kasih banyak, kak! Anda sangat membantu."
            "Saya sibuk sekarang, coba tanya yang lain.":
                player "Saya sibuk sekarang, coba tanya yang lain."
                $ student1_state = "leaving"
                $ happiness = max(happiness - 3, 0)
                $ reputation = max(reputation - 2, 0)
                "Siswa" "Oh... baiklah."
        hide student with moveoutright
    elif visitor_choice == 2:
        $ current_visitor = "guru"
        $ teacher_state = "asking_help"
        show teacher at right with moveinright
        "Guru" "Saya sedang meneliti untuk makalah, apakah Anda punya referensi tentang sejarah lokal?"
        menu:
            "Ya, kami punya beberapa koleksi bagus di rak sejarah.":
                player "Ya, kami punya beberapa koleksi bagus di rak sejarah."
                scene bg_library_history with dissolve
                show mc idle at left with moveinleft
                player "Ini dia, rak sejarah lokal. Ada beberapa buku yang mungkin Anda butuhkan."
                show teacher at right with moveinright
                "Guru" "Wah, ini sangat membantu! Saya akan mencatat beberapa judul yang menarik."
                $ teacher_state = "researching"
                $ happiness = min(happiness + 3, 100)
                $ reputation = min(reputation + 2, 100)
                "Guru" "Sempurna! Ini sangat membantu penelitian saya."
            "Maaf, koleksi sejarah lokal kami terbatas.":
                player "Maaf, koleksi sejarah lokal kami terbatas."
                $ teacher_state = "leaving"
                $ happiness = max(happiness - 3, 0)
                "Guru" "Yah, sayang sekali. Mungkin lain kali."
        hide teacher with moveoutleft
    elif visitor_choice == 3:
        $ current_visitor = "anak kecil"
        $ child_state = "asking_questions"
        show child at right with moveinright
        "Anak Kecil" "Aku suka dinosaurus! Punya buku dinosaurus yang gambarnya bagus?"
        menu:
            "Tentu! Mari kita ke bagian buku anak-anak.":
                player "Tentu! Mari kita ke bagian buku anak-anak."
                scene bg_library_child with dissolve
                show mc idle at left with moveinleft
                player "Ini dia, rak buku anak-anak. Bagian dinosaurus ada di sini."
                show child at right with moveinright
                "Anak Kecil" "Wah, gambarnya keren! Aku suka dinosaurus T-Rex!"
                $ child_state = "happy"
                $ happiness = min(happiness + 3, 100)
                $ reputation = min(reputation + 2, 100)
                "Anak Kecil" "Yay! Terima kasih kak!"
            "Mungkin lain kali ya, sekarang sedang sibuk.":
                player "Mungkin lain kali ya, sekarang sedang sibuk."
                $ child_state = "tired"
                $ happiness = max(happiness - 5, 0)
                $ reputation = max(reputation - 2, 0)
                "Anak Kecil" "Awww... aku kecewa."
        hide child with moveoutright
    else:
        $ current_visitor = "siswa lain"
        $ student2_state = "asking_help"
        show student2 at right with moveinright
        "Siswa Lain" "Saya kesulitan mencari buku referensi untuk tugas matematika saya."
        menu:
            "Saya akan tunjukkan di mana bagian bukunya.":
                player "Saya akan tunjukkan di mana bagian bukunya."
                scene bg_library_math with dissolve
                show mc idle at left with moveinleft
                player "Ini dia, rak buku matematika. Semua buku referensi matematika ada di sini."
                show student2 at right with moveinright
                "Siswa Lain" "Wah, terima kasih! Aku tidak tahu harus mulai dari mana."
                $ student2_state = "studying"
                $ happiness = min(happiness + 3, 100)
                $ reputation = min(reputation + 2, 100)
                "Siswa Lain" "Terima kasih! Sekarang saya bisa mengerjakan tugas."
            "Coba cari di katalog komputer dulu.":
                player "Coba cari di katalog komputer dulu."
                $ student2_state = "browsing"
                $ happiness = max(happiness - 3, 0)
                $ reputation = max(reputation - 2, 0)
                "Siswa Lain" "Oh, baiklah. Saya akan coba."
        hide student2 with moveoutright

    jump daily_routine

label organize_books:
    hide screen library_actions
    $ organize_books_done_today = True
    scene bg library shelves with dissolve
    player "Aku harus merapikan beberapa buku hari ini."
    $ reputation = min(reputation + 3, 100)
    player "Aku sudah merapikan buku-buku hari ini. Perpustakaan terlihat lebih rapi sekarang."
    jump daily_routine

label education_program:
    hide screen library_actions
    $ education_program_done_today = True
    scene bg library event with dissolve
    player "Aku akan mengadakan program edukasi hari ini."
    $ happiness = min(happiness + 8, 100)
    $ reputation = min(reputation + 5, 100)
    jump daily_routine

label daily_report:
    hide screen library_actions
    show screen daily_status
    pause
    hide screen daily_status
    jump daily_routine

# Aksi Ekonomi: Upgrade
label upgrade_shelves:
    hide screen management_actions
    $ shelves_upgraded = True
    $ reputation += 10
    player "Rak buku yang baru terlihat jauh lebih kokoh dan bagus. Semoga pengunjung suka. (+10 Reputasi)"
    jump daily_routine

label upgrade_tables:
    hide screen management_actions
    $ tables_upgraded = True
    $ happiness += 10
    player "Dengan meja dan kursi baru ini, suasana membaca jadi lebih nyaman. Aku jadi lebih semangat! (+10 Kebahagiaan)"
    jump daily_routine

# Aksi di Rumah
label rest:
    scene bg house with dissolve
    player "Aku butuh istirahat sebentar..."
    "Anda beristirahat di rumah dan memulihkan 40 energi."
    jump daily_routine

label talk_grandparents:
    hide screen home_actions
    $ talk_grandparents_done_today = True
    scene bg house with dissolve
    show kakek smile at right
    show nenek smile at left
    with dissolve
    player "Kek, Nek, apa kabar?"
    kakek "Kami baik-baik saja, Nak. Melihatmu bersemangat mengurus perpustakaan membuat kami senang."
    nenek "Jangan terlalu lelah, ya. Ini Nenek buatkan teh hangat."
    $ happiness = min(happiness + 5, 100)
    "Mengobrol dengan Kakek dan Nenek membuat hatimu hangat."
    hide kakek
    hide nenek
    with dissolve
    jump daily_routine

# ========================
# === AKHIR HARI & ENDINGS ===
# ========================

label go_to_sleep:
    scene bg kamar with dissolve
    player "Baiklah, waktunya istirahat untuk hari esok."
    pause 2.0
    jump next_day

label force_end_day:
    scene bg library evening with fade
    player "Aku sangat lelah... Aku tidak bisa melakukan apa-apa lagi. Sebaiknya aku langsung pulang dan tidur."
    pause 2.0
    jump next_day

label next_day:
    $ day += 1
    $ energy = 100
    # Reset status harian
    $ daily_morning_event_done = False
    $ help_visitors_done_today = False
    $ organize_books_done_today = False
    $ education_program_done_today = False
    $ rest_done_today = False
    $ talk_grandparents_done_today = False
    
    # Logika Ekonomi: Donasi Harian
    python:
        if reputation >= 80:
            daily_donation = renpy.random.randint(20000, 30000)
        elif reputation >= 60:
            daily_donation = renpy.random.randint(10000, 15000)
        else:
            daily_donation = 0
        cash += daily_donation

    # Degradasi alami
    $ happiness = max(happiness - renpy.random.randint(2, 5), 0)
    $ reputation = max(reputation - renpy.random.randint(1, 3), 0)
    
    if renpy.random.random() > 0.7:
        if fiction_condition == "good":
            $ fiction_condition = "fair"
        elif fiction_condition == "fair":
            $ fiction_condition = "poor"
    
    $ current_location = "perpustakaan" 
    scene bg library morning with fade
    if daily_donation > 0:
        "Pagi telah tiba... Saat kamu membuka kotak donasi, kamu menemukan ada tambahan uang! (Donasi: Rp[daily_donation:,])"
    else:
        "Pagi telah tiba, hari baru dimulai di Desa Welasari."
    
    jump daily_routine

label victory:
    $ victory = True
    scene bg library celebration with fade
    play music "audio/victory.mp3"
    
    "Setelah berbulan-bulan bekerja keras, perpustakaan kecil itu kini bersinar kembali..."

    # PERBAIKAN: Menampilkan gambar Pak Amin
    show pak_amin at right with dissolve
    "Kepala Desa, Pak Amin, datang memberikan pidato."
    "Pak Amin" "Atas nama Desa Welasari, saya menyatakan perpustakaan ini sebagai pusat literasi terbaik! Kami mengalokasikan dana tambahan Rp5.000.000."
    $ cash += 5000000
    hide pak_amin with dissolve

    if relationship_sari >= 80:
        scene bg library garden night with fade
        show sari happy at center with dissolve
        s "[player_name]... aku ingin menjalani hari-hari di desa ini bersamamu."
        menu:
            "Aku pun merasakan hal yang sama, Sari.":
                show sari blush with dissolve
                s "Kamu mau jadi pustakawan hidupku?"
            "Aku senang bisa kembali dan bekerja sama denganmu.":
                s "Aku juga senang, [player_name]. Mari kita jaga perpustakaan ini bersama."
    
    scene bg library sunset with fade
    "EPILOGUE: Perpustakaan Welasari kini menjadi kebanggaan desa."
    "Setiap hari ramai dikunjungi warga, dari anak-anak yang haus dongeng hingga petani yang mencari ilmu baru."
    "Aku dan Sari mengelola tempat ini bersama, dengan Kakek dan Nenek yang sesekali datang membawa kue dan cerita-cerita lama."
    "Di antara tumpukan buku dan senyum warga, aku akhirnya menemukan kedamaian yang selama ini kucari."
    "Inilah rumahku. Inilah kebahagiaan sejati."

    show screen good_ending_screen with dissolve
    pause 2.0
    hide screen good_ending_screen with dissolve

    # PERBAIKAN: Menampilkan statistik akhir sebelum kembali ke menu
    "Statistik Akhir Permainan:"
    "Total Hari Bermain: [day]"
    "Reputasi Akhir: [reputation] / 100"
    "Kebahagiaan Akhir: [happiness] / 100"
    "Hubungan dengan Sari: [relationship_sari] / 100"
    "Sisa Kas: Rp[cash:,]"
    "Terima kasih telah bermain!"
    
    # PERBAIKAN: Kembali ke Main Menu
    $ renpy.full_restart()
    return

label game_over:
    $ game_over = True
    scene bg library night with fade
    play music "audio/sad.mp3"
    
    if reputation <= 0:
        "Reputasi perpustakaan merosot tajam..."
    elif day > 30:
        "Waktu telah habis... Kamu merasa tidak membuat kemajuan berarti dan memutuskan untuk kembali ke kota."
    else:
        "Kebahagiaanku terkikis hari demi hari..."

    show kakek sad at center with dissolve
    kakek "Mungkin ini bukan jalan yang tepat untukmu, Nak."
    hide kakek sad with dissolve

    # PERBAIKAN: Menampilkan statistik akhir sebelum kembali ke menu
    "Statistik Akhir Permainan:"
    "Total Hari Bermain: [day]"
    "Reputasi Akhir: [reputation] / 100"
    "Kebahagiaan Akhir: [happiness] / 100"
    "Hubungan dengan Sari: [relationship_sari] / 100"
    "Sisa Kas: Rp[cash:,]"
    "Mungkin di lain kesempatan bisa lebih baik. Tekan untuk melanjutkan."

    pause

    # PERBAIKAN: Kembali ke Main Menu
    $ renpy.full_restart()
    return

label restart_game:
    $ day = 1
    $ reputation = 40
    $ happiness = 50
    $ energy = 100
    $ books = 20
    $ game_over = False
    $ victory = False
    $ relationship_sari = 30
    $ reputation_desa = 0
    $ cash = 1000000
    $ shelves_upgraded = False
    $ tables_upgraded = False
    jump start
