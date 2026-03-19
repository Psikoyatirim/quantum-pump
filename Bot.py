import warnings
warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd
import yfinance as yf
import requests
import time
import os
from datetime import datetime

# ─────────────────────────────────────────
# TELEGRAM AYARLARI
# ─────────────────────────────────────────
TELEGRAM_TOKEN   = os.getenv('TELEGRAM_BOT_TOKEN', '8035211094:AAEqHt4ZosBJsuT1FxdCcTR9p9uJ1O073zY')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID', '-1002715468798')

# ─────────────────────────────────────────
# SUNUCU AYARLARI (SABİT)
# ─────────────────────────────────────────
SCAN_INTERVAL_SECONDS = 1800  # 30 dakika

# ─────────────────────────────────────────
# HİSSE LİSTESİ
# ─────────────────────────────────────────
HISSELER = [
    "A1YEN.IS", "A1CAP.IS", "AYEN.IS", "ACSEL.IS", "ADEL.IS", "ADESE.IS", "ADGYO.IS", "AEFES.IS",
    "AFYON.IS", "AGESA.IS", "AGHOL.IS", "AGROT.IS", "AGYO.IS", "AHGAZ.IS", "AHSGY.IS", "AKBNK.IS",
    "AKCNS.IS", "AKENR.IS", "AKFGY.IS", "AKFIS.IS", "AKFYE.IS", "AKGRT.IS", "AKHAN.IS", "AKMGY.IS",
    "AKSA.IS", "AKSEN.IS", "AKSGY.IS", "AKSUE.IS", "AKYHO.IS", "ALARK.IS", "ALBRK.IS", "ALCAR.IS",
    "ALCTL.IS", "ALFAS.IS", "ALGYO.IS", "ALKA.IS", "ALKIM.IS", "ALKLC.IS", "ALTNY.IS", "ALVES.IS",
    "ANELE.IS", "ANGEN.IS", "ANHYT.IS", "ANSGR.IS", "ARCLK.IS", "ARDYZ.IS", "ARENA.IS", "ARSAN.IS",
    "ARTMS.IS", "ARZUM.IS", "ASELS.IS", "ASGYO.IS", "ASTOR.IS", "ASUZU.IS", "ATAGY.IS", "ATAKP.IS",
    "ATATP.IS", "ATEKS.IS", "ATLAS.IS", "AVGYO.IS", "AVHOL.IS", "AVOD.IS", "AVTUR.IS", "AYDEM.IS",
    "AYES.IS", "AYGAZ.IS", "AZTEK.IS", "BAGFS.IS", "BAKAB.IS", "BALAT.IS", "BALSU.IS", "BANVT.IS",
    "BASCM.IS", "BAYGZ.IS", "BAYRK.IS", "BEGYO.IS", "BERA.IS", "BESLR.IS", "BEYAZ.IS", "BFREN.IS",
    "BIMAS.IS", "BIOEN.IS", "BIZIM.IS", "BJKAS.IS", "BLCYT.IS", "BMSTL.IS", "BNTAS.IS", "BORLS.IS",
    "BORSK.IS", "BOSSA.IS", "BRISA.IS", "BRKO.IS", "BRKSN.IS", "BRSAN.IS", "BRYAT.IS", "BSOKE.IS",
    "BTCIM.IS", "BUCIM.IS", "BURCE.IS", "BURVA.IS", "BVSAN.IS", "CANTE.IS", "CASA.IS", "CCOLA.IS",
    "CELHA.IS", "CEMAS.IS", "CEMTS.IS", "CIMSA.IS", "CLEBI.IS", "CMENT.IS", "COSMO.IS", "CRDFA.IS",
    "CRFSA.IS", "CUSAN.IS", "CWENE.IS", "DAGI.IS", "DARDL.IS", "DENGE.IS", "DERIM.IS", "DESA.IS",
    "DESPC.IS", "DEVA.IS", "DGGYO.IS", "DITAS.IS", "DOAS.IS", "DOHOL.IS", "DOKTA.IS", "DUNYH.IS",
    "DYOBY.IS", "DZGYO.IS", "EBEBK.IS", "ECILC.IS", "ECZYT.IS", "EDIP.IS", "EGEEN.IS", "EGEGY.IS",
    "EGEPO.IS", "EGGUB.IS", "EGSER.IS", "EKGYO.IS", "EKIZ.IS", "EKOS.IS", "EKSUN.IS", "EMKEL.IS",
    "EMNIS.IS", "ENERY.IS", "ENJSA.IS", "ENKAI.IS", "ENTRA.IS", "EPLAS.IS", "ERBOS.IS", "EREGL.IS",
    "ERSU.IS", "ESCOM.IS", "ESEN.IS", "ETILR.IS", "EUHOL.IS", "EUPWR.IS", "EUREN.IS", "EUYO.IS",
    "EYGYO.IS", "FENER.IS", "FONET.IS", "FORMT.IS", "FORTE.IS", "FRIGO.IS", "FROTO.IS", "GARAN.IS",
    "GATEG.IS", "GEDIK.IS", "GEDZA.IS", "GENIL.IS", "GENTS.IS", "GEREL.IS", "GESAN.IS", "GIPTA.IS",
    "GLBMD.IS", "GLCVY.IS", "GLRMK.IS", "GLYHO.IS", "GMTAS.IS", "GOLTS.IS", "GOODY.IS", "GOZDE.IS",
    "GRSEL.IS", "GSDDE.IS", "GSDHO.IS", "GSRAY.IS", "GUBRF.IS", "GWIND.IS", "HALKB.IS", "HATEK.IS",
    "HATSN.IS", "HEDEF.IS", "HEKTS.IS", "HLGYO.IS", "HOROZ.IS", "HRKET.IS", "HUBVC.IS", "HUNER.IS",
    "HURGZ.IS", "ICBCT.IS", "IDGYO.IS", "IHLAS.IS", "IHLGM.IS", "IMASM.IS", "INDES.IS", "INFO.IS",
    "INTEK.IS", "INVEO.IS", "INVES.IS", "ISBIR.IS", "ISCTR.IS", "ISDMR.IS", "ISFIN.IS", "ISGLK.IS",
    "ISGSY.IS", "ISGYO.IS", "ISKUR.IS", "ISMEN.IS", "IZENR.IS", "IZMDC.IS", "JANTS.IS", "KAPLM.IS",
    "KAREL.IS", "KARSN.IS", "KARTN.IS", "KATMR.IS", "KAYSE.IS", "KBORU.IS", "KCHOL.IS", "KENT.IS",
    "KERVN.IS", "KGYO.IS", "KIMMR.IS", "KLGYO.IS", "KLKIM.IS", "KLMSN.IS", "KLNMA.IS", "KLRHO.IS",
    "KLSER.IS", "KLSYN.IS", "KLYPV.IS", "KMPUR.IS", "KNFRT.IS", "KOCMT.IS", "KONKA.IS", "KONTR.IS",
    "KONYA.IS", "KOPOL.IS", "KORDS.IS", "KOTON.IS", "KRDMA.IS", "KRDMB.IS", "KRDMD.IS", "KRONT.IS",
    "KRSTL.IS", "KRTEK.IS", "KRVGD.IS", "KSTUR.IS", "KTSKR.IS", "KUTPO.IS", "KUYAS.IS", "LIDER.IS",
    "LIDFA.IS", "LINK.IS", "LOGO.IS", "LUKSK.IS", "MAALT.IS", "MAGEN.IS", "MAKIM.IS", "MANAS.IS",
    "MARBL.IS", "MARKA.IS", "MARMR.IS", "MARTI.IS", "MAVI.IS", "MEDTR.IS", "MEGAP.IS", "MEGMT.IS",
    "MEPET.IS", "MERCN.IS", "MERIT.IS", "MERKO.IS", "METRO.IS", "MEYSU.IS", "MGROS.IS", "MNDRS.IS",
    "MOBTL.IS", "MOGAN.IS", "MPARK.IS", "MRSHL.IS", "MSGYO.IS", "MTRKS.IS", "MTRYO.IS", "NATEN.IS",
    "NETAS.IS", "NIBAS.IS", "NTGAZ.IS", "NTHOL.IS", "NUGYO.IS", "NUHCM.IS", "OBASE.IS", "ODAS.IS",
    "ORGE.IS", "ORMA.IS", "OSTIM.IS", "OTKAR.IS", "OTTO.IS", "OYAKC.IS", "OYLUM.IS", "OZGYO.IS",
    "OZRDN.IS", "OZSUB.IS", "PAGYO.IS", "PAHOL.IS", "PARSN.IS", "PATEK.IS", "PEKGY.IS", "PENTA.IS",
    "PETKM.IS", "PETUN.IS", "PGSUS.IS", "PKART.IS", "PKENT.IS", "PNSUT.IS", "POLHO.IS", "PRDGS.IS",
    "PRKAB.IS", "PRKME.IS", "PSGYO.IS", "QNBFK.IS", "QNBTR.IS", "RAYSG.IS", "RGYAS.IS", "RODRG.IS",
    "RUBNS.IS", "RYSAS.IS", "SAHOL.IS", "SANEL.IS", "SANFM.IS", "SANKO.IS", "SARKY.IS", "SASA.IS",
    "SAYAS.IS", "SEGMN.IS", "SEGYO.IS", "SEKUR.IS", "SELEC.IS", "SELVA.IS", "SILVR.IS", "SISE.IS",
    "SKBNK.IS", "SKTAS.IS", "SMART.IS", "SNGYO.IS", "SNPAM.IS", "SOKM.IS", "SONME.IS", "SUMAS.IS",
    "SUNTK.IS", "SUWEN.IS", "TATGD.IS", "TAVHL.IS", "TBORG.IS", "TCELL.IS", "TDGYO.IS", "TEKTU.IS",
    "TGSAS.IS", "THYAO.IS", "TKFEN.IS", "TKNSA.IS", "TLMAN.IS", "TMSN.IS", "TOASO.IS", "TRGYO.IS",
    "TRHOL.IS", "TRILC.IS", "TSKB.IS", "TTKOM.IS", "TTRAK.IS", "TUKAS.IS", "TUPRS.IS", "TURSG.IS",
    "ULKER.IS", "ULUSE.IS", "ULUUN.IS", "UNLU.IS", "USAK.IS", "VAKBN.IS", "VAKKO.IS", "VANGD.IS",
    "VBTYZ.IS", "VERTU.IS", "VESBE.IS", "VESTL.IS", "VKGYO.IS", "VKING.IS", "VSNMD.IS"
]

# ─────────────────────────────────────────
# Pine Script parametreleri
# ─────────────────────────────────────────
AP           = 10
MULT2        = 3.0
MAVI_ATR_LEN = 14
MAVI_ATR_MUL = 0.6
SARI_ATR_LEN = 14
SARI_THR_MUL = 2.0
ADX_FARK_MIN = 10.0

PERIOD   = "6mo"
INTERVAL = "1d"


# ─────────────────────────────────────────
# TELEGRAM
# ─────────────────────────────────────────
def telegram_gonder(mesaj: str) -> bool:
    try:
        r = requests.post(
            f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
            data={"chat_id": TELEGRAM_CHAT_ID, "text": mesaj, "parse_mode": "HTML"},
            timeout=10
        )
        return r.status_code == 200
    except Exception:
        return False


# ─────────────────────────────────────────
# PINE SCRIPT HESAPLAMALAR
# ─────────────────────────────────────────
def pine_rma(series: pd.Series, period: int) -> pd.Series:
    return series.ewm(alpha=1.0 / period, adjust=False).mean()


def pine_atr(high, low, close, period):
    prev_close = close.shift(1)
    tr = pd.concat([
        high - low,
        (high - prev_close).abs(),
        (low  - prev_close).abs()
    ], axis=1).max(axis=1)
    return pine_rma(tr, period)


def pine_dmi(high, low, close, di_length=14):
    up   = high.diff()
    down = -(low.diff())
    plus_dm  = pd.Series(np.where((up > down) & (up > 0),   up,   0.0), index=high.index)
    minus_dm = pd.Series(np.where((down > up) & (down > 0), down, 0.0), index=high.index)
    atr_val  = pine_atr(high, low, close, di_length)
    plus_di  = pine_rma(plus_dm,  di_length) / atr_val * 100
    minus_di = pine_rma(minus_dm, di_length) / atr_val * 100
    denom    = (plus_di + minus_di).replace(0, np.nan)
    return ((plus_di - minus_di) / denom) * 100


def pine_cci(high, low, close, period=21):
    tp = (high + low + close) / 3.0
    ma = tp.rolling(period).mean()
    md = tp.rolling(period).apply(lambda x: np.mean(np.abs(x - x.mean())), raw=True)
    return (tp - ma) / (0.015 * md)


def pine_rsi(close, period=14):
    delta    = close.diff()
    gain     = delta.clip(lower=0)
    loss     = (-delta).clip(lower=0)
    avg_gain = pine_rma(gain, period)
    avg_loss = pine_rma(loss, period)
    rs = avg_gain / avg_loss.replace(0, np.nan)
    return 100.0 - (100.0 / (1.0 + rs))


def pine_calc_quantum(close, high, low):
    hl2   = (high + low) / 2.0
    _atr  = pine_atr(high, low, close, AP)
    _cci  = pine_cci(high, low, close, 21)

    upT_arr = (hl2 - _atr * MULT2).values
    dnT_arr = (hl2 + _atr * MULT2).values
    cci_arr = _cci.values

    MT = np.full(len(close), np.nan)
    for i in range(len(close)):
        if np.isnan(upT_arr[i]) or np.isnan(cci_arr[i]):
            continue
        prev_MT = MT[i-1] if i > 0 and not np.isnan(MT[i-1]) else upT_arr[i]
        MT[i] = max(upT_arr[i], prev_MT) if cci_arr[i] >= 0 else min(dnT_arr[i], prev_MT)

    _atr_c = pine_atr(high, low, close, SARI_ATR_LEN)
    thr_c  = (_atr_c * SARI_THR_MUL).values
    src_arr = close.values

    DL = np.full(len(close), np.nan)
    for i in range(len(close)):
        c = src_arr[i]
        t = thr_c[i]
        if np.isnan(t):
            DL[i] = c
            continue
        prev_DL = DL[i-1] if i > 0 and not np.isnan(DL[i-1]) else c
        if   c > prev_DL + t: DL[i] = c - t
        elif c < prev_DL - t: DL[i] = c + t
        else:                  DL[i] = prev_DL

    return pd.Series(MT, index=close.index), pd.Series(DL, index=close.index)


def pine_mavi_atr_hatti(close, high, low):
    atr_val = pine_atr(high, low, close, MAVI_ATR_LEN)
    src_arr = close.values
    atr_arr = atr_val.values

    M = np.full(len(close), np.nan)
    prev = 0.0
    for i in range(len(close)):
        c = src_arr[i]
        a = atr_arr[i] * MAVI_ATR_MUL
        if np.isnan(a):
            M[i] = c
            prev = c
            continue
        M[i] = max(prev, c - a) if c > prev else min(prev, c + a)
        prev = M[i]

    return pd.Series(M, index=close.index)


def pine_crossover(s1, s2):
    return (s1 > s2) & (s1.shift(1) <= s2.shift(1))


def pine_crossunder(s1, s2):
    return (s1 < s2) & (s1.shift(1) >= s2.shift(1))


def quantum_sinyal_hesapla(df: pd.DataFrame) -> dict:
    close = df["Close"].squeeze()
    high  = df["High"].squeeze()
    low   = df["Low"].squeeze()

    as_fark_pct      = pine_dmi(high, low, close)
    rsi_val          = pine_rsi(close, 14)
    mainMT, mainDL   = pine_calc_quantum(close, high, low)
    kirilim          = (mainMT + mainDL) / 2.0
    mavi             = pine_mavi_atr_hatti(close, high, low)

    golden_signal = pine_crossover(mavi, mainDL)  & (as_fark_pct >= ADX_FARK_MIN)
    dump_signal   = pine_crossunder(mavi, mainDL) & (as_fark_pct.abs() >= ADX_FARK_MIN)

    return {
        "fiyat"   : round(float(close.iloc[-1]), 4),
        "mavi"    : round(float(mavi.iloc[-1]), 4),
        "sari"    : round(float(mainDL.iloc[-1]), 4),
        "kirilim" : round(float(kirilim.iloc[-1]), 4),
        "adx_fark": round(float(as_fark_pct.iloc[-1]), 2),
        "rsi"     : round(float(rsi_val.iloc[-1]), 1),
        "pump_son": bool(golden_signal.iloc[-1]),
        "dump_son": bool(dump_signal.iloc[-1]),
    }


# ─────────────────────────────────────────
# ANA TARAMA
# ─────────────────────────────────────────
def tarama_yap(scan_number=1):
    toplam     = len(HISSELER)
    tamamlanan = 0
    hatali     = 0
    pump_list  = []
    dump_list  = []

    print(f"\n{'='*52}")
    print(f"🔍 TARAMA #{scan_number} BAŞLIYOR — {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}")
    print(f"{'='*52}")

    for i, hisse in enumerate(HISSELER, 1):
        if i % 50 == 1:
            print(f"📈 [{i}/{toplam}] İşleniyor...")

        try:
            df = yf.download(
                hisse,
                period=PERIOD,
                interval=INTERVAL,
                progress=False,
                auto_adjust=True
            )

            if df is None or len(df) < 50:
                hatali += 1
                continue

            bilgi          = quantum_sinyal_hesapla(df)
            bilgi["hisse"] = hisse.replace(".IS", "")
            tamamlanan    += 1

            if bilgi["pump_son"]:
                pump_list.append(bilgi)
                print(f"  🟢 PUMP: {bilgi['hisse']} — {bilgi['fiyat']:.4f}")
            if bilgi["dump_son"]:
                dump_list.append(bilgi)
                print(f"  🔴 DUMP: {bilgi['hisse']} — {bilgi['fiyat']:.4f}")

        except Exception:
            hatali += 1

        time.sleep(0.1)

    print(f"\n✅ Tamamlandı: {tamamlanan}/{toplam}  |  ⚠️ Hatalı: {hatali}")
    print(f"🟢 PUMP: {len(pump_list)}  |  🔴 DUMP: {len(dump_list)}")

    # Telegram mesajı
    zaman = datetime.now().strftime("%d.%m.%Y %H:%M")

    if pump_list or dump_list:
        satirlar = [
            "🔬 <b>QUANTUM PUMP &amp; DUMP</b>",
            f"📅 {zaman}  |  🔢 Tarama #{scan_number}",
            f"📊 Taranan: {tamamlanan} hisse",
            "",
        ]

        if pump_list:
            satirlar.append("🟢 <b>PUMP SİNYALLERİ</b>")
            for r in pump_list:
                satirlar.append(
                    f"  • <b>{r['hisse']}</b>\n"
                    f"    Fiyat: {r['fiyat']:.4f}  |  Kırılım: {r['kirilim']:.4f}\n"
                    f"    ADX Fark: {r['adx_fark']:+.1f}%  |  RSI: {r['rsi']:.0f}"
                )
            satirlar.append("")

        if dump_list:
            satirlar.append("🔴 <b>DUMP SİNYALLERİ</b>")
            for r in dump_list:
                satirlar.append(
                    f"  • <b>{r['hisse']}</b>\n"
                    f"    Fiyat: {r['fiyat']:.4f}  |  Kırılım: {r['kirilim']:.4f}\n"
                    f"    ADX Fark: {r['adx_fark']:+.1f}%  |  RSI: {r['rsi']:.0f}"
                )

        satirlar.append(f"\n⏰ Sonraki tarama 30 dakika sonra...")
        basarili = telegram_gonder("\n".join(satirlar))
        print(f"📨 Telegram: {'✅ Gönderildi' if basarili else '❌ Gönderilemedi'}")
    else:
        # Sinyal yoksa da bilgi ver
        mesaj = (
            f"🔬 <b>QUANTUM PUMP &amp; DUMP</b>\n"
            f"📅 {zaman}  |  🔢 Tarama #{scan_number}\n"
            f"📊 Taranan: {tamamlanan} hisse\n\n"
            f"ℹ️ Bu taramada sinyal bulunamadı.\n"
            f"⏰ Sonraki tarama 30 dakika sonra..."
        )
        telegram_gonder(mesaj)
        print("📭 Sinyal yok — bilgi mesajı gönderildi.")


# ─────────────────────────────────────────
# OTOMATİK TARAMA DÖNGÜSÜ
# ─────────────────────────────────────────
def continuous_scan():
    scan_count = 0

    basarili = telegram_gonder(
        f"🤖 <b>Quantum Bot Aktif</b>\n"
        f"📅 {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}\n"
        f"🔄 Her 30 dakikada bir tarama yapılacak"
    )
    print(f"✅ Bot başladı. Telegram: {'OK' if basarili else 'HATA'}")

    while True:
        scan_count += 1
        tarama_yap(scan_number=scan_count)
        print(f"\n⏳ 30 dakika bekleniyor...\n")
        time.sleep(SCAN_INTERVAL_SECONDS)


# ─────────────────────────────────────────
# ANA ÇALIŞTIRMA
# ─────────────────────────────────────────
if __name__ == "__main__":
    print("🚀 QUANTUM PUMP & DUMP Otomatik Tarayıcı")
    continuous_scan()
