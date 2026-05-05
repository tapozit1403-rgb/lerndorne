import streamlit as st

# --- פונקציות ליבה על בסיס נתוני המצגת והרגולציה ---

def get_regulation_data(category):
    """נתונים רשמיים מתוך חוקת הטיס ונהלי רת"א"""
    data = {
        "מרחקי הפרדה": {
            "אדם / מבנה / רכב / כביש": "50 מטר",
            "התקהלות בני אדם (מעל 30 איש)": "250 מטר [הנחיית רת\"א מעודכנת]", # על פי תיקון המשתמש
            "גבול שדה תעופה / מנחת": "2 קילומטר (כפוף לאישור CTR)",
            "גובה טיסה מקסימלי": "120 מטר (400 רגל) מעל פני השטח (AGL)"
        },
        "טכני וסוללות": {
            "מתח תא נומינלי": "3.7V",
            "מתח טעינה מקסימלי": "4.2V",
            "מתח פריקה מינימלי (בטיחות)": "3.5V",
            "מתח אחסון (Storage)": "3.8V - 3.85V"
        }
    }
    return data.get(category, {})

def calculate_density_altitude_impact(temp, mtow):
    """חישוב השפעת רום צפיפות על ביצועי המראה (מטאורולוגיה)"""
    # סטנדרט ISA הוא 15 מעלות. בישראל הטמפרטורה לרוב גבוהה יותר.
    if temp <= 15:
        return mtow, 0
    
    # כלל אצבע: ירידה של כ-0.3% בביצועים על כל מעלה מעל הסטנדרט
    penalty_factor = (temp - 15) * 0.003
    safe_weight = mtow * (1 - penalty_factor)
    return round(safe_weight, 2), round(penalty_factor * 100, 1)

# --- ממשק המשתמש (Streamlit UI) ---

def main():
    st.set_page_config(page_title="Drone AI Expert - Exam Ready", page_icon="🎓", layout="wide")
    
    st.title("🚁 Drone AI Expert Pro - הכנה למבחן רת\"א (עד 25 ק\"ג)")
    st.write("מערכת עזר המבוססת על נתוני המצגת וסימולציות המבחן")
    st.divider()

    # סרגל צד - בדיקות חובה (Checklist) לפי סע"מ
    st.sidebar.header("📋 רשימת תיוג לפני המראה")
    safety_checks = [
        "בדיקת שלדה, זרועות ומנועים",
        "פרופלורים - בדיקת סדקים ואיזון",
        "סוללה - בדיקת מתח תאים וחיבורים",
        "קליטת GPS - לפחות 10 לוויינים",
        "וידוא VLOS (קשר עין ישיר)",
        "בדיקת NOTAM ואזורים אסורים (AIP)"
    ]
    for check in safety_checks:
        st.sidebar.checkbox(check)

    # חלק 1: חוקה ותקנות
    st.header("⚖️ חוקה ותקנות (מרחקי הפרדה)")
    reg_data = get_regulation_data("מרחקי הפרדה")
    
    cols = st.columns(len(reg_data))
    for i, (key, value) in enumerate(reg_data.items()):
        cols[i].metric(label=key, value=value)
    
    st.warning("אי שמירה על מרחק של 250 מטר מהתקהלות היא עבירה על תקנות המטיס!")

    st.divider()

    # חלק 2: מטאורולוגיה וביצועים
    st.header("🌤️ מטאורולוגיה וביצועי כלי טיס")
    c1, c2 = st.columns(2)
    
    with c1:
        base_weight = st.number_input("משקל המראה מקסימלי יצרן (MTOW) בק\"ג:", value=20.0, step=0.5)
        temp_input = st.slider("טמפרטורה חיצונית (°C):", 0, 50, 25)
    
    with c2:
        safe_wt, loss_pct = calculate_density_altitude_impact(temp_input, base_weight)
        st.metric("משקל המראה בטוח מומלץ", f"{safe_wt} ק\"ג", f"-{loss_pct}% ביצועים")
        st.info("רום צפיפות גבוה (אוויר חם) מפחית את העילוי ומחייב הפחתת משקל.")

    st.divider()

    # חלק 3: מערכת אבחון תקלות (טכני)
    st.header("🛠️ דיאגנוסטיקה ותחזוקה")
    issue = st.selectbox("זהית תקלה או התנהגות חריגה?", 
                        ["-- בחר סימפטום --", "רעידות חריגות", "סטייה מהנתיב (Drift)", 
                         "נפילת מתח חריגה בעומס", "איבוד קשר (Failsafe)"])
    
    if issue == "נפילת מתח חריגה בעומס":
        st.error("אבחנה: תא פגום בסוללה או התנגדות פנימית גבוהה. חובה לנחות מיד!")
    elif issue == "רעידות חריגות":
        st.error("אבחנה: בעיה באיזון פרופלורים או מנוע רופף. סכנת כשל מבני.")
    elif issue == "סטייה מהנתיב (Drift)":
        st.error("אבחנה: שגיאת מצפן (Compass) או הפרעה אלקטרומגנטית. עבור למצב ATTI.")
    elif issue == "איבוד קשר (Failsafe)":
        st.success("פעולה: וודא גובה RTH מוגדר מעל מכשולים. הכלי יבצע חזרה הביתה או נחיתה.")

if __name__ == "__main__":
    main()
