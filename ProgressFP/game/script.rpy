# init python:
#     # Setiap item akan memiliki nama, deskripsi, gambar ikon, dan efek jika bisa digunakan.
#     class Item(object):
#         def __init__(self, name, description, image_path, effect=None, is_key_item=False):
#             self.name = name
#             self.description = description
#             self.image_path = image_path # Path ke gambar ikon item
#             self.effect = effect # Fungsi yang akan dipanggil saat item digunakan
#             self.is_key_item = is_key_item # Tandai jika ini adalah item penting (tidak bisa dibuang/dijual)

#         # Fungsi untuk menggunakan item
#         def use_item(self):
#             if self.effect:
#                 # Jika item punya efek, panggil fungsinya
#                 return self.effect()
#             # Jika tidak, kembalikan pesan bahwa item tidak bisa digunakan
#             renpy.say(player, "Sepertinya ini tidak bisa digunakan sekarang.")
#             return False

#     # Ini adalah fungsi yang akan dijalankan saat item "Kopi Jahe" digunakan.
#     def effect_kopi_jahe():
#         # Memulihkan 20 energi, maksimum 100.
#         store.energy = min(store.energy + 20, 100)
#         # Hapus item dari inventaris setelah digunakan.
#         inventory.remove(kopi_jahe)
#         # Tampilkan pesan ke pemain.
#         renpy.say(player, "Ah... Wedang jahe buatan Nenek memang yang terbaik! Aku merasa lebih berenergi.")
#         return True

# label splashscreen:
#     scene black
#     pause 1.0
#     show text "The Librarian's Path" with dissolve
#     pause 2.0
#     hide text with dissolve
#     return

image splash = "splash.png"
label splashscreen:
    scene black
    pause 1.0
    show splash with dissolve 
    pause 2.0
    scene black with dissolve
    
    hide splash
    return

# Variabel game
default day = 1
default reputation = 40
default happiness = 50
default energy = 100
default books = 20
default game_over = False
default victory = False
default relationship_sari = 30
default reputation_desa = 0
default cash = 1000000
default player_name = ""
default current_location = "perpustakaan"
default daily_morning_event_done = False
default help_visitors_done_today = False
default organize_books_done_today = False
default education_program_done_today = False
default rest_done_today = False
default talk_grandparents_done_today = False

# Variabel pengunjung
default student1_state = "browsing"
default student2_state = "reading"
default teacher_state = "researching"
default child_state = "storytime"

# Variabel kondisi buku
default fiction_condition = "good"
default science_condition = "good"
default history_condition = "good"

# Screen untuk menampilkan status harian
screen daily_status():
    modal True 
    
    frame:
        xalign 0.5
        yalign 0.5 
        xpadding 30
        ypadding 20
        
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
            
            null height 15
            
            textbutton "Tutup" action Hide("daily_status") xalign 0.5

screen library_actions():
    modal True
    frame:
        xalign 0.5
        yalign 0.5
        xpadding 30
        ypadding 20
        
        vbox:
            spacing 15
            text "Aktivitas di Perpustakaan" size 24
            
            if energy >= 25 and not help_visitors_done_today:
                textbutton "Bantu Pengunjung (-20 Energi)":
                    action [SetVariable("energy", energy - 20), 
                            SetVariable("happiness", min(happiness + 5, 100)),
                            SetVariable("reputation", min(reputation + 2, 100)),
                            Jump("help_visitors")]
            
            if energy >= 20 and not organize_books_done_today:
                textbutton "Atur Buku (-15 Energi)":
                    action [SetVariable("energy", energy - 15),
                            SetVariable("reputation", min(reputation + 3, 100)),
                            Jump("organize_books")]
            
            if energy >= 35 and not education_program_done_today:
                textbutton "Program Edukasi (-30 Energi)":
                    action [SetVariable("energy", energy - 30),
                            SetVariable("happiness", min(happiness + 8, 100)),
                            SetVariable("reputation", min(reputation + 5, 100)),
                            Jump("education_program")]
            
            textbutton "Lihat Laporan Harian":
                action Jump("daily_report")
            
            textbutton "Tutup":
                action Hide("library_actions")

screen home_actions():
    modal True
    frame:
        xalign 0.5
        yalign 0.5
        xpadding 30
        ypadding 20
        
        vbox:
            spacing 15
            text "Aktivitas di Rumah" size 24

            if energy < 50 and not rest_done_today:
                textbutton "Istirahat (+30 Energi)":
                    action [SetVariable("energy", min(energy + 30, 100)),
                            Jump("rest")]
            
            if not talk_grandparents_done_today:
                textbutton "Mengobrol dengan Kakek & Nenek":
                    action Jump("talk_grandparents")

            textbutton "Akhiri Hari dan Tidur":
                action [Hide("home_actions"), Jump("go_to_sleep")]

            textbutton "Tutup":
                action Hide("home_actions")

# ========================
# PROLOGUE - RICH LORE
# ========================
label start:
    scene black
    "Selamat datang di Simulasi Pustakawan Desa Welasari"
    
    python:
        player_name = renpy.input("Masukkan nama karakter utama:", default="", length=20)
        player_name = player_name.strip()
        
        if not player_name:
            player_name = ""
            
        confirmed = False
        while not confirmed:
            confirm = renpy.input(f"Nama kamu adalah {player_name}. Benar? (ya/tidak)", default="ya", length=5)
            if confirm.lower() in ["ya", "y", "yes", "iya", "oke", "ok", "benar", "betul"]:
                confirmed = True
            else:
                player_name = renpy.input("Masukkan nama baru:", default=player_name, length=20)
                player_name = player_name.strip()
                if not player_name:
                    player_name = "Aditya"

    scene bg city with fade
    play music "audio/melancholy.wav" fadeout 1.0
    
    """
    Kota ini tak pernah tidur. 

    Gedung-gedung tinggi menjulang, lampu terang yang tak pernah padam, dan suara klakson yang menjadi lagu pengantar tidur.

    Sudah dua tahun [player_name] bekerja di sini sebagai copywriter di sebuah agensi periklanan. Rutinitas yang tak berujung: rapat pagi, meeting siang, revisi tanpa akhir, lalu pulang larut malam.
    """

    show mc tired at right with dissolve
    player """
    Jangankan tenang, tidur nyenyak saja gabisa.

    Setiap pagi, aku terbangun dengan perasaan hampa. Bukan karena pekerjaanku buruk, tapi... ada sesuatu yang hilang.
    """

    """
    Hingga suatu malam, setelah lembur sampai larut, aku menerima telepon dari Kakek.
    """

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

    kakek "Kakek sudah berusaha merawatnya, tapi semakin hari semakin sulit. Kakek tidak ingin tempat itu ditutup begitu saja."
    kakek "Kakek ingin kamu kembali ke desa, membantu Kakek mengurus perpustakaan itu."

    menu:
        "Tapi... pekerjaanku di sini, Kek. Aku tidak bisa meninggalkannya begitu saja.":
            player "Tapi... pekerjaanku di sini, Kek. Aku tidak bisa meninggalkannya begitu saja."
            kakek "Kakek mengerti, Nak. Kakek hanya... berharap ada yang bisa meneruskan perpustakaan ini"
        
        "Aku akan memikirkannya, Kek.":
            player "Aku akan memikirkannya, Kek. Beri aku waktu."
            kakek "Tentu, Nak. Pikirkanlah baik-baik."

    kakek "Tempat itu bukan hanya tumpukan kertas, [player_name]. Itu adalah peninggalan orang tuamu, kenangan terakhir dari mereka. Kakek hanya tidak ingin kenangan itu memudar."
    kakek "Sudah dulu, ya. Jaga dirimu baik-baik di sana."

    "Telepon ditutup. Aku termangu di kamarku yang sempit, dikelilingi gemerlap lampu kota yang terasa dingin."
    "Kata-kata Kakek terus terngiang, menusuk langsung ke perasaan hampa yang selama ini kurasakan."
    
    player "Peninggalan orang tuaku... Kenangan terakhir dari mereka."
    player "Apa yang sebenarnya aku cari di sini?"
    
    "Malam itu juga, tanpa pikir panjang, aku memesan tiket kereta untuk pulang."

    scene bg train with fade
    
    """
    Aku duduk di dalam kereta, menatap keluar jendela.

    Kereta diisi oleh orang-orang yang sibuk dengan gadget mereka, tapi pikiranku melayang jauh ke masa lalu.

    Perjalanan ini terasa seperti perjalanan kembali ke rumah, meskipun rumah itu sudah lama kutinggalkan.
    """
   
    scene black with fade
    pause 2.0
  
    player "Aku tertidur... Ketika terbangun, waktu sudah menunjukkan pagi dan kereta sudah memasuki stasiun kecil di desa Welasari."
 
    scene bg stasiun with fade
    """
    Ketika aku membuka mata, hari sudah pagi dan pemandangan di luar jendela telah berubah total.

    Perjalanan kereta cukup panjang, tapi sama sekali tidak terasa karena aku menikmatinya.
    """

    show mc idle at left with moveinleft
    player "Akhirnya aku sampai di desa Welasari. stasiun ini masih sama seperti yang kuingat."
    hide mc with dissolve
    show kakek smile at right with moveinright
    kakek "[player_name], kakek ada di sini!"
    hide kakek with dissolve

    """    
    Kakek sudah menunggu di stasiun, aku langusng menghampirinya dan memeluknya erat.
    """

    scene bg village with fade
    play music "audio/nostalgia.mp3" fadeout 1.0

    """
    Desa Welasari masih sama seperti yang kuingat.

    Udara segar, sawah menghijau, dan senyum hangat warga yang saling menyapa.

    Kakek menjemputku di stasiun dengan mobil tuanya. Wajahnya berkeriput tapi matanya masih berbinar.
    """
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
    """
    Perpustakaan kecil itu masih berdiri di ujung jalan setapak.

    Terlihat dari jauh, catnya telah mengelupas, tapi bangunannya masih bagus dan kokoh.
    """

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
    """
    Aroma kertas tua yang khas langsung menyambutku.
    Rak-rak buku yang berdebu dan tumpukan yang tak teratur menjadi pemandangan pertama.
    """

    show kakek serious at right with moveinright
    kakek """
    Seperti yang kamu lihat... Sudah setahun terakhir ini Kakek kesulitan merawatnya sendirian.

    Buku-buku mulai rusak, pengunjung berkurang, dan dana operasional hampir habis.
    
    Tapi Kakek yakin, dengan bantuanmu, kita bisa menghidupkan kembali tempat ini.
    """
    show mc idle at left with moveinleft
    player "Aku mengerti, Kek. Mari kita mulai bekerja."
    
    jump prologue_mission

 
# ========================
# PROLOGUE MISSION
# ========================
label prologue_mission:
    scene bg library 2 with fade
    show kakek at right with dissolve
    
    """
    Kakek memandu keliling perpustakaan. Kondisinya lebih buruk dari yang kubayangkan:
    
    - Rak buku berdebu dan beberapa lapuk

    - Buku-buku berserakan tanpa katalog jelas

    - Beberapa koleksi rusak dimakan rayap
    """

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
            """
            Kakek dengan sabar mengajariku sistem klasifikasi sederhana.
            
            Aku belajar membedakan kategori fiksi, non-fiksi, dan referensi.
            """
        "Saya coba belajar sendiri, Kek.":
            $ energy -= 15
            $ reputation += 2
            """
            Aku mencoba memahami sistem katalog sendiri.
            
            Butuh waktu lebih lama, tapi akhirnya aku menemukan polanya.
            """

    scene bg rak with fade
    """
    Hari pertama berakhir dengan capaian kecil tapi berarti.
    
    Beberapa rak sudah lebih rapi, daftar katalog mulai terbentuk, dan Kakek terlihat lega.
    """
    
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

    kakek "Mengelola perpustakaan ini bukan hanya soal menata buku. Ini tentang membangun kembali jiwanya. Ada beberapa hal yang harus kamu jaga keseimbangannya."

    # Loop menu tutorial, agar pemain bisa bertanya lagi jika mau.
    label tutorial_menu:
        menu:
            "Jelaskan tentang Reputasi dan Kebahagiaan.":
                kakek "Tentu. Mari kita mulai dari yang paling dasar."
                kakek "Reputasi adalah pandangan warga desa terhadap perpustakaan kita. Semakin sering kamu membantu pengunjung atau mengadakan acara, reputasi akan naik."
                kakek "Sebaliknya, jika kamu mengabaikan mereka, reputasi bisa turun. Jika reputasi mencapai nol, desa akan kehilangan kepercayaan dan perpustakaan ini bisa ditutup."
                kakek "Sementara Kebahagiaan adalah cerminan semangatmu sendiri. Kalau kamu merasa senang dan puas dengan pekerjaanmu, kamu akan lebih produktif."
                kakek "Berinteraksi dengan kami, kakek dan nenek, atau melihat hasil kerjamu dihargai akan membuatmu bahagia."
                player "Jadi, aku harus menjaga reputasi perpustakaan dan kebahagiaanku sendiri tetap tinggi."
                kakek "Tepat sekali."
                jump tutorial_menu

            "Untuk apa gunanya Energi?":
                kakek "Energi itu tenagamu. Setiap aktivitas di perpustakaan, seperti membantu pengunjung atau menata buku, akan menguras energimu."
                kakek "Bahkan berjalan dari rumah ke perpustakaan juga butuh energi, walau sedikit."
                kakek "Jika energimu habis, kamu tidak akan bisa melakukan apa-apa lagi di perpustakaan dan harus pulang untuk beristirahat."
                player "Bagaimana cara memulihkannya, Kek?"
                kakek "Istirahat di rumah, atau tidur di malam hari akan memulihkan energimu sepenuhnya untuk keesokan harinya. Ingat, jangan memaksakan diri."
                jump tutorial_menu

            "Bagaimana dengan Hubungan dan Reputasi Desa?":
                kakek "Ah, ini bagian yang menarik. Hubungan dengan Sari akan meningkat seiring interaksimu dengannya. Siapa tahu, persahabatan kalian bisa menjadi lebih dari itu..."
                kakek "Semakin baik hubunganmu, mungkin akan ada kejadian-kejadian spesial yang bisa kalian alami bersama."
                kakek "Reputasi Desa sedikit berbeda dari reputasi perpustakaan. Ini adalah bagaimana desa secara keseluruhan memandangmu sebagai pribadi. Keputusan-keputusan besar yang kamu ambil bisa memengaruhinya."
                player "Jadi ini lebih tentang hubungan sosialku di desa ya, Kek."
                kakek "Benar. Desa ini kecil, hubungan antar warganya sangat berarti."
                jump tutorial_menu
            
            "Lalu, Kas ini untuk apa?":
                kakek "Itu adalah dana operasional perpustakaan kita. Kakek sudah menyiapkan dana awal untukmu."
                kakek "Nantinya, kamu bisa menggunakannya untuk membeli buku baru, memperbaiki fasilitas, atau mungkin mengadakan acara yang lebih besar."
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
    """
    Hari pun terasa cepat berlalu. Aku berbaring di ranjang sembari memikirkan hari esok."
    """
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
# MAIN GAME LOOP
# ========================
label daily_routine:
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
                visitor "Kami ingin menyumbangkan beberapa buku untuk perpustakaan."
                player "Terima kasih banyak atas donasinya!"
                hide donor with dissolve
            elif random_event == 2:
                $ happiness = min(happiness + 10, 100)
                $ reputation = min(reputation + 8, 100)
                show vip at right with dissolve
                visitor "Saya mendengar perpustakaan ini sangat bagus. Saya salah satu penulis dan ingin mengadakan workshop di sini."
                player "Wow! Ini kehormatan bagi kami!"
                hide vip with dissolve
            elif random_event == 3:
                $ energy = max(energy - 20, 0)
                $ reputation = min(reputation + 3, 100)
                show technician at right with dissolve
                visitor "Kami dari tim maintenance datang untuk memeriksa sistem AC."
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

    if reputation <= 30 or happiness <= 0:
        jump game_over
    if reputation >= 100:
        jump victory
    if energy <= 10:
        player "Aku terlalu lelah... sebaiknya aku pulang untuk istirahat."
        jump force_end_day

        # Tampilkan UI berdasarkan lokasi saat ini
    if current_location == "perpustakaan":
        jump library_loop
    elif current_location == "rumah":
        jump home_loop

label library_loop:
    $ current_location = "perpustakaan"
    scene bg library with fade
    
    show screen top_right_icons
    show screen top_left_icons
    show screen top_center_icons

    $ renpy.ui.interact()

label home_loop:
    $ current_location = "rumah"
    scene bg house with fade

    show screen top_right_icons
    show screen top_left_icons
    show screen top_center_icons

    $ renpy.ui.interact()

# Aksi Navigasi (tetap sama, sudah benar)
label go_to_library:
    $ energy -= 5
    player "Oke, aku akan pergi ke perpustakaan. (-5 Energi)"
    $ current_location = "perpustakaan"
    jump daily_routine

label go_home:
    $ energy -= 5 # Biaya energi untuk berjalan
    player "Aku akan pulang ke rumah. (-5 Energi)"
    $ current_location = "rumah"
    jump daily_routine

# Aksi di Perpustakaan
label help_visitors:
    hide screen library_actions
    
    scene bg library with dissolve
    $ visitor_choice = renpy.random.randint(1, 4)
 
    if visitor_choice == 1:
        $ current_visitor = "siswa"
        $ student1_state = "asking_help"

        show student at right with moveinright

        visitor "Maaf, bisakah Anda membantu saya menemukan buku tentang fisika?"

        menu:
            "Tentu, mari kita cari bersama.":
                player "Tentu, mari kita cari bersama. Bagian sains ada di sebelah sini."

                scene bg_library_physics with dissolve
                show mc idle at left with moveinleft
                player "Nah, ini dia rak untuk buku-buku fisika. Kamu cari tentang topik spesifik?"
                show student at right with moveinright
                visitor "Tentang mekanika kuantum, kak. Wah, koleksinya lumayan lengkap juga, ya!"

                $ student1_state = "satisfied"
                $ happiness = min(happiness + 3, 100)
                $ reputation = min(reputation + 2, 100)

                visitor "Ini buku yang kucari! Terima kasih banyak, kak! Anda sangat membantu."

            "Saya sibuk sekarang, coba tanya yang lain.":
                player "Saya sibuk sekarang, coba tanya yang lain."
                $ student1_state = "leaving"
                $ happiness = max(happiness - 3, 0)
                $ reputation = max(reputation - 2, 0)
                visitor "Oh... baiklah."

        hide student at right with moveoutright
        
    elif visitor_choice == 2:
        $ current_visitor = "guru"
        $ teacher_state = "asking_help"
        
        show teacher at right with moveinright
        
        visitor "Saya sedang meneliti untuk makalah, apakah Anda punya referensi tentang sejarah lokal?"
        
        menu:
            "Ya, kami punya beberapa koleksi bagus di rak sejarah.":
                player "Ya, kami punya beberapa koleksi bagus di rak sejarah."
                
                scene bg_library_history with dissolve
                
                show mc idle at left with moveinleft
                player "Ini dia, rak sejarah lokal. Ada beberapa buku yang mungkin Anda butuhkan."
                
                show teacher at right with moveinright
                visitor "Wah, ini sangat membantu! Saya akan mencatat beberapa judul yang menarik."

                $ teacher_state = "researching"
                $ happiness = min(happiness + 3, 100)
                $ reputation = min(reputation + 2, 100)
                visitor "Sempurna! Ini sangat membantu penelitian saya."
                
            "Maaf, koleksi sejarah lokal kami terbatas.":
                player "Maaf, koleksi sejarah lokal kami terbatas."
                $ teacher_state = "leaving"
                $ happiness = max(happiness - 3, 0)
                visitor "Yah, sayang sekali. Mungkin lain kali."
        
        hide teacher at left with moveoutleft
        
    elif visitor_choice == 3:
        $ current_visitor = "anak kecil"
        $ child_state = "asking_questions"
        
        show child at right with moveinright
        
        visitor "Aku suka dinosaurus! Punya buku dinosaurus yang gambarnya bagus?"
        
        menu:
            "Tentu! Mari kita ke bagian buku anak-anak.":
                player "Tentu! Mari kita ke bagian buku anak-anak."

                scene bg_library_child with dissolve
                show mc idle at left with moveinleft
                player "Ini dia, rak buku anak-anak. Bagian dinosaurus ada di sini."
                show child at right with moveinright         
                visitor "Wah, gambarnya keren! Aku suka dinosaurus T-Rex!"

                $ child_state = "happy"
                $ happiness = min(happiness + 3, 100)
                $ reputation = min(reputation + 2, 100)
                visitor "Yay! Terima kasih kak!"
                
            "Mungkin lain kali ya, sekarang sedang sibuk.":
                player "Mungkin lain kali ya, sekarang sedang sibuk."
                $ child_state = "tired"
                $ happiness = max(happiness - 5, 0)
                $ reputation = max(reputation - 2, 0)
                visitor "Awww... aku kecewa."
        
        hide child at right with moveoutright
        
    else:
        $ current_visitor = "siswa lain"
        $ student2_state = "asking_help"
        
        show student2 at right with moveinright
        
        visitor "Saya kesulitan mencari buku referensi untuk tugas matematika saya."
        
        menu:
            "Saya akan tunjukkan di mana bagian bukunya.":
                player "Saya akan tunjukkan di mana bagian bukunya."

                scene bg_library_math with dissolve

                show mc idle at left with moveinleft
                player "Ini dia, rak buku matematika. Semua buku referensi matematika ada di sini."
                show student2 at right with moveinright
                visitor "Wah, terima kasih! Aku tidak tahu harus mulai dari mana."

                $ student2_state = "studying"
                $ happiness = min(happiness + 3, 100)
                $ reputation = min(reputation + 2, 100)
                visitor "Terima kasih! Sekarang saya bisa mengerjakan tugas."
                
            "Coba cari di katalog komputer dulu.":
                player "Coba cari di katalog komputer dulu."
                $ student2_state = "Browse"
                $ happiness = max(happiness - 3, 0)
                $ reputation = max(reputation - 2, 0)
                visitor "Oh, baiklah. Saya akan coba."
        
        hide student2 at right with moveoutright
    
    $ help_visitors_done_today = True
    jump end_action

label organize_books:
    hide screen library_actions
    
    scene bg library shelves with dissolve
    
    player "Aku harus merapikan beberapa buku hari ini."
    
    menu:
        "Buku Fiksi":
            if fiction_condition == "fair":
                player "Beberapa buku fiksi mulai rusak. Aku akan memperbaikinya."
                $ fiction_condition = "good"
                $ reputation = min(reputation + 2, 100)
            else:
                player "Buku fiksi sudah dalam kondisi baik."
                
        "Buku Sains":
            if science_condition == "fair":
                player "Beberapa buku sains perlu diperbaiki. Aku akan merawatnya."
                $ science_condition = "good"
                $ reputation = min(reputation + 2, 100)
            else:
                player "Buku sains masih dalam kondisi bagus."
                
        "Buku Sejarah":
            if history_condition == "fair":
                player "Buku sejarah perlu sedikit perhatian. Aku akan merapikannya."
                $ history_condition = "good"
                $ reputation = min(reputation + 2, 100)
            else:
                player "Buku sejarah masih terawat dengan baik."
    
    scene bg rak with dissolve
    show mc idle at left with moveinleft
    player "Aku sudah merapikan buku-buku hari ini. Perpustakaan terlihat lebih rapi sekarang."
    $ organize_books_done_today = True
    jump end_action

label education_program:
    hide screen library_actions
    
    scene bg library event with dissolve
    
    player "Aku akan mengadakan program edukasi hari ini."
    
    menu:
        "Literasi Digital":
            player "Mengajarkan literasi digital kepada pengunjung."
            $ reputation = min(reputation + 5, 100)
            with dissolve
            visitor "Workshop ini sangat bermanfaat!"
            with dissolve
            
        "Story Time untuk Anak":
            player "Membacakan cerita untuk anak-anak."
            $ happiness = min(happiness + 7, 100)
            with dissolve
            visitor "Ceritanya seru! Aku mau datang lagi besok!"
            with dissolve
            
        "Diskusi Buku":
            player "Memimpin diskusi buku untuk remaja dan dewasa."
            $ reputation = min(reputation + 3, 100)
            $ happiness = min(happiness + 5, 100)
            with dissolve
            visitor "Diskusi hari ini sangat menarik!"
            with dissolve
    
    $ education_program_done_today = True
    jump end_action

label daily_report:
    hide screen library_actions
    
    scene bg library desk with dissolve
    
    show screen daily_status
    
    player "Ini laporan harian perpustakaan:"
    
    # Laporan kondisi buku
    "Kondisi Buku:"
    "- Fiksi: [fiction_condition]"
    "- Sains: [science_condition]"
    "- Sejarah: [history_condition]"
    
    # Laporan pengunjung
    "Status Pengunjung:"
    "- Siswa 1: [student1_state]"
    "- Siswa 2: [student2_state]"
    "- Guru: [teacher_state]"
    "- Anak: [child_state]"
    
    "Tekan tombol apapun untuk melanjutkan..."
    pause
    
    jump end_action

# Aksi di Rumah
label rest:
    hide screen home_actions
    scene bg house with dissolve
    player "Aku butuh istirahat sebentar..."
    "Anda beristirahat di rumah dan memulihkan 30 energi."
    jump end_action

label talk_grandparents:
    hide screen home_actions
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
    jump end_action

label end_action:
    # Kembali ke loop utama setelah aksi selesai
    jump daily_routine

label force_end_day:
    scene bg library evening with fade
    player "Aku sangat lelah... Aku tidak bisa melakukan apa-apa lagi. Sebaiknya aku langsung pulang dan tidur."
    pause 2.0
    jump next_day

label next_day:
    $ day += 1
    $ energy = 100
    $ daily_morning_event_done = False
    $ help_visitors_done_today = False
    $ organize_books_done_today = False
    $ education_program_done_today = False
    $ rest_done_today = False
    $ talk_grandparents_done_today = False
    
    # Degradasi alami
    $ happiness = max(happiness - renpy.random.randint(2, 5), 0)
    $ reputation = max(reputation - renpy.random.randint(1, 3), 0)
    
    # Degradasi kondisi buku
    $ book_degrade_chance = renpy.random.random()
    if book_degrade_chance > 0.7:
        if fiction_condition == "good":
            $ fiction_condition = "fair"
        elif fiction_condition == "fair":
            $ fiction_condition = "poor"
    
    $ book_degrade_chance = renpy.random.random()
    if book_degrade_chance > 0.7:
        if science_condition == "good":
            $ science_condition = "fair"
        elif science_condition == "fair":
            $ science_condition = "poor"
    
    $ book_degrade_chance = renpy.random.random()
    if book_degrade_chance > 0.7:
        if history_condition == "good":
            $ history_condition = "fair"
        elif history_condition == "fair":
            $ history_condition = "poor"
    
    scene bg library morning with fade
    $ current_location = "perpustakaan"
    
    "Pagi telah tiba, hari baru dimulai di Desa Welasari."
    
    jump daily_routine

# ========================
# EPILOGUE - GOOD ENDING
# ========================
label victory:
    $ victory = True
    scene bg library celebration with fade
    play music "audio/victory.mp3" fadeout 1.0
    
    """
    Setelah sepuluh hari bekerja keras, perpustakaan kecil itu kini bersinar kembali.
    
    Warga desa berdatangan, anak-anak riang membaca di pojok khusus, dan rak-rak buku terisi penuh dengan koleksi terawat.
    """

    show pak_amin at right with dissolve
    pak_amin """
    Atas nama Desa Welasari, saya menyatakan perpustakaan ini sebagai pusat literasi terbaik tahun ini!
    
    Kami mengalokasikan dana tambahan Rp500.000 untuk pembelian buku baru dan renovasi ruang baca.
    """

    menu:
        "Terima kasih, Pak Kepala Desa. Ini semua berkat semangat warga.":
            $ reputation_desa += 10
        "Saya akan gunakan dana ini sebaik-baiknya untuk generasi penerus.":
            $ reputation_desa += 10
            $ happiness += 5

    if relationship_sari >= 80:
        scene bg library garden night with fade
        show sari happy at center with dissolve
        """
        Di teras perpustakaan yang diterangi lentera, Sari dan aku duduk berdua menikmati keheningan malam.
        
        Suara jangkrik dan gemericik air mancur kecil menjadi musik pengantar percakapan kami.
        """

        sari """
        [player_name]... selama ini aku menunggu kamu pulang.
        
        Aku ingin menjalani hari-hari di desa ini bersamamu.
        """

        menu:
            "Aku pun merasakan hal yang sama, Sari. Aku ingin tinggal di sini, menata perpustakaan kita berdua.":
                $ relationship_sari += 10
                show sari blush with dissolve
                sari "Kamu mau jadi pustakawan hidupku?"
                """
                Senyumnya merekah seperti bulan purnama yang menerangi kegelapan.
                
                Di antara rak-rak kayu dan aroma kertas kuno, kami menemukan bahagia yang selama ini kami cari.
                """
            "Aku senang bisa kembali dan bekerja sama denganmu.":
                $ relationship_sari += 5
                sari "Aku juga senang, [player_name]. Mari kita jaga perpustakaan ini bersama."

    scene bg library sunset with fade
    """
    EPILOGUE:
    
    Perpustakaan Welasari kini menjadi kebanggaan desa.
    
    Setiap hari ramai dikunjungi warga, dari anak-anak yang haus dongeng hingga petani yang mencari ilmu baru.
    
    Aku dan Sari mengelola tempat ini bersama, dengan Kakek dan Nenek yang sesekali datang membawa kue dan cerita-cerita lama.
    
    Di antara tumpukan buku dan senyum warga, aku akhirnya menemukan kedamaian yang selama ini kucari.
    
    Inilah rumahku. Inilah kebahagiaan sejati.
    """

    show screen good_ending_screen with dissolve
    pause 5.0
    hide screen good_ending_screen with dissolve

    return

# ========================
# GAME OVER
# ========================
label game_over:
    $ game_over = True
    scene bg library night with fade
    play music "audio/sad.mp3" fadeout 1.0
    
    if reputation <= 0:
        """
        Reputasi perpustakaan merosot tajam.
        
        Warga kehilangan kepercayaan, pengunjung berhenti datang, dan akhirnya dewan desa memutuskan untuk menutup tempat ini.
        """
    else:
        """
        Kebahagiaanku terkikis hari demi hari.
        
        Tekanan dan kelelahan membuatku memutuskan untuk berhenti dan kembali ke kota.
        """

    show kakek sad at center with dissolve
    kakek """
    Mungkin ini bukan jalan yang tepat untukmu, Nak.
    
    Tapi Kakek tetap bangga padamu.
    """

    menu:
        "Main lagi":
            jump restart_game
        "Keluar":
            return

label restart_game:
    $ day = 1
    $ reputation = 50
    $ happiness = 50
    $ energy = 100
    $ books = 20
    $ game_over = False
    $ victory = False
    $ relationship_sari = 30
    $ reputation_desa = 0
    $ cash = 1000000
    
    $ student1_state = "Browse"
    $ student2_state = "reading"
    $ teacher_state = "researching"
    $ child_state = "storytime"
    
    $ fiction_condition = "good"
    $ science_condition = "good"
    $ history_condition = "good"
    $ current_location = "perpustakaan"
    
    jump start

# Screen UI Icons
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
                idle Transform("images/ui/icon_home_action.png", zoom=0.2) # Ganti dengan ikon yang sesuai
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
        # Posisikan di tengah layar
        align (0.5, 0.5)

        background "#6d4c41" 
        xpadding 60
        ypadding 40

        vbox:
            spacing 15 
            text "GOOD ENDING" size 42 color "#FFFFFF" xalign 0.5
            text "Perpustakaan Berjaya\n& Cinta Bersemi" size 26 color "#FFFFFF" xalign 0.5

# Label perantara untuk transisi sebelum tidur
label go_to_sleep:
    scene bg kamar with dissolve
    player "Baiklah, waktunya istirahat untuk hari esok."
    pause 2.0
    jump next_day




