import pandas as pd
import numpy as np

# Daftar 150 saham (Pindahkan list panjangmu ke sini)
active_tickers = [
               # --- 1. JANGKAR LIKUIDITAS & BLUE CHIP AKTIF (20 Saham) ---
            "BBCA.JK", "BBRI.JK", "BMRI.JK", "BBNI.JK", "BBTN.JK", "BRIS.JK", "ARTO.JK", "BBYB.JK", "ASII.JK", "TLKM.JK",
            "UNVR.JK", "KLBF.JK", "INDF.JK", "ICBP.JK", "AMMN.JK", "GOTO.JK", "BUKA.JK", "EMTK.JK", "ASHA.JK", "AUTO.JK",

            # --- 2. HIGH BETA, TEKNOLOGI & GRUP KONGROMERAT (25 Saham) ---
            "BREN.JK", "CUAN.JK", "TPIA.JK", "BRPT.JK", "WIRG.JK", "FILM.JK", "MLPL.JK", "MPPA.JK", "KPIG.JK", "LPKR.JK",
            "LPPF.JK", "MNCN.JK", "PWON.JK", "SCMA.JK", "SRTG.JK", "BMTR.JK", "BSDE.JK", "CTRA.JK", "DILD.JK", "JSMR.JK",
            "CENT.JK", "CFIN.JK", "PANS.JK", "GGRM.JK", "KAEF.JK",

            # --- 3. KOMODITAS: ENERGI, EMAS & MINERAL (35 Saham) ---
            "ADRO.JK", "PTBA.JK", "ITMG.JK", "HRUM.JK", "MEDC.JK", "ENRG.JK", "SGER.JK", "MBMA.JK", "NCKL.JK", "ANTM.JK",
            "BRMS.JK", "MDKA.JK", "TINS.JK", "DKFT.JK", "KKGI.JK", "BUMI.JK", "DEWA.JK", "DOID.JK", "ELSA.JK", "AKRA.JK",
            "PGAS.JK", "PGEO.JK", "COAL.JK", "ELPI.JK", "RMKO.JK", "RMKE.JK", "BIPI.JK", "WINS.JK", "SIDO.JK", "SMGR.JK",
            "LSIP.JK", "SSMS.JK", "TBLA.JK", "TKIM.JK", "TOWR.JK",

            # --- 4. FAVORIT SCALPER, LAPIS 3 & WILD CARD (70 Saham) ---
            "BCIP.JK", "BAJA.JK", "AADI.JK", "ACES.JK", "PANI.JK", "CHIP.JK", "RGAS.JK", "GULA.JK", "RAFI.JK", "NZIA.JK",
            "CAKK.JK", "YELO.JK", "KAYU.JK", "WIIM.JK", "PACK.JK", "VAST.JK", "HALO.JK", "FUTR.JK", "TRON.JK", "VKTR.JK",
            "INET.JK", "CYBR.JK", "MUTU.JK", "HUMI.JK", "STRK.JK", "SURI.JK", "LIVE.JK", "VISI.JK", "DATA.JK", "CARS.JK",
            "CLEO.JK", "ERAA.JK", "ESSA.JK", "EXCL.JK", "GJTL.JK", "HMSP.JK", "MAPI.JK", "MPMX.JK", "PNLF.JK", "PTPP.JK",
            "WIKA.JK", "SSIA.JK", "ADMR.JK", "HEAL.JK", "MDKI.JK", "SMLE.JK", "ACRO.JK", "CGAS.JK", "NICE.JK", "MSJA.JK",
            "RAJA.JK", "RALS.JK", "SMSM.JK", "TBIG.JK", "BIRD.JK", "BKSL.JK", "BWPT.JK", "TAYS.JK", "NATO.JK", "BULL.JK",
            "APIC.JK", "META.JK", "ASPI.JK", "AWAN.JK", "DOOH.JK", "LABA.JK", "GRPH.JK", "AREA.JK", "ATLA.JK", "SOLA.JK"
                   ]


def calculate_indicators(df):
    # Pengaman: pastikan kolom yang dibutuhkan ada
    required_columns = ['Open', 'High', 'Low', 'Close', 'Volume']
    if not all(col in df.columns for col in required_columns):
        return None

    if len(df) < 200:
        return None

    df = df.copy()

    # 1. EMA 5, 20, 200
    df['ema5'] = df['Close'].ewm(span=5, adjust=False).mean()
    df['ema20'] = df['Close'].ewm(span=20, adjust=False).mean()
    df['ema200'] = df['Close'].ewm(span=200, adjust=False).mean()

    # 2. RSI 14
    delta = df['Close'].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.ewm(com=13, adjust=False).mean()
    avg_loss = loss.ewm(com=13, adjust=False).mean()
    rs = avg_gain / (avg_loss + 1e-10)
    df['rsi'] = 100 - (100 / (1 + rs))

    # 3. VWAP
    typical_price = (df['High'] + df['Low'] + df['Close']) / 3
    df['vwap'] = (typical_price * df['Volume']).rolling(window=14).sum() / (df['Volume'].rolling(window=14).sum() + 1e-10)

    # 4. ATR 14
    high_low = df['High'] - df['Low']
    high_cp = (df['High'] - df['Close'].shift()).abs()
    low_cp = (df['Low'] - df['Close'].shift()).abs()
    tr = pd.concat([high_low, high_cp, low_cp], axis=1).max(axis=1)
    df['atr'] = tr.ewm(com=13, adjust=False).mean()

    # 5. ADX 14
    plus_dm = df['High'].diff()
    minus_dm = df['Low'].diff()
    plus_dm = np.where((plus_dm > minus_dm) & (plus_dm > 0), plus_dm, 0.0)
    minus_dm = np.where((minus_dm > plus_dm) & (minus_dm > 0), minus_dm, 0.0)

    plus_di = 100 * (pd.Series(plus_dm, index=df.index).ewm(com=13, adjust=False).mean() / (df['atr'] + 1e-10))
    minus_di = 100 * (pd.Series(minus_dm, index=df.index).ewm(com=13, adjust=False).mean() / (df['atr'] + 1e-10))

    dx = 100 * (plus_di - minus_di).abs() / ((plus_di + minus_di) + 1e-10)
    df['adx'] = dx.ewm(com=13, adjust=False).mean()

    return d
