import streamlit as st

# --- פונקציות עזר (Business Logic) ---

def calculate_safety_distance(target_type):
    """מחזיר את מרחק ההפרדה הנדרש לפי תקנות רת"א"""
    distances = {
        "אדם בודד / מבנה / רכב": 50,
        "התקהלות בני אדם (מעל 30 איש)": 250,
        "שדה תעופה אזרחי": 2000
    }
    return distances.get(target_type, 50)

def calculate_drone_performance(base_mtow, current_temp):
    """חישוב משקל המראה בטוח בהתאם לרום צפיפות (טמפרטורה)"""
    standard_temp = 15
    if current_temp <= standard_temp:
        return base_mtow
    # איבוד של 0.3% לכל מעלה מעל 15 מעלות צלזיוס
    loss_factor = 0.003
    temp_diff = current_temp - standard_temp
    recommended_mtow = base_mtow * (1 - (temp_diff * loss_factor))
    return round(recommended_mtow, 2)

def troubleshoot_drone(issue):
    """מערכת מומחה לדיאגנוסטיקה של תקלות בכטב"ם"""
    knowledge_base = {
        "רעידות חריגות": "בדוק איזון פרופלורים, הידוק מנועים לשלדה, וודא שאין סדקים בזרועות.",
        "סטייה מהנתיב (Drift)": "בצע כיול מצפן (Compass) הרחק ממקורות מתכת, ובדוק קליטת לוויינים.",
        "התחממות סוללה": "בדוק אם המשקל (MTOW) חורג מהמותר לטמפרטורה, או אם הסוללה ישנה.",
        "רעש שריקה מהמנועים": "בדוק חדירת גופים זרים למנוע או שחיקה של המיסבים (Bearings).",
        "ניתוקי וידאו": "בדוק תקינות אנטנות (Downlink) וודא שאין חסימה בקו הראייה (VLOS)."
    }
    return knowledge_base.get(issue, "תקלה לא מוכרת. מומלץ לנחות ולבצע בדיקה מקיפה.")

# --- ממשק המשתמש (Streamlit UI) ---

def main():
    st.set_page_config(page_title="Drone AI Expert Pro", page_icon="🚁", layout="wide")
    
    st.title("🚁 Drone AI Expert - Pro Edition (Up to 25kg)")
    st.markdown("---")

    # סרגל צדדי - Checklist
    st.sidebar.header("✅ בדיקות לפני המראה")
    steps = [
        "בדיקת שלדה וברגים", "פרופלורים תקינים", 
        "סוללות נעולות", "נעילת GPS (10+)", 
        "מרחקי הפרדה (50/250מ')", "שטח המראה פנוי"
    ]
    completed = [st.sidebar.checkbox(step) for step in steps]
    
    if all(completed):
        st.sidebar.success("Ready for Takeoff! 🚀")
    else:
        st.sidebar.warning("השלם רשימת תיוג")

    # פריסה ראשית
    col1, col2 = st.columns(2)

    with col1:
        st.header("📋 תכנון ובטיחות")
        target = st.selectbox("סביבת ההטסה:", 
                             ["אדם בודד / מבנה / רכב", "התקהלות בני אדם (מעל 30 איש)", "שדה תעופה אזרחי"])
        dist = calculate_safety_distance(target)
        st.info(f"מרחק הפרדה נדרש: **{dist} מטרים**")
        
        st.subheader("🔋 נתוני מתח (סוללה)")
        s_count = st.number_input("מספר תאים (S):", 1, 12, 6)
        st.write(f"מתח נומינלי: **{s_count * 3.7:.1f}V** | אחסון: **{s_count * 3.8:.1f}V**")

    with col2:
        st.header("🌡️ חישובי ביצועים")
        mtow = st.number_input("משקל המראה יצרן (ק\"ג):", value=20.0)
        temp = st.slider("טמפרטורה (°C):", 0, 50, 25)
        safe_weight = calculate_drone_performance(mtow, temp)
        
        loss_pct = ((mtow - safe_weight) / mtow) * 100
        st.metric("משקל המראה בטוח מומלץ", f"{safe_weight} ק\"ג", f"-{loss_pct:.1f}%")

    st.markdown("---")
    st.header("🛠️ מערכת אבחון תקלות")
    issue = st.selectbox("זהית תקלה? בחר סימפטום:", ["-- בחר --"] + list(troubleshoot_drone("").split("\n"))) # תיקון קל לדינמיות
    # לשיפור ה-Selectbox נשתמש ברשימה קשיחה:
    issue = st.selectbox("בחר סימפטום לניתוח:", 
                        ["-- בחר --", "רעידות חריגות", "סטייה מהנתיב (Drift)", "התחממות סוללה", "רעש שריקה מהמנועים", "ניתוקי וידאו"])
    
    if issue != "-- בחר --":
        st.error(f"**המלצת המערכת:** {troubleshoot_drone(issue)}")

if __name__ == "__main__":
    main()
