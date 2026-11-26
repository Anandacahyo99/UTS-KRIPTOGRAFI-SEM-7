import math

# ==========================================
# BAGIAN A: AFFINE CIPHER & EXTENDED EUCLID
# ==========================================

def extended_gcd(a, b):
    """Algoritma Euclid yang diperluas untuk mencari FPB dan koefisien Bezout."""
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y

def mod_inverse(a, m=26):
    """Menghitung invers modulo a^-1 mod m secara manual tanpa pow()."""
    gcd, x, _ = extended_gcd(a, m)
    if gcd != 1:
        raise ValueError(f"Kunci a={a} tidak valid! FPB({a}, {m}) = {gcd} (harus 1 / koprima dengan {m}).")
    return (x % m + m) % m

def affine_enkripsi(plain, a, b):
    """Enkripsi teks menggunakan Affine Cipher: E(x) = (ax + b) mod 26."""
    mod_inverse(a, 26)
    hasil = []
    for char in plain.upper():
        if char.isalpha():
            x = ord(char) - ord('A')
            enkrip = (a * x + b) % 26
            hasil.append(chr(enkrip + ord('A')))
        else:
            hasil.append(char)
    return "".join(hasil)

def affine_dekripsi(cipher, a, b):
    """Dekripsi teks menggunakan Affine Cipher: D(y) = a^-1 * (y - b) mod 26."""
    a_inv = mod_inverse(a, 26)
    hasil = []
    for char in cipher.upper():
        if char.isalpha():
            y = ord(char) - ord('A')
            dekrip = (a_inv * (y - b)) % 26
            hasil.append(chr(dekrip + ord('A')))
        else:
            hasil.append(char)
    return "".join(hasil)


# ==========================================
# BAGIAN B: BRUTE FORCE AFFINE CIPHER
# ==========================================

def brute_force_affine(cipher, kata):
    """Mencoba semua kombinasi kunci (a, b) dan mencari kandidat yang memuat kata tertentu."""
    kunci_a_valid = [1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25]
    kata_target = kata.upper()
    kandidat = []

    print(f"Target Kata : '{kata_target}'")
    print(f"Ciphertext  : {cipher}\n")
    
    for a in kunci_a_valid:
        for b in range(26):
            teks_dekripsi = affine_dekripsi(cipher, a, b)
            if kata_target in teks_dekripsi:
                kandidat.append((a, b, teks_dekripsi))
                print(f"  [DITEMUKAN] Kunci (a={a}, b={b}) -> Plaintext: {teks_dekripsi}")
    
    if not kandidat:
        print("  Tidak ada kandidat yang cocok ditemukan.")
    return kandidat


# ==========================================
# BAGIAN C: CIPHER TRANSPOSISI
# ==========================================

def columnar_enkripsi(plain, kunci):
    """Enkripsi Columnar Transposition dengan jumlah kolom fleksibel."""
    teks = plain.replace(" ", "").upper()
    kunci = kunci.upper()
    kolom = len(kunci)
    baris = math.ceil(len(teks) / kolom)
    
    panjang_total = baris * kolom
    teks_padded = teks.ljust(panjang_total, 'X')
    matriks = [list(teks_padded[i:i + kolom]) for i in range(0, panjang_total, kolom)]
    urutan_kunci = sorted(range(kolom), key=lambda k: kunci[k])
    
    ciphertext = []
    for idx_kolom in urutan_kunci:
        for r in range(baris):
            ciphertext.append(matriks[r][idx_kolom])
            
    return "".join(ciphertext)

def columnar_dekripsi(cipher, kunci):
    """Dekripsi Columnar Transposition."""
    teks = cipher.replace(" ", "").upper()
    kunci = kunci.upper()
    kolom = len(kunci)
    baris = math.ceil(len(teks) / kolom)
    
    matriks = [[''] * kolom for _ in range(baris)]
    urutan_kunci = sorted(range(kolom), key=lambda k: kunci[k])
    
    idx_teks = 0
    for idx_kolom in urutan_kunci:
        for r in range(baris):
            if idx_teks < len(teks):
                matriks[r][idx_kolom] = teks[idx_teks]
                idx_teks += 1
                
    plaintext = []
    for r in range(baris):
        for c in range(kolom):
            plaintext.append(matriks[r][c])
            
    return "".join(plaintext)

def rail_fence_enkripsi(plain, rel):
    """Enkripsi Rail Fence Cipher dengan jumlah rel fleksibel."""
    if rel <= 1:
        return plain
    
    teks = plain.replace(" ", "").upper()
    pagar = [[] for _ in range(rel)]
    baris = 0
    arah = 1
    
    for char in teks:
        pagar[baris].append(char)
        if baris == 0:
            arah = 1
        elif baris == rel - 1:
            arah = -1
        baris += arah
        
    return "".join("".join(r) for r in pagar)

def rail_fence_dekripsi(cipher, rel):
    """Dekripsi Rail Fence Cipher."""
    if rel <= 1:
        return cipher
        
    teks = cipher.replace(" ", "").upper()
    panjang = len(teks)
    pagar = [['\n' for _ in range(panjang)] for _ in range(rel)]
    
    baris = 0
    arah = 1
    for i in range(panjang):
        pagar[baris][i] = '*'
        if baris == 0:
            arah = 1
        elif baris == rel - 1:
            arah = -1
        baris += arah
        
    idx = 0
    for r in range(rel):
        for c in range(panjang):
            if pagar[r][c] == '*' and idx < panjang:
                pagar[r][c] = teks[idx]
                idx += 1
                
    hasil = []
    baris = 0
    arah = 1
    for i in range(panjang):
        hasil.append(pagar[baris][i])
        if baris == 0:
            arah = 1
        elif baris == rel - 1:
            arah = -1
        baris += arah
        
    return "".join(hasil)


# ==========================================
# BAGIAN D & E: MODUL PENGUJIAN TERPISAH
# ==========================================

def uji_soal_1_2_3():
    """Blok Pengujian 1: Soal 1, Soal 2, dan Soal 3."""
    print("\n" + "=" * 60)
    print("BAGIAN 1: PENGUJIAN SOAL 1, SOAL 2, DAN SOAL 3")
    print("=" * 60)

    # Uji Validasi Kunci Affine
    print("\n[Validasi Kunci Affine]")
    try:
        affine_enkripsi("TES", a=4, b=5)
    except ValueError as e:
        print(f"  Status : BERHASIL MENOLAK KUNCI -> {e}")

    # Soal 1: Affine Cipher (Enkripsi & Dekripsi)
    print("\n[Soal 1 - Affine Cipher]")
    plain_s1 = "KRIPTOGRAFI"
    a_s1, b_s1 = 7, 10
    cipher_s1 = affine_enkripsi(plain_s1, a_s1, b_s1)
    dekrip_s1 = affine_dekripsi(cipher_s1, a_s1, b_s1)
    print(f"  Plaintext      : {plain_s1}")
    print(f"  Kunci          : a={a_s1}, b={b_s1}")
    print(f"  Hasil Enkripsi : {cipher_s1}")
    print(f"  Hasil Dekripsi : {dekrip_s1}")

    print("\n[Soal 2 - DESKRIPSI Affine Cipher]")
    cipher_uji = "EVWUNINLWZIP"
    expected_uji = "UNISBABLITAR"
    hasil_uji = affine_dekripsi(cipher_uji, a=5, b=8)
    print(f"     Input Cipher : {cipher_uji} (a=5, b=8)")
    print(f"     Hasil Dekrip : {hasil_uji}")
    print(f"     Status       : {'LULUS' if hasil_uji == expected_uji else 'GAGAL'}")

    # Soal 3: Columnar Transposition Cipher
    print("\n[Soal 3 - Columnar Transposition Cipher]")
    plain_s3 = "TEKNIKINFORMATIKAUNISBA"
    kunci_kolom = "KUNCI"
    c_col = columnar_enkripsi(plain_s3, kunci_kolom)
    d_col = columnar_dekripsi(c_col, kunci_kolom)
    print(f"  Plaintext      : {plain_s3}")
    print(f"  Kata Kunci     : '{kunci_kolom}'")
    print(f"  Hasil Enkripsi : {c_col}")
    print(f"  Hasil Dekripsi : {d_col}")


def uji_brute_force():
    """Blok Pengujian 2: Khusus Brute Force Affine Cipher."""
    print("\n" + "=" * 60)
    print("BAGIAN 2: PENGUJIAN BRUTE FORCE AFFINE CIPHER")
    print("=" * 60 + "\n")
    
    # Ganti variabel 'cipher_target' dengan ciphertext asli dari soal jika berbeda
    contoh_plain = "TEKNIKINFORMATIKAUNISBA"
    cipher_target = affine_enkripsi(contoh_plain, a=7, b=3)
    
    brute_force_affine(cipher_target, "INFORMATIKA")



def uji_data_pribadi():
    """Blok Pengujian 3: Uji Columnar Transposition & Rail Fence pada Data Pribadi (Fleksibel)."""
    print("\n" + "=" * 60)
    print("BAGIAN 3: PENGUJIAN DATA PRIBADI (TRANSPOSISI FLEKSIBEL)")
    print("=" * 60)

    # Silakan ganti dengan Nama Lengkap (tanpa spasi) dan NIM Anda
    nama_pribadi = "ANANDACAHYOKARTIKO"
    DESA = "DESATULISKRIYO"

    # 1. Pengujian Columnar Transposition dengan variasi panjang kunci (jumlah kolom fleksibel)
    print("\n[Uji 1: Columnar Transposition pada Nama (Kolom Fleksibel)]")
    daftar_kunci_kolom = ["KEY", "UNISBA"]  # Uji dengan 3 kolom dan 6 kolom
    
    for kunci in daftar_kunci_kolom:
        c_col = columnar_enkripsi(nama_pribadi, kunci)
        d_col = columnar_dekripsi(c_col, kunci)
        # Hapus karakter padding 'X' di akhir saat mencocokkan dengan nama asli
        d_col_bersih = d_col.rstrip('X')
        
        print(f"  -> Kunci '{kunci}' ({len(kunci)} Kolom):")
        print(f"     Data Asli      : {nama_pribadi}")
        print(f"     Hasil Enkripsi : {c_col}")
        print(f"     Hasil Dekripsi : {d_col} (Tanpa padding: {d_col_bersih})")
        print(f"     Verifikasi     : {'COCOK (100% Sama)' if nama_pribadi == d_col_bersih else 'TIDAK COCOK'}\n")

    # 2. Pengujian Rail Fence Cipher dengan variasi jumlah rel fleksibel
    print("[Uji 2: Rail Fence Cipher pada NIM & Nama (Rel Fleksibel)]")
    daftar_rel = [2, 3, 4]  # Uji dengan 2 rel, 3 rel, dan 4 rel
    
    for rel in daftar_rel:
        c_rf = rail_fence_enkripsi(DESA, rel)
        d_rf = rail_fence_dekripsi(c_rf, rel)
        
        print(f"  -> Jumlah Rel = {rel}:")
        print(f"     Data Asli      : {DESA}")
        print(f"     Hasil Enkripsi : {c_rf}")
        print(f"     Hasil Dekripsi : {d_rf}")
        print(f"     Verifikasi     : {'COCOK (100% Sama)' if DESA == d_rf else 'TIDAK COCOK'}\n")



#PANGGIL FUNGSSI BLOK DIATAS 
def main():
    print("*" * 60)
    print("         PROGRAM UTS KRIPTOGRAFI - PYTHON")
    print("*" * 60)

    # Memanggil ketiga blok pengujian secara berurutan dan terpisah
    uji_soal_1_2_3()
    uji_brute_force()
    uji_data_pribadi()

    print("\n" + "*" * 60)
    print("                 SELURUH PENGUJIAN SELESAI")
    print("*" * 60)

if __name__ == "__main__":
    main()
