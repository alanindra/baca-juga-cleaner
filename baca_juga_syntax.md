# Syntax of `"baca juga"` constituents

These syntactic constructions are derived from empirical observations of how `"baca juga"` is typically used in Indonesian news articles. Full analysis is available in the [analysis notebook](https://github.com/alanindra/baca-juga-cleaner/blob/main/analysis.ipynb).

## 1. Syntax classification

Each syntax rule follows the format **[Class][Pattern]**, where:

- **Class**:
  - **1**: Short constituents (≤ 10 words)
  - **2**: Medium constituents (11–35 words)
  - **3**: Long constituents (> 35 words)

- **Pattern**:
  - **A**: Starts with `"baca juga"`, contains capitalized clusters, ends with `"!"`
  - **B**: Ends with `"!"`, and either starts with `"baca juga"` or contains capitalized words
  - **C**: Starts with `"baca juga"` only
  - **D**: Contains capitalized words only
  - **E**: Ends with `"!"` only

## 2. General principles

- Constituents are extracted from up to **three sentence tokens** immediately following `"baca juga"`.
- Most are **short** and structured as promotional or imperative headlines.
- Constituents matching **1A**—those starting with `"baca juga"`, containing capitalized clusters, and ending with `"!"`—are the most consistently irrelevant.

## 3. Irrelevant constituent criteria

### 3.1 Short constituents (Class 1)
These are flagged as irrelevant when matching:

- **1A**: Starts with `"baca juga"`, contains capitalized words, ends with `"!"`
- **1B**: Ends with `"!"`, and either starts with `"baca juga"` or contains capitalized words
- **1C**: Starts with `"baca juga"` only
- **1D**: Contains capitalized words only
- **1E**: Ends with `"!"` only

### 3.2 Medium constituents (Class 2)
Medium-length segments are considered irrelevant under:

- **2A**: Starts with `"baca juga"`, has capitalized words, ends with `"!"`
- **2B**: Ends with `"!"`, and either starts with `"baca juga"` or contains capitalized words
- **2C**: Starts with `"baca juga"`
- **2D**: Contains capitalized word clusters

### 3.3 Long constituents (Class 3)
Long segments are rarely promotional, but these are filtered:

- **3C**: Starts with `"baca juga"`
- **3D**: Contains capitalized clusters and lexical clues (e.g., `"cek"`, `"klaim"`, etc.)

## 4. Relevant and edge cases

- Constituents under **2E** and **4C** are typically relevant and preserved.
- Criteria such as **3A**, **3B**, **3E**, **4A**, **4B** occur infrequently and are subject to manual review.
- A fallback rule scans for unmatched `"baca juga"` strings to catch edge cases.

## 5. Constituents with partially relevant content

Certain constituents, particularly those classified under **2B**, **2C**, and **3C**, may contain fragments of relevant information. These undergo additional transformation steps:

- **If the constituent contains more than 15 words and includes capitalized word clusters**, it will be truncated after the **penultimate capitalized cluster**.

  **Example**  
  - **Raw**:  
    *Baca juga: IHSG Terpuruk, Sri Mulyani Sindir Tata Kelola BUMN Sederet saham top gainers di antaranya adalah PT Lion Metal Works Tbk (LION), PT Pradiksi Gunatama Tbk (PGUN), dan PT Daaz Bara Lestari Tbk (DAAZ).*  
  - **Cleaned**:  
    *Baca juga: IHSG Terpuruk, Sri Mulyani Sindir Tata Kelola BUMN*

- **If the constituent contains more than 15 words without capitalized word clusters**, it will either be **truncated to the first 18 words** or **removed entirely** based on preference or agreed rules.

## 6. Constituent examples

This section illustrates example constituents classified by syntax criteria. For categories involving transformation (e.g., **2B**, **2C**, **3C**, **3D**), both raw and cleaned versions are shown to highlight how the filtering logic operates.

### 6.1 Short constituents (Class 1)

- **1A** — Start with *"baca juga"*, contain capitalized words, and end with "!":
  - *Baca Juga: Google Assistant Bakal Pamit, Digantikan dengan AI Canggih Ini!*

- **1B** — End with "!" and either start with *"baca juga"* or contain capitalized words:
  - *Aplikasi Ini Terbukti Membayar, Begini Cara Dapatkan Cuannya!*

- **1C** — Start with *"baca juga"* only:
  - *BACA JUGA: Kesempatan Terbatas Dapat Saldo Gratis Hingga Rp300.000.*

- **1D** — Contain capitalized words only:
  - *Begini Cara Pinjam Uang di Dompet Digital DANA*

- **1E** — End with "!" only:
  - *Cek Faktanya!*

### 6.2 Medium constituents (Class 2)

- **2A** — Start with *"baca juga"*, contain capitalized words, and end with "!":
  - *Baca Juga: SELAMAT Nomor HP Dompet Elektronik Anda Bisa Klaim Saldo DANA Gratis Rp125.000 Hari Ini Jumat 21 Maret 2025!*

- **2B** — End with "!" and either start with *"baca juga"* or contain capitalized words:
  - **Raw**:  
    *Baca Juga : Sidang Paripurna Ke-5 Masa Persidangan I DPRD Denpasar, Wali Kota Jaya Negara Sampaikan Rancangan Awal RPJMD Kota Denpasar Tahun 2025-2029 Selain promo spesial pembukaan, Wingstop juga menawarkan paket lengkap yaitu Hematnya Juara!*  
  - **Cleaned**:  
    *Baca Juga : Sidang Paripurna Ke-5 Masa Persidangan I DPRD Denpasar, Wali Kota Jaya Negara Sampaikan Rancangan Awal*

- **2C** — Start with *"baca juga"*:
  - **Raw**:  
    *Baca juga: IHSG Terpuruk, Sri Mulyani Sindir Tata Kelola BUMN Sederet saham top gainers di antaranya adalah PT Lion Metal Works Tbk (LION), PT Pradiksi Gunatama Tbk (PGUN), dan PT Daaz Bara Lestari Tbk (DAAZ).*  
  - **Cleaned**:  
    *Baca juga: IHSG Terpuruk, Sri Mulyani Sindir Tata Kelola BUMN*

- **2D** — Contain capitalized words:
  - **Raw**:  
    *Akun Kamu Terdata Dapat Saldo DANA Gratis Rp617.000 dari Klaim Link DANA Kaget Siang Ini, Cek Dompet Digital Ini menjadi kesempatan emas untuk mengumpulkan saldo gratis dengan cara sederhana.*  
  - **Cleaned**:  
    *Akun Kamu Terdata Dapat Saldo DANA Gratis Rp617.000 dari Klaim Link DANA Kaget Siang Ini, Cek Dompet Digital*

### 6.3 Long constituents (Class 3)

- **3C** — Start with *"baca juga"*:
  - **Raw**:  
    *Baca Juga Cara Dapat Tiket Pesawat Murah, Ada Diskon 14% untuk Mudik Lebaran 2025 Pemerintah Jamin Beri Potongan Harga Tiket Pesawat Selama Ramadan dan Mudik Lebaran Rahasia Mendapatkan Harga Tiket Pesawat Surabaya Jakarta Termurah Selain waktu pemesanan, ada beberapa faktor lain yang perlu diperhatikan.*  
  - **Cleaned**:  
    *Baca Juga Cara Dapat Tiket Pesawat Murah, Ada Diskon 14% untuk Mudik Lebaran 2025 Pemerintah Jamin Beri Potongan Harga Tiket Pesawat Selama Ramadan dan Mudik Lebaran Rahasia Mendapatkan Harga Tiket Pesawat Surabaya Jakarta Termurah*

- **3D** — Contain capitalized words and lexical cues (e.g., *cek*, *klaim*, etc.):
  - **Raw**:  
    *Coba Nih Aplikasi Penghasil Saldo DANA Tercepat &amp; Termudah 2025 Beberapa metode ini memanfaatkan fitur dalam aplikasi DANA atau layanan pihak ketiga yang memungkinkan pengguna mendapatkan saldo DANA gratis atau pinjaman tanpa perlu memberikan dokumen pribadi.*
  - **Cleaned**:  
    *Coba Nih Aplikasi Penghasil Saldo DANA Tercepat &amp; Termudah*
