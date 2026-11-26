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
    """Menghitung invers modulo a^-1 mod m secara manual."""
    gcd, x, _ = extended_gcd(a, m)
    if gcd != 1:
        raise ValueError(f"Kunci a={a} tidak valid! FPB({a}, {m}) = {gcd} (harus 1 / koprima dengan {m}).")
    return (x % m + m) % m

def affine_enkripsi(plain, a, b):
    """Enkripsi teks menggunakan Affine Cipher: E(x) = (ax + b) mod 26."""
    # Validasi kunci 'a' terlebih dahulu
    mod_inverse(a, 26)
    
    hasil = []
    for char in plain.upper():
        if char.isalpha():
            x = ord(char) - ord('A')
            enkrip = (a * x + b) % 26
            hasil.append(chr(enkrip + ord('A')))
        else:
            # Pertahankan spasi atau tanda baca jika ada
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

    print(f"Mencari kata '{kata_target}' pada ciphertext: {cipher}")
    for a in kunci_a_valid:
        for b in range(26):
            teks_dekripsi = affine_dekripsi(cipher, a, b)
            if kata_target in teks_dekripsi:
                kandidat.append((a, b, teks_dekripsi))
                print(f"[DITEMUKAN] Kunci (a={a}, b={b}) -> Plaintext: {teks_dekripsi}")
    
    if not kandidat:
        print("Tidak ada kandidat yang cocok ditemukan.")
    return kandidat


# ==========================================
# BAGIAN C: CIPHER TRANSPOSISI
# ==========================================

# 1. Columnar Transposition Cipher
def columnar_enkripsi(plain, kunci):
    """Enkripsi Columnar Transposition dengan jumlah kolom fleksibel sesuai panjang kunci."""
    teks = plain.replace(" ", "").upper()
    kunci = kunci.upper()
    kolom = len(kunci)
    baris = math.ceil(len(teks) / kolom)
    
    # Tambahkan padding 'X' jika panjang teks tidak habis dibagi jumlah kolom
    panjang_total = baris * kolom
    teks_padded = teks.ljust(panjang_total, 'X')
    
    # Susun ke dalam matriks baris x kolom
    matriks = [list(teks_padded[i:i + kolom]) for i in range(0, panjang_total, kolom)]
    
    # Urutan pembacaan kolom berdasarkan urutan abjad kunci
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

# 2. Rail Fence Cipher
def rail_fence_enkripsi(plain, rel):
    """Enkripsi Rail Fence Cipher dengan jumlah rel fleksibel."""
    if rel <= 1:
        return plain
    
    teks = plain.replace(" ", "").upper()
    pagar = [[] for _ in range(rel)]
    baris = 0
    arah = 1  # 1 = turun, -1 = naik
    
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
    
    # Tandai pola zig-zag
    baris = 0
    arah = 1
    for i in range(panjang):
        pagar[baris][i] = '*'
        if baris == 0:
            arah = 1
        elif baris == rel - 1:
            arah = -1
        baris += arah
        
    # Isi tanda '*' dengan huruf dari ciphertext
    idx = 0
    for r in range(rel):
        for c in range(panjang):
            if pagar[r][c] == '*' and idx < panjang:
                pagar[r][c] = teks[idx]
                idx += 1
                
    # Baca secara zig-zag
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
# BAGIAN D & E: FUNGSI MAIN & PENGUJIAN
# ==========================================

def main():
    print("=" * 55)
    print("PROGRAM UJIAN TENGAH SEMESTER - KRIPTOGRAFI")
    print("=" * 55)

    # 1. Uji Validasi Kunci Affine (Menolak kunci tidak valid)
    print("\n[UJI VALIDASI KUNCI AFFINE]")
    try:
        affine_enkripsi("TES", a=4, b=5)
    except ValueError as e:
        print(f"Berhasil menangkap error: {e}")

    # 2. Simulasi Soal 1 (Affine Cipher)
    print("\n[SOAL 1 - AFFINE CIPHER]")
    # Silakan sesuaikan plaintext dan kunci dengan soal UTS Anda
    plain_s1 = "KRIPTOGRAFI"
    a_s1, b_s1 = 5, 8
    cipher_s1 = affine_enkripsi(plain_s1, a_s1, b_s1)
    dekrip_s1 = affine_dekripsi(cipher_s1, a_s1, b_s1)
    print(f"Plaintext  : {plain_s1}")
    print(f"Kunci      : a={a_s1}, b={b_s1}")
    print(f"Ciphertext : {cipher_s1}")
    print(f"Dekripsi   : {dekrip_s1}")

    # 3. Simulasi Soal 2 (Cipher Transposisi)
    print("\n[SOAL 2 - CIPHER TRANSPOSISI]")
    # Silakan sesuaikan plaintext dan kunci/rel dengan soal UTS Anda
    plain_s2 = "KEAMANANDATA"
    kunci_kolom = "KUNCI"
    rel_rf = 3
    
    c_col = columnar_enkripsi(plain_s2, kunci_kolom)
    d_col = columnar_dekripsi(c_col, kunci_kolom)
    print(f"Columnar (Kunci='{kunci_kolom}')")
    print(f"  Enkripsi : {c_col}")
    print(f"  Dekripsi : {d_col}")
    
    c_rf = rail_fence_enkripsi(plain_s2, rel_rf)
    d_rf = rail_fence_dekripsi(c_rf, rel_rf)
    print(f"Rail Fence (Rel={rel_rf})")
    print(f"  Enkripsi : {c_rf}")
    print(f"  Dekripsi : {d_rf}")

    # 4. Simulasi Soal 3 & Bagian B (Brute Force Affine)
    print("\n[SOAL 3 - BRUTE FORCE AFFINE CIPHER]")
    # Contoh ciphertext yang memuat kata INFORMATIKA (misal dienkripsi dengan a=7, b=3)
    # Ganti variabel 'cipher_s3' di bawah ini dengan ciphertext asli dari Soal 3 UTS Anda!
    contoh_plain_s3 = "TEKNIKINFORMATIKA"
    cipher_s3 = affine_enkripsi(contoh_plain_s3, a=7, b=3) 
    brute_force_affine(cipher_s3, "INFORMATIKA")

    # 5. Bagian E: Uji dengan Data Pribadi
    print("\n[BAGIAN E - UJI DATA PRIBADI]")
    # Silakan ganti dengan Nama Lengkap & NIM Anda
    nama_pribadi = "BUDISANTOSO"
    nim_pribadi = "20241010"
    
    # Uji Affine pada Nama (a=3, b=7)
    c_nama = affine_enkripsi(nama_pribadi, 3, 7)
    d_nama = affine_dekripsi(c_nama, 3, 7)
    print(f"Data Pribadi (Nama) : {nama_pribadi}")
    print(f"Affine Enkripsi     : {c_nama}")
    print(f"Affine Dekripsi     : {d_nama} -> Match: {nama_pribadi == d_nama}")

    # Uji Rail Fence pada NIM (rel=3)
    c_nim = rail_fence_enkripsi(nim_pribadi, 3)
    d_nim = rail_fence_dekripsi(c_nim, 3)
    print(f"\nData Pribadi (NIM)  : {nim_pribadi}")
    print(f"Rail Fence Enkripsi : {c_nim}")
    print(f"Rail Fence Dekripsi : {d_nim} -> Match: {nim_pribadi == d_nim}")

if __name__ == "__main__":
    main()
