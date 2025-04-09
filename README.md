# news-content-cleaner
This program cleans news content text data from irrelevant syntactic constituents initiated by "baca juga" and "advertisement" strings, e.g.:

> "BACA JUGA: Dapatkan Hadiah Uang Gratis Melalui DANA Kaget".

The program is intended for media monitoring purposes, spefically, to clean text data for share of voice (SOV) analysis of news coverage across monitored brands.

The data cleaning algorithm removes irrelevant sentences by analyzing how syntactic constituents associated with the "baca juga" strings are structured in news content [more information here](docs/analysis.ipynb). Namely, it determines irrelevant sentences by means of regular expression matching, followed by analysis of sentence structure (word length, punctuation usage, salient lemmas), and/or sentence segmentation/tokenization using NLTK library.

## Example uses:
### Punctuated irrelevant syntactic constituents
Uncleaned news content:
> Berbelanja di aplikasi Shopee akan semakin nyaman dengan menggunakan voucher gratis ongkir, cashback hingga potongan diskon. Itulah sebabnya Anda harus mengetahui cara mendapatkan voucher Shopee gratis ongkir dan cashback, untuk belanja hemat. Voucher Shopee memiliki perbedaan sesuai fungsinya. Voucher gratis ongkir berfungsi untuk mendapatkan gratis ongkos kirim. Voucher cashback berfungsi untuk mendapatkan cashback berupa koin shopee. Sedangkan voucher diskon berfungsi untuk mendapat potongan diskon. **BACA JUGA: Butuh Dana Cepat Rp5,5 Juta? Pahami Cara Pinjam Uang di Shopee Paylater dan Shopee Pinjam**. Ada 5 cara mendapatkan voucher Shopee gratis ongkir, cashback dan juga potongan diskon. Berikut cara mendapatkan sekaligus mengklaim voucher Shopee, yang dikutip dari halaman bantuan Shopee, help.shopee.co.id: 1. Klaim Voucher Shopee Voucher Shopee juga bisa diklaim dengan mudah untuk mendapatkan cashback koin hingga gratis ongkir di menu utama.

Cleaned news content:

> Berbelanja di aplikasi Shopee akan semakin nyaman dengan menggunakan voucher gratis ongkir, cashback hingga potongan diskon. Itulah sebabnya Anda harus mengetahui cara mendapatkan voucher Shopee gratis ongkir dan cashback, untuk belanja hemat. Voucher Shopee memiliki perbedaan sesuai fungsinya. Voucher gratis ongkir berfungsi untuk mendapatkan gratis ongkos kirim. Voucher cashback berfungsi untuk mendapatkan cashback berupa koin shopee. Sedangkan voucher diskon berfungsi untuk mendapat potongan diskon. Ada 5 cara mendapatkan voucher Shopee gratis ongkir, cashback dan juga potongan diskon. Berikut cara mendapatkan sekaligus mengklaim voucher Shopee, yang dikutip dari halaman bantuan Shopee, help.shopee.co.id: 1. Klaim Voucher Shopee Voucher Shopee juga bisa diklaim dengan mudah untuk mendapatkan cashback koin hingga gratis ongkir di menu utama.

It removes the promotional/advertising "**BACA JUGA: Butuh Dana Cepat Rp5,5 Juta? Pahami Cara Pinjam Uang di Shopee Paylater dan Shopee Pinjam**" phrase mentioning the brand DANA from news mentioning the brand Shopee.

### Unpunctuated irrelevant syntactic consituents
Uncleaned news content:
> lorem ipsum

Cleaned news content:
> lorem ipsum

### Sequences of irrelevant syntactic consituents, where some consituents are not initiated by "baca juga" string
Uncleaned news content:
> lorem ipsum

Cleaned news content:
> lorem ipsum

## Getting started
Type this into the terminal to download the required libraries in this program:
```
pip install pandas
pip install nltk
```
