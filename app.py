import streamlit as st

# --- פונקציות חישוב (מטאורולוגיה, טכני ופיזיקה) ---

def calculate_density_altitude(pressure_alt, temp):
    """חישוב רום צפיפות - קריטי למבחן המקצועי"""
    # נוסחת קירוב: Pressure Altitude + [120 * (OAT - ISA_Temp)]
    isa_temp = 15
    density_alt = pressure_alt + (120 * (temp - isa_temp))
    return density_alt

def calculate_cg(weights, arms):
    """חישוב מרכז כובד (Center of Gravity)"""
    total_moment = sum(w * a for w, a in zip(weights, arms))
    total_weight = sum(weights)
    if total_weight == 0: return 0
    return round(total_moment / total_weight, 2)

def convert_units(value, conversion_type):
    """מחשבון המרות תעופתי"""
    conversions = {
     "מייל לק'מ": value * 1.609,
"מטר לשנייה לקמ\"ש": value * 3.6,        "רגל למטר": value * 0.3048
    }
    return round(conversions.get(conversion_type, 0), 2)

# --- ממשק המשתמש ---

def main():
    st.set_page_config(page_title="RT-A Exam Expert", layout="wide")
    st.title("🚁 Drone AI Expert - מערכת עזר למבחן רת\"א (עד 25 ק\"ג)")
    st.markdown("---")

    # טאבים לפי נושאי המצגת וחומר העזר
    tab1, tab2, tab3, tab4 = st.tabs(["🌤️ מטאורולוגיה וגבהים", "⚖️ משקל ואיזון (CG)", "🔋 סוללות וחשמל", "📏 המרות תעופתיות"])

    with tab1:
        st.header("חישוב רום צפיפות (Density Altitude)")
        st.info("רום צפיפות גבוה מפחית את ביצועי המנועים והעילוי.")
        c1, c2 = st.columns(2)
        p_alt = c1.number_input("רום לחץ (Pressure Altitude) ברגליים:", value=0)
        oat = c2.number_input("טמפרטורה חיצונית (°C):", value=15)
        d_alt = calculate_density_altitude(p_alt, oat)
        st.metric("רום צפיפות (Density Altitude)", f"{d_alt} רגל")

    with tab2:
        st.header("חישוב מרכז כובד (Center of Gravity)")
        st.write("הזן משקל (ק\"ג) וזרוע (ס\"מ) עבור רכיבי הכלי:")
        
        col_w, col_a = st.columns(2)
        w1 = col_w.number_input("משקל גוף + מנועים:", value=10.0)
        a1 = col_a.number_input("זרוע גוף (ס\"מ):", value=0.0)
        w2 = col_w.number_input("משקל סוללה:", value=5.0)
        a2 = col_a.number_input("זרוע סוללה (ס\"מ):", value=15.0)
        w3 = col_w.number_input("משקל מטען (Payload):", value=2.0)
        a3 = col_a.number_input("זרוע מטען (ס\"מ):", value=-10.0)
        
        cg_result = calculate_cg([w1, w2, w3], [a1, a2, a3])
        st.success(f"מיקום מרכז הכובד מהציר: **{cg_result} ס\"מ**")

    with tab3:
        st.header("ניהול סוללות (LiPo)")
        s_count = st.slider("מספר תאים (S):", 1, 12, 6)
        st.table({
            "מצב": ["מתח נומינלי", "טעינה מלאה", "מתח אחסון (Storage)", "מתח פריקה מקסימלי"],
            "מתח כולל (V)": [s_count * 3.7, s_count * 4.2, s_count * 3.8, s_count * 3.5]
        })

    with tab4:
        st.header("מחשבון המרות מהיר")
        col_input, col_conv = st.columns(2)
        val = col_input.number_input("ערך להמרה:", value=1.0)
ctype = col_conv.selectbox('המרה:', ["מייל לק\"מ", "מטר לשנייה לקמ\"ש", "רגל למטר"])        result = convert_units(val, ctype)
        st.metric(f"תוצאה ({ctype.split(' ')[-1]})", result)

if __name__ == "__main__":
    main()
