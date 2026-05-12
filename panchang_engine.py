"""
Adhyatmik Bharat - Panchang Engine v2.1 FINAL (IST FIXED)
"""
import swisseph as swe, json, sys, pytz
from datetime import datetime, date, timedelta
from astral import LocationInfo
from astral.sun import sun
from astral.moon import moonrise, moonset

swe.set_ephe_path(None)
swe.set_sid_mode(swe.SIDM_LAHIRI)
F = swe.FLG_SIDEREAL

CITIES = {
    "Delhi":      {"lat":28.6139,"lon":77.2090,"tz":"Asia/Kolkata"},
    "Mumbai":     {"lat":19.0760,"lon":72.8777,"tz":"Asia/Kolkata"},
    "Bangalore":  {"lat":12.9716,"lon":77.5946,"tz":"Asia/Kolkata"},
    "Chennai":    {"lat":13.0827,"lon":80.2707,"tz":"Asia/Kolkata"},
    "Kolkata":    {"lat":22.5726,"lon":88.3639,"tz":"Asia/Kolkata"},
    "Hyderabad":  {"lat":17.3850,"lon":78.4867,"tz":"Asia/Kolkata"},
    "Pune":       {"lat":18.5204,"lon":73.8567,"tz":"Asia/Kolkata"},
    "Ahmedabad":  {"lat":23.0225,"lon":72.5714,"tz":"Asia/Kolkata"},
    "Jaipur":     {"lat":26.9124,"lon":75.7873,"tz":"Asia/Kolkata"},
    "Varanasi":   {"lat":25.3176,"lon":82.9739,"tz":"Asia/Kolkata"},
    "Lucknow":    {"lat":26.8467,"lon":80.9462,"tz":"Asia/Kolkata"},
    "Bhopal":     {"lat":23.2599,"lon":77.4126,"tz":"Asia/Kolkata"},
    "Indore":     {"lat":22.7196,"lon":75.8577,"tz":"Asia/Kolkata"},
    "Patna":      {"lat":25.5941,"lon":85.1376,"tz":"Asia/Kolkata"},
    "Nagpur":     {"lat":21.1458,"lon":79.0882,"tz":"Asia/Kolkata"},
    "Haridwar":   {"lat":29.9457,"lon":78.1642,"tz":"Asia/Kolkata"},
    "Ujjain":     {"lat":23.1765,"lon":75.7885,"tz":"Asia/Kolkata"},
    "Mathura":    {"lat":27.4924,"lon":77.6737,"tz":"Asia/Kolkata"},
}

NAK_EN=["Ashwini","Bharani","Krittika","Rohini","Mrigashira","Ardra","Punarvasu","Pushya",
        "Ashlesha","Magha","Purva Phalguni","Uttara Phalguni","Hasta","Chitra","Swati",
        "Vishakha","Anuradha","Jyeshtha","Moola","Purva Ashadha","Uttara Ashadha",
        "Shravana","Dhanishtha","Shatabhisha","Purva Bhadrapada","Uttara Bhadrapada","Revati"]
NAK_HI=["अश्विनी","भरणी","कृत्तिका","रोहिणी","मृगशिरा","आर्द्रा","पुनर्वसु","पुष्य",
        "आश्लेषा","मघा","पूर्व फाल्गुनी","उत्तर फाल्गुनी","हस्त","चित्रा","स्वाति",
        "विशाखा","अनुराधा","ज्येष्ठा","मूल","पूर्व आषाढ़","उत्तर आषाढ़",
        "श्रवण","धनिष्ठा","शतभिषा","पूर्व भाद्रपद","उत्तर भाद्रपद","रेवती"]
NAK_LORD=["Ketu","Shukra","Surya","Chandra","Mangal","Rahu","Brihaspati","Shani","Budh"]*3
NAK_DEITY=["Ashwini Kumars","Yama","Agni","Brahma","Chandra","Rudra","Aditi","Brihaspati",
           "Sarpa","Pitru","Aryaman","Bhaga","Savitar","Vishwakarma","Vayu","Indra-Agni",
           "Mitra","Indra","Nirrti","Apas","Vishvedeva","Vishnu","8 Vasus","Varuna",
           "Aja Ekapada","Ahirbudhnya","Pushan"]

YOG_EN=["Vishkumbha","Priti","Ayushman","Saubhagya","Shobhana","Atiganda","Sukarma","Dhriti",
        "Shoola","Ganda","Vriddhi","Dhruva","Vyaghata","Harshana","Vajra","Siddhi","Vyatipata",
        "Variyana","Parigha","Shiva","Siddha","Sadhya","Shubha","Shukla","Brahma","Indra","Vaidhriti"]
YOG_HI=["विष्कुम्भ","प्रीति","आयुष्मान","सौभाग्य","शोभन","अतिगण्ड","सुकर्मा","धृति",
        "शूल","गण्ड","वृद्धि","ध्रुव","व्याघात","हर्षण","वज्र","सिद्धि","व्यतीपात",
        "वरीयान","परिघ","शिव","सिद्ध","साध्य","शुभ","शुक्ल","ब्रह्म","इन्द्र","वैधृति"]
YOG_GOOD={"Priti","Ayushman","Saubhagya","Shobhana","Sukarma","Dhriti","Vriddhi","Dhruva",
          "Harshana","Siddhi","Shiva","Siddha","Sadhya","Shubha","Shukla","Brahma","Indra"}

KAR_EN=["Bava","Balava","Kaulava","Taitila","Garija","Vanija","Vishti",
        "Shakuni","Chatushpada","Naga","Kimstughna"]
KAR_HI=["बव","बालव","कौलव","तैतिल","गर","वणिज","विष्टि",
        "शकुनि","चतुष्पाद","नाग","किंस्तुघ्न"]
KAR_GOOD={"Bava","Balava","Kaulava","Taitila","Garija","Vanija"}

TTH_EN=["Pratipada","Dwitiya","Tritiya","Chaturthi","Panchami","Shashthi","Saptami",
        "Ashtami","Navami","Dashami","Ekadashi","Dwadashi","Trayodashi","Chaturdashi","Purnima"]
TTH_HI=["प्रतिपदा","द्वितीया","तृतीया","चतुर्थी","पंचमी","षष्ठी","सप्तमी",
        "अष्टमी","नवमी","दशमी","एकादशी","द्वादशी","त्रयोदशी","चतुर्दशी","पूर्णिमा"]

MAS_EN=["Vaishakh","Jyeshtha","Ashadha","Shravan","Bhadrapada","Ashwin",
        "Kartik","Margashirsha","Pausha","Magha","Phalguna","Chaitra"]
MAS_HI=["वैशाख","ज्येष्ठ","आषाढ़","श्रावण","भाद्रपद","आश्विन",
        "कार्तिक","मार्गशीर्ष","पौष","माघ","फाल्गुन","चैत्र"]

RSH_EN=["Mesh","Vrishabh","Mithun","Kark","Simha","Kanya",
        "Tula","Vrishchik","Dhanu","Makar","Kumbh","Meen"]
RSH_HI=["मेष","वृषभ","मिथुन","कर्क","सिंह","कन्या",
        "तुला","वृश्चिक","धनु","मकर","कुम्भ","मीन"]

WD_HI=["सोमवार","मंगलवार","बुधवार","गुरुवार","शुक्रवार","शनिवार","रविवार"]
WD_DEI_HI=["शिव","मंगल","बुध","बृहस्पति","शुक्र","शनि","सूर्य"]
WD_DEI_EN=["Shiva","Mangal","Budh","Brihaspati","Shukra","Shani","Surya"]

RAHU_S={0:2,1:7,2:5,3:6,4:4,5:3,6:8}
YAMA_S={0:5,1:4,2:3,3:2,4:8,5:7,6:6}
GULI_S={0:8,1:2,2:7,3:6,4:5,5:4,6:3}

CHAU={
    0:["Amrit","Kaal","Shubh","Rog","Udveg","Char","Labh","Amrit"],
    1:["Rog","Udveg","Char","Labh","Amrit","Kaal","Shubh","Rog"],
    2:["Labh","Amrit","Kaal","Shubh","Rog","Udveg","Char","Labh"],
    3:["Shubh","Rog","Udveg","Char","Labh","Amrit","Kaal","Shubh"],
    4:["Udveg","Char","Labh","Amrit","Kaal","Shubh","Rog","Udveg"],
    5:["Kaal","Shubh","Rog","Udveg","Char","Labh","Amrit","Kaal"],
    6:["Udveg","Char","Labh","Amrit","Kaal","Shubh","Rog","Udveg"],
}
CHAU_HI={"Amrit":"अमृत","Kaal":"काल","Shubh":"शुभ","Rog":"रोग","Udveg":"उद्वेग","Char":"चर","Labh":"लाभ"}
CHAU_GOOD={"Amrit","Shubh","Labh","Char"}
DUR={0:[7,15],1:[6,7],2:[8],3:[14],4:[9,10],5:[5,14],6:[9]}

SVNAM=["Prabhava","Vibhava","Shukla","Pramoda","Prajapati","Angirasa","Shrimukha","Bhava",
       "Yuva","Dhatru","Ishvara","Bahudhanya","Pramathi","Vikrama","Vrisha","Chitrabhanu",
       "Subhanu","Tarana","Parthiva","Vyaya","Sarvajit","Sarvadhari","Virodhi","Vikruti",
       "Khara","Nandana","Vijaya","Jaya","Manmatha","Durmukhi","Hevilambi","Vilambi",
       "Vikari","Sharvari","Plava","Shubhakruth","Sobhakruth","Krodhi","Vishvavasu",
       "Parabhava","Plavanga","Kilaka","Saumya","Sadharana","Virodhikruth","Paridhaavi",
       "Pramaadi","Aananda","Rakshasa","Nala","Pingala","Kalayukta","Siddharthi","Raudra",
       "Durmathi","Dundubhi","Rudhirodgari","Raktakshi","Krodhana","Akshaya"]

FEST={
    (1,9,"Shukla"):{"name":"Ram Navami","name_hi":"राम नवमी"},
    (1,15,"Shukla"):{"name":"Hanuman Jayanti","name_hi":"हनुमान जयंती"},
    (2,3,"Shukla"):{"name":"Akshaya Tritiya","name_hi":"अक्षय तृतीया"},
    (2,11,"Shukla"):{"name":"Mohini Ekadashi","name_hi":"मोहनी एकादशी"},
    (3,11,"Shukla"):{"name":"Nirjala Ekadashi","name_hi":"निर्जला एकादशी"},
    (4,11,"Shukla"):{"name":"Dev Shayani Ekadashi","name_hi":"देव शयनी एकादशी"},
    (4,15,"Shukla"):{"name":"Guru Purnima","name_hi":"गुरु पूर्णिमा"},
    (5,15,"Shukla"):{"name":"Raksha Bandhan","name_hi":"रक्षा बंधन"},
    (5,8,"Krishna"):{"name":"Janmashtami","name_hi":"कृष्ण जन्माष्टमी"},
    (5,4,"Shukla"):{"name":"Ganesh Chaturthi","name_hi":"गणेश चतुर्थी"},
    (6,1,"Shukla"):{"name":"Navratri Begins","name_hi":"शारदीय नवरात्रि"},
    (6,10,"Shukla"):{"name":"Dussehra","name_hi":"दशहरा"},
    (7,13,"Krishna"):{"name":"Dhanteras","name_hi":"धनतेरस"},
    (7,14,"Krishna"):{"name":"Narak Chaturdashi","name_hi":"नरक चतुर्दशी"},
    (7,15,"Krishna"):{"name":"Diwali","name_hi":"दीपावली"},
    (7,1,"Shukla"):{"name":"Govardhan Puja","name_hi":"गोवर्धन पूजा"},
    (7,2,"Shukla"):{"name":"Bhai Dooj","name_hi":"भाई दूज"},
    (7,11,"Shukla"):{"name":"Dev Uthani Ekadashi","name_hi":"देव उठनी एकादशी"},
    (7,15,"Shukla"):{"name":"Kartik Purnima","name_hi":"कार्तिक पूर्णिमा"},
    (9,5,"Shukla"):{"name":"Basant Panchami","name_hi":"बसंत पंचमी"},
    (10,13,"Krishna"):{"name":"Mahashivratri","name_hi":"महाशिवरात्रि"},
    (11,15,"Shukla"):{"name":"Holi","name_hi":"होली"},
    (11,14,"Shukla"):{"name":"Holika Dahan","name_hi":"होलिका दहन"},
}

def pt(t): return datetime.strptime(t,"%H:%M")
def slot(sr24,n,m=90):
    s=pt(sr24)+timedelta(minutes=m*(n-1)); e=pt(sr24)+timedelta(minutes=m*n)
    return f"{s.strftime('%I:%M %p')} - {e.strftime('%I:%M %p')}"
def rashi(lon):
    i=int(lon/30)%12; return {"name":RSH_EN[i],"name_hi":RSH_HI[i]}

def calc_tithi(sl,ml):
    diff=(ml-sl)%360; n=int(diff/12)+1
    if n>30: n=30
    p="Shukla" if n<=15 else "Krishna"
    ph="शुक्ल" if n<=15 else "कृष्ण"
    if n==15: nm,nh="Purnima","पूर्णिमा"
    elif n==30: nm,nh="Amavasya","अमावस्या"
    elif n<=15: nm,nh=TTH_EN[n-1],TTH_HI[n-1]
    else: nm,nh=TTH_EN[n-16],TTH_HI[n-16]
    return {"number":n,"name":nm,"name_hi":nh,"paksha":p,"paksha_hi":ph}

def calc_nak(ml):
    sz=360/27; i=min(int(ml/sz),26); pada=int((ml%sz)/(sz/4))+1
    return {"name":NAK_EN[i],"name_hi":NAK_HI[i],"pada":pada,
            "index":i+1,"lord":NAK_LORD[i],"deity":NAK_DEITY[i]}

def calc_yog(sl,ml):
    i=min(int(((sl+ml)%360)/(360/27)),26)
    nat="good" if YOG_EN[i] in YOG_GOOD else "bad"
    return {"name":YOG_EN[i],"name_hi":YOG_HI[i],"nature":nat}

def calc_kar(sl,ml,second=False):
    kn=int(((ml-sl)%360)/6)+(1 if second else 0)
    if kn==0: i=10
    elif kn>=57: i={57:7,58:8,59:9,60:10}.get(kn,10)
    else: i=(kn-1)%7
    i=min(i,10)
    nat="good" if KAR_EN[i] in KAR_GOOD else "bad"
    return {"name":KAR_EN[i],"name_hi":KAR_HI[i],"nature":nat}

def calc_masa(sl):
    i = int(sl/30)%12
    amanta_en = MAS_EN[i]
    amanta_hi = MAS_HI[i]
    purn_i = (i+1)%12
    purnimanta_en = MAS_EN[purn_i]
    purnimanta_hi = MAS_HI[purn_i]
    return {
        "index": i+1,
        "masa": amanta_en,
        "masa_hi": amanta_hi,
        "purnimanta": purnimanta_en,
        "purnimanta_hi": purnimanta_hi,
    }
def vikram(y,m,d): return y+57 if (m>4 or (m==4 and d>=14)) else y+56
def shaka(y,m,d): return y-78 if m>3 else y-79
def svname(vs): return SVNAM[(vs-1)%60]

def get_times(dt,city):
    c=CITIES.get(city,CITIES["Delhi"])
    loc=LocationInfo(city,"India",c["tz"],c["lat"],c["lon"])
    s=sun(loc.observer,date=dt,tzinfo=loc.timezone)
    try: mr=moonrise(loc.observer,date=dt,tzinfo=loc.timezone)
    except: mr=None
    try: ms=moonset(loc.observer,date=dt,tzinfo=loc.timezone)
    except: ms=None
    return {
        "sunrise":s["sunrise"].strftime("%I:%M %p"),
        "sunset":s["sunset"].strftime("%I:%M %p"),
        "sunrise_24":s["sunrise"].strftime("%H:%M"),
        "sunset_24":s["sunset"].strftime("%H:%M"),
        "solar_noon":s["noon"].strftime("%I:%M %p"),
        "moonrise":mr.strftime("%I:%M %p") if mr else "N/A",
        "moonset":ms.strftime("%I:%M %p") if ms else "N/A",
    }

def abhijit(sr24,ss24):
    sr=pt(sr24); ss=pt(ss24); mid=sr+timedelta(seconds=(ss-sr).seconds//2)
    return f"{(mid-timedelta(minutes=24)).strftime('%I:%M %p')} - {(mid+timedelta(minutes=24)).strftime('%I:%M %p')}"

def amrit(ml,sr24):
    sr=pt(sr24); off=(int(ml/(360/27))*47)%(24*60)
    base=pt("00:00")+timedelta(minutes=off)
    while base<sr: base+=timedelta(minutes=228)
    return f"{base.strftime('%I:%M %p')} - {(base+timedelta(minutes=228)).strftime('%I:%M %p')}"

def varjyam(ml,sr24):
    sr=pt(sr24); off=(int(ml/(360/27))*63+45)%(24*60)
    base=pt("00:00")+timedelta(minutes=off)
    while base<sr: base+=timedelta(minutes=96)
    return f"{base.strftime('%I:%M %p')} - {(base+timedelta(minutes=96)).strftime('%I:%M %p')}"

def dur_m(wd,sr24):
    sr=pt(sr24)
    return [f"{(sr+timedelta(minutes=48*(s-1))).strftime('%I:%M %p')} - {(sr+timedelta(minutes=48*s)).strftime('%I:%M %p')}"
            for s in DUR.get(wd,[])]

def chaughadi(wd,sr24,ss24):
    sr=pt(sr24); ss=pt(ss24); dm=(ss-sr).seconds//60; sm=dm/8; out=[]
    for i,nm in enumerate(CHAU[wd]):
        s=sr+timedelta(minutes=sm*i); e=sr+timedelta(minutes=sm*(i+1))
        out.append({"slot":i+1,"name":nm,"name_hi":CHAU_HI[nm],
                    "time":f"{s.strftime('%I:%M %p')} - {e.strftime('%I:%M %p')}","is_good":nm in CHAU_GOOD})
    return out

def graha(jd):
    pl=[("Surya","सूर्य",swe.SUN),("Chandra","चन्द्र",swe.MOON),
        ("Mangal","मंगल",swe.MARS),("Budh","बुध",swe.MERCURY),
        ("Brihaspati","बृहस्पति",swe.JUPITER),("Shukra","शुक्र",swe.VENUS),
        ("Shani","शनि",swe.SATURN)]
    out=[]
    for en,hi,pid in pl:
        pos,_=swe.calc_ut(jd,pid,F); lon=pos[0]%360; r=rashi(lon)
        out.append({"planet":en,"planet_hi":hi,"longitude":round(lon,2),
                    "degree_in_rashi":f"{lon%30:.1f}","rashi":r["name"],"rashi_hi":r["name_hi"]})
    rp,_=swe.calc_ut(jd,swe.TRUE_NODE,F); rl=rp[0]%360; kl=(rl+180)%360
    for en,hi,lon in [("Rahu","राहु",rl),("Ketu","केतु",kl)]:
        r=rashi(lon)
        out.append({"planet":en,"planet_hi":hi,"longitude":round(lon,2),
                    "degree_in_rashi":f"{lon%30:.1f}","rashi":r["name"],"rashi_hi":r["name_hi"]})
    return out

def vrats(tnum,paksha,wd):
    v=[]
    if tnum in [11,26]: v.append({"name":f"{paksha} Ekadashi","name_hi":"एकादशी व्रत","type":"major"})
    if tnum in [4,19] and paksha=="Krishna": v.append({"name":"Sankashti Chaturthi","name_hi":"संकष्टी चतुर्थी","type":"major"})
    elif tnum==4: v.append({"name":"Vinayaka Chaturthi","name_hi":"विनायक चतुर्थी","type":"medium"})
    if tnum in [13,28]: v.append({"name":"Pradosh Vrat","name_hi":"प्रदोष व्रत","type":"major"})
    if tnum==15: v.append({"name":"Purnima Vrat","name_hi":"पूर्णिमा व्रत","type":"major"})
    if tnum==30: v.append({"name":"Amavasya","name_hi":"अमावस्या","type":"major"})
    if tnum in [6,21]: v.append({"name":"Sashti Vrat","name_hi":"षष्ठी व्रत","type":"medium"})
    if tnum in [8,23]: v.append({"name":"Ashtami Vrat","name_hi":"अष्टमी व्रत","type":"medium"})
    dn=["Somvar","Mangalvar","Budhvar","Guruvar","Shukravar","Shanivar","Ravivar"]
    dh=["सोमवार व्रत","मंगलवार व्रत","बुधवार व्रत","गुरुवार व्रत","शुक्रवार व्रत","शनिवार व्रत","रविवार व्रत"]
    v.append({"name":f"{dn[wd]} Vrat","name_hi":dh[wd],"type":"minor"})
    return v

def calculate_panchang(target_date=None,city="Delhi"):
    if target_date is None: target_date=date.today()
    Y,M,D=target_date.year,target_date.month,target_date.day
    wd=target_date.weekday()
    jd=swe.julday(Y,M,D,0.5)
    sl,_=swe.calc_ut(jd,swe.SUN,F);  sl=sl[0]%360
    ml,_=swe.calc_ut(jd,swe.MOON,F); ml=ml[0]%360
    ti=calc_tithi(sl,ml); nak=calc_nak(ml); yo=calc_yog(sl,ml)
    k1=calc_kar(sl,ml,False); k2=calc_kar(sl,ml,True)
    mas=calc_masa(sl); vs=vikram(Y,M,D); shk=shaka(Y,M,D)
    tm=get_times(target_date,city); sr24,ss24=tm["sunrise_24"],tm["sunset_24"]
    sr=rashi(sl); mr=rashi(ml)
    return {
        "date":{
            "gregorian":target_date.strftime("%d %B %Y"),
            "gregorian_short":target_date.strftime("%Y-%m-%d"),
            "weekday_en":target_date.strftime("%A"),
            "weekday_hi":WD_HI[wd],
            "day_deity":WD_DEI_EN[wd],
            "day_deity_hi":WD_DEI_HI[wd],
            "prev_date":(target_date-timedelta(days=1)).strftime("%Y-%m-%d"),
            "next_date":(target_date+timedelta(days=1)).strftime("%Y-%m-%d"),
        },
        "hindu_calendar":{
            "vikram_samvat":vs,
            "samvat_name":svname(vs),
            "shaka_samvat":shk,
            "masa": mas["masa"],
            "masa_hi": mas["masa_hi"],
            "purnimanta": mas["purnimanta"],
            "purnimanta_hi": mas["purnimanta_hi"],
            "paksha":ti["paksha"],
            "paksha_hi":ti["paksha_hi"],
        },
        "panch_ang":{
            "tithi":ti,"nakshatra":nak,"yoga":yo,"karana1":k1,"karana2":k2,
            "var":{"name":target_date.strftime("%A"),"name_hi":WD_HI[wd],"deity":WD_DEI_EN[wd]},
        },
        "sun_moon":{**tm,
            "sun_rashi":sr["name"],"sun_rashi_hi":sr["name_hi"],
            "moon_rashi":mr["name"],"moon_rashi_hi":mr["name_hi"],
        },
        "auspicious":{
            "abhijit_muhurat":abhijit(sr24,ss24),
            "amrit_kalam":amrit(ml,sr24),
        },
        "inauspicious":{
            "rahu_kalam":slot(sr24,RAHU_S[wd]),
            "yama_kandam":slot(sr24,YAMA_S[wd]),
            "gulika_kalam":slot(sr24,GULI_S[wd]),
            "varjyam":varjyam(ml,sr24),
            "dur_muhurtam":dur_m(wd,sr24),
        },
        "chaughadi":chaughadi(wd,sr24,ss24),
        "graha_positions":graha(jd),
        "vrats":vrats(ti["number"],ti["paksha"],wd),
        "festival":FEST.get((mas["index"],ti["number"],ti["paksha"])),
        "city":city,
    }

if __name__=="__main__":
    IST = pytz.timezone('Asia/Kolkata')
    india_now = datetime.now(IST)
    t = india_now.date() 
    city = "Delhi"
    if len(sys.argv)>=2:
        try: t=date.fromisoformat(sys.argv[1])
        except: pass
    if len(sys.argv)>=3: city=sys.argv[2]
    print(json.dumps(calculate_panchang(t,city),ensure_ascii=False,indent=2))
