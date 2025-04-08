# news-content-cleaner
This program cleans news content text data from irrelevant sentence segments initiated by "baca juga" and "advertisement" strings, e.g.:

> "BACA JUGA: Dapatkan Hadiah Uang Gratis Melalui DANA Kaget".

The program is intended for media monitoring purposes, spefically, for analyzing the share of voice (SOV) of news coverage across monitored brands.

The data cleaning algorithm removes irrelevant sentences by analyzing how sentences or phrases associated with the "baca juga" strings are structured in news content [more information here](docs/analysis.ipynb). Namely, it determines irrelevant sentences by means of regular expression matching, followed by analysis of sentence structure (word length, punctuation usage, salient lemmas), and/or sentence segmentation/tokenization using NLTK library.

## Example uses:
Uncleaned news content:
> Berbelanja di aplikasi Shopee akan semakin nyaman dengan menggunakan voucher gratis ongkir, cashback hingga potongan diskon. Itulah sebabnya Anda harus mengetahui cara mendapatkan voucher Shopee gratis ongkir dan cashback, untuk belanja hemat. Voucher Shopee memiliki perbedaan sesuai fungsinya. Voucher gratis ongkir berfungsi untuk mendapatkan gratis ongkos kirim. Voucher cashback berfungsi untuk mendapatkan cashback berupa koin shopee. Sedangkan voucher diskon berfungsi untuk mendapat potongan diskon. **BACA JUGA: Butuh Dana Cepat Rp5,5 Juta? Pahami Cara Pinjam Uang di Shopee Paylater dan Shopee Pinjam**. Ada 5 cara mendapatkan voucher Shopee gratis ongkir, cashback dan juga potongan diskon. Berikut cara mendapatkan sekaligus mengklaim voucher Shopee, yang dikutip dari halaman bantuan Shopee, help.shopee.co.id: 1. Klaim Voucher Shopee Voucher Shopee juga bisa diklaim dengan mudah untuk mendapatkan cashback koin hingga gratis ongkir di menu utama.

Cleaned news content:

> Berbelanja di aplikasi Shopee akan semakin nyaman dengan menggunakan voucher gratis ongkir, cashback hingga potongan diskon. Itulah sebabnya Anda harus mengetahui cara mendapatkan voucher Shopee gratis ongkir dan cashback, untuk belanja hemat. Voucher Shopee memiliki perbedaan sesuai fungsinya. Voucher gratis ongkir berfungsi untuk mendapatkan gratis ongkos kirim. Voucher cashback berfungsi untuk mendapatkan cashback berupa koin shopee. Sedangkan voucher diskon berfungsi untuk mendapat potongan diskon. Ada 5 cara mendapatkan voucher Shopee gratis ongkir, cashback dan juga potongan diskon. Berikut cara mendapatkan sekaligus mengklaim voucher Shopee, yang dikutip dari halaman bantuan Shopee, help.shopee.co.id: 1. Klaim Voucher Shopee Voucher Shopee juga bisa diklaim dengan mudah untuk mendapatkan cashback koin hingga gratis ongkir di menu utama.

It removes the promotional/advertising "**BACA JUGA: Butuh Dana Cepat Rp5,5 Juta? Pahami Cara Pinjam Uang di Shopee Paylater dan Shopee Pinjam**" phrase mentioning the brand DANA from news mentioning the brand Shopee.

## Getting started
Type this into the terminal to download the required libraries in this program:
```
pip install pandas
pip install nltk
```
