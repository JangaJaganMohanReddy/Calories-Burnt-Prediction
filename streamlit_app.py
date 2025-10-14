import streamlit as st
import pandas as pd
import joblib
import time

# Page configuration
st.set_page_config(
    page_title="Calories Burnt Predictor",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for animations and styling
st.markdown("""
    <style>
    /* Animated Background */
    .stApp {
        background: linear-gradient(-45deg, #ee7752, #e73c7e, #23a6d5, #23d5ab);
        background-size: 400% 400%;
        animation: gradientBG 15s ease infinite;
    }
    
    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Floating particles effect */
    .stApp::before {
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: 
            radial-gradient(circle, rgba(255, 255, 255, 0.1) 1px, transparent 1px),
            radial-gradient(circle, rgba(255, 255, 255, 0.15) 1px, transparent 1px);
        background-size: 50px 50px, 80px 80px;
        background-position: 0 0, 40px 40px;
        animation: particleFloat 20s linear infinite;
        pointer-events: none;
        z-index: 0;
    }
    
    @keyframes particleFloat {
        0% { transform: translateY(0); }
        100% { transform: translateY(-100px); }
    }
    
    /* Make content visible over background */
    .main .block-container {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        position: relative;
        z-index: 1;
    }
    
    /* Animated gradient background for title */
    .main-title {
        background: linear-gradient(45deg, #FF6B6B, #4ECDC4, #45B7D1, #FFA07A);
        background-size: 300% 300%;
        animation: gradient 5s ease infinite;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        padding: 20px;
    }
    
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Pulse animation for buttons */
    .stButton>button {
        animation: pulse 2s infinite;
        background: linear-gradient(45deg, #FF6B6B, #4ECDC4);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 15px 30px;
        font-size: 18px;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 5px 15px rgba(0,0,0,0.3);
    }
    
    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(78, 205, 196, 0.7); }
        70% { box-shadow: 0 0 0 10px rgba(78, 205, 196, 0); }
        100% { box-shadow: 0 0 0 0 rgba(78, 205, 196, 0); }
    }
    
    /* Fade in animation for content */
    .fade-in {
        animation: fadeIn 1s ease-in;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* Card styling with hover effect */
    .info-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: transform 0.3s ease;
        margin: 10px 0;
    }
    
    .info-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.2);
    }
    
    /* Tips card styling */
    .tips-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin: 15px 0;
        color: white;
    }
    
    .tips-card h3 {
        color: white !important;
        margin-bottom: 15px;
    }
    
    .tips-card ul {
        list-style-type: none;
        padding-left: 0;
    }
    
    .tips-card li {
        padding: 8px 0;
        border-bottom: 1px solid rgba(255,255,255,0.2);
    }
    
    .tips-card li:last-child {
        border-bottom: none;
    }
    
    /* Animated icons */
    .icon-bounce {
        animation: bounce 2s infinite;
        display: inline-block;
    }
    
    @keyframes bounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-10px); }
    }
    
    /* Progress bar animation */
    .stProgress > div > div {
        background: linear-gradient(90deg, #FF6B6B, #4ECDC4, #45B7D1);
        background-size: 200% 100%;
        animation: loading 2s linear infinite;
    }
    
    @keyframes loading {
        0% { background-position: 0% 0%; }
        100% { background-position: 200% 0%; }
    }
    
    /* Sidebar styling with glassmorphism */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(102, 126, 234, 0.9) 0%, rgba(118, 75, 162, 0.9) 100%);
        backdrop-filter: blur(10px);
        border-right: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    [data-testid="stSidebar"] > div:first-child {
        background: transparent;
    }
    
    /* Style sidebar text */
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    
    /* Success message animation */
    .success-message {
        animation: slideInRight 0.5s ease-out;
        background: linear-gradient(45deg, #11998e, #38ef7d);
        padding: 20px;
        border-radius: 10px;
        color: white;
        font-size: 1.5rem;
        font-weight: bold;
        text-align: center;
        margin: 20px 0;
    }
    
    @keyframes slideInRight {
        from { transform: translateX(100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    </style>
""", unsafe_allow_html=True)

# Function to load the model
@st.cache_data
def load_model():
    with open('calories_model', 'rb') as file:
        loaded_model = joblib.load(file)
    return loaded_model

# Function to calculate BMI and determine weight category
def calculate_bmi_category(weight, height):
    height_m = height / 100
    bmi = weight / (height_m ** 2)
    
    if bmi < 18.5:
        return bmi, "Underweight", "gain"
    elif 18.5 <= bmi < 25:
        return bmi, "Normal Weight", "maintain"
    elif 25 <= bmi < 30:
        return bmi, "Overweight", "loss"
    else:
        return bmi, "Obese", "loss"

# Function to get personalized tips based on weight goal
def get_personalized_tips(calories_burnt, duration, weight, height, age, gender, exercise_type):
    bmi, bmi_category, goal = calculate_bmi_category(weight, height)
    cal_per_min = calories_burnt / duration
    
    if calories_burnt < 200:
        intensity = "Low"
    elif calories_burnt < 400:
        intensity = "Moderate"
    else:
        intensity = "High"
    
    exercise_tips = {
        'Running': "🏃 Great cardio choice! Try interval training to boost calorie burn.",
        'Cycling': "🚴 Excellent low-impact option! Increase resistance for more intensity.",
        'Swimming': "🏊 Full-body workout! Perfect for joint health and endurance.",
        'Walking': "🚶 Perfect for beginners! Increase pace or add inclines for progression.",
        'Weight Training': "🏋️ Building muscle increases resting metabolism! Focus on compound movements.",
        'Yoga': "🧘 Great for flexibility and mindfulness! Try power yoga for more calorie burn.",
        'HIIT': "⚡ Maximum calorie burn! Ensure proper rest between sessions.",
        'Dancing': "💃 Fun and effective! Increase tempo for higher intensity.",
        'Sports': "⚽ Team sports keep you motivated! Great for overall fitness.",
        'Other': "💪 Keep up the good work! Consistency is key to results."
    }
    
    if goal == "gain":
        workout_tips = [
            f"🎯 {exercise_tips.get(exercise_type, exercise_tips['Other'])}",
            "🍗 **Increase Caloric Intake**: Consume 300-500 calories more than you burn daily",
            "🏋️ **Focus on Strength Training**: Build muscle mass with resistance exercises",
            "💪 **Progressive Overload**: Gradually increase weights to build strength",
            "🥛 **Protein Rich Diet**: Aim for 1.6-2.2g protein per kg body weight"
        ]
        general_tips = [
            "🍽️ **Eat More Frequently**: Have 5-6 smaller meals throughout the day",
            "🥜 **Nutrient Dense Foods**: Include nuts, avocados, whole grains, and lean meats",
            "🥤 **Weight Gainer Shakes**: Consider healthy smoothies with protein powder",
            "😴 **Adequate Sleep**: Get 8-9 hours for muscle recovery and growth",
            "📊 **Track Calories**: Ensure you're in a caloric surplus consistently"
        ]
        goal_message = "🎯 Your Goal: Healthy Weight Gain"
        
    elif goal == "maintain":
        workout_tips = [
            f"🎯 {exercise_tips.get(exercise_type, exercise_tips['Other'])}",
            "✅ **Great Work**: Your BMI is in the healthy range! Focus on maintenance",
            "🔄 **Balanced Routine**: Mix cardio and strength training equally",
            "💪 **Build Muscle**: Focus on toning and building lean muscle mass",
            "📈 **Challenge Yourself**: Gradually increase intensity to stay engaged"
        ]
        general_tips = [
            "⚖️ **Caloric Balance**: Match your calorie intake with calories burnt",
            "🥗 **Balanced Diet**: Include all food groups in appropriate portions",
            "💧 **Stay Hydrated**: Drink 8-10 glasses of water daily",
            "🧘 **Flexibility & Mobility**: Add yoga or stretching to your routine",
            "🏃 **Active Lifestyle**: Stay active throughout the day, not just during workouts"
        ]
        goal_message = "🎯 Your Goal: Maintain Healthy Weight"
        
    else:
        if intensity == "Low":
            workout_tips = [
                f"🎯 {exercise_tips.get(exercise_type, exercise_tips['Other'])}",
                "💪 **Increase Intensity**: Gradually boost your workout intensity to burn more calories",
                "⏱️ **Extend Duration**: Add 15-20 more minutes to your workout session",
                "🏃 **Add HIIT**: Include high-intensity interval training 2-3 times per week",
                "🎯 **Set Targets**: Aim to burn at least 300-500 calories per workout"
            ]
        elif intensity == "Moderate":
            workout_tips = [
                f"🎯 {exercise_tips.get(exercise_type, exercise_tips['Other'])}",
                "👍 **Good Progress**: You're on the right track! Keep the momentum",
                "🚴 **Mix It Up**: Try different activities to challenge your body",
                "💧 **Stay Hydrated**: Proper hydration boosts metabolism",
                "🏋️ **Add Weights**: Include resistance training to build muscle and burn more"
            ]
        else:
            workout_tips = [
                f"🎯 {exercise_tips.get(exercise_type, exercise_tips['Other'])}",
                "🌟 **Excellent Effort**: You're burning significant calories! Keep it up!",
                "🍎 **Fuel Properly**: Ensure adequate nutrition for high-intensity workouts",
                "😴 **Recovery Matters**: Rest 1-2 days per week to prevent burnout",
                "📈 **Avoid Plateaus**: Change your routine every 4-6 weeks"
            ]
        
        general_tips = [
            "🍽️ **Calorie Deficit**: Create a deficit of 500-750 calories daily for healthy loss",
            "🌙 **Quality Sleep**: Get 7-9 hours to support metabolism and recovery",
            "🚫 **Cut Processed Foods**: Reduce sugar, refined carbs, and processed foods",
            "📱 **Use Apps**: Track calories and macros with fitness apps",
            "👥 **Get Support**: Join a fitness group or find a workout buddy"
        ]
        goal_message = "🎯 Your Goal: Healthy Weight Loss"
    
    return intensity, workout_tips, general_tips, bmi, bmi_category, goal_message

# Load your model
loaded_model = load_model()

# Animated sidebar
st.sidebar.markdown('<h1 class="icon-bounce">🔥</h1>', unsafe_allow_html=True)
st.sidebar.title('Navigation')
options = st.sidebar.selectbox('Select a page:', 
                           ['Prediction', 'Code', 'About'])

if options == 'Prediction':
    st.markdown('<h1 class="main-title">Calories Burnt Prediction 🔥</h1>', unsafe_allow_html=True)
    
    st.markdown('<div class="fade-in">', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("👤 Personal Information")
        gender = st.selectbox('Gender', ['Male','Female'])
        age = st.number_input('Age', 1, 100, 25)
        height = st.number_input('Height (cm)', 100, 250, 170)
        weight = st.number_input('Weight (kg)', 30, 200, 70)
    
    with col2:
        st.subheader("🏃 Exercise Metrics")
        exercise_type = st.selectbox('Type of Exercise', 
                                     ['Running', 'Cycling', 'Swimming', 'Walking', 
                                      'Weight Training', 'Yoga', 'HIIT', 'Dancing', 
                                      'Sports', 'Other'])
        duration = st.number_input('Duration (minutes)', 1, 180, 60)

    st.markdown('</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        predict_button = st.button('🔮 Predict Calories Burnt', use_container_width=True)
    
    if predict_button:
        with st.spinner('🔄 Calculating your calories burnt...'):
            progress_bar = st.progress(0)
            for i in range(100):
                time.sleep(0.01)
                progress_bar.progress(i + 1)
            
            # Using default values for heart_rate and body_temp
            user_inputs = {
                'gender': 0 if gender == 'Male' else 1,
                'age': age,
                'height': height,
                'weight': weight,
                'duration': duration,
                'heart_rate': 100,  # Default value
                'body_temp': 37.0   # Default value
            }
            
            prediction = loaded_model.predict(pd.DataFrame(user_inputs, index=[0]))
            
        progress_bar.empty()
        
        st.markdown(f'''
            <div class="success-message">
                🎉 Predicted Calories Burnt: {prediction[0]:,.2f} kcal
            </div>
        ''', unsafe_allow_html=True)
        
        st.balloons()
        
        intensity, workout_tips, general_tips, bmi, bmi_category, goal_message = get_personalized_tips(
            prediction[0], duration, weight, height, age, gender, exercise_type
        )
        
        st.markdown("---")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Your BMI", f"{bmi:.1f}", help="Body Mass Index")
        with col2:
            bmi_color = "🟢" if bmi_category == "Normal Weight" else "🟡" if bmi_category in ["Underweight", "Overweight"] else "🔴"
            st.metric("Category", f"{bmi_color} {bmi_category}")
        with col3:
            st.metric("Workout Intensity", f"⚡ {intensity}")
        with col4:
            st.metric("Exercise Type", f"💪 {exercise_type}")
        
        st.markdown(f"### {goal_message}")
        
        st.markdown("### 💡 Personalized Fitness Tips")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown(f"""
                <div class="tips-card">
                    <h3>🎯 Workout Tips for Your Goal</h3>
                    <ul>
                        {''.join([f'<li>{tip}</li>' for tip in workout_tips])}
                    </ul>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
                <div class="tips-card">
                    <h3>🌟 Nutrition & Lifestyle Tips</h3>
                    <ul>
                        {''.join([f'<li>{tip}</li>' for tip in general_tips])}
                    </ul>
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("### 📊 Quick Weight Loss Stats")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            days_to_lose_1lb = round(3500 / prediction[0], 1)
            st.metric("Days to Lose 1 lb", f"{days_to_lose_1lb} days", 
                     help="At this burn rate, doing same workout daily")
        
        with col2:
            weekly_burn = round(prediction[0] * 7, 2)
            st.metric("Weekly Burn", f"{weekly_burn:,.0f} kcal",
                     help="If you maintain this workout 7 days/week")
        
        with col3:
            monthly_loss = round((prediction[0] * 30) / 3500, 1)
            st.metric("Monthly Loss", f"{monthly_loss} lbs",
                     help="Potential weight loss in 30 days")
        
        with col4:
            cal_per_min = round(prediction[0] / duration, 2)
            st.metric("Burn Rate", f"{cal_per_min} kcal/min",
                     help="Calories burnt per minute")
        
        with st.expander("📊 Show Detailed Analysis"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric("Exercise", exercise_type, "💪")
            with col2:
                st.metric("Duration", f"{duration} min", "⏱️")
            
            st.write("---")
            st.write("**Model Details:**")
            st.info("🤖 Model: Random Forest Regressor\n\n📈 Trained on 15,000 samples")
            
            st.write("**Your Input Summary:**")
            input_df = pd.DataFrame([user_inputs])
            input_df['gender'] = 'Male' if user_inputs['gender'] == 0 else 'Female'
            input_df['exercise_type'] = exercise_type
            st.dataframe(input_df, use_container_width=True)

elif options == 'Code':
    st.markdown('<h1 class="main-title">📝 Code & Resources</h1>', unsafe_allow_html=True)
    
    st.markdown('<div class="fade-in">', unsafe_allow_html=True)
    with st.container():
        st.header('📓 Jupyter Notebook')
        st.write('Download the complete notebook with model building process and analysis.')
        
        try:
            notebook_path = 'calories_burnt_prediction.ipynb'
            with open(notebook_path, "rb") as file:
                st.download_button(
                    label="⬇️ Download Jupyter Notebook",
                    data=file,
                    file_name="calories_burnt_prediction.ipynb",
                    mime="application/x-ipynb+json",
                    use_container_width=True
                )
        except FileNotFoundError:
            st.warning("⚠️ Notebook file not found!")
    
    st.write('---')
    
    with st.container():
        st.header('📊 Dataset')
        st.write('Download the dataset used for training the model.')
        
        try:
            data_path = 'calories_data.csv'
            with open(data_path, "rb") as file:
                st.download_button(
                    label="⬇️ Download Dataset (CSV)",
                    data=file,
                    file_name="calories_data.csv",
                    mime="text/csv",
                    use_container_width=True
                )
        except FileNotFoundError:
            st.warning("⚠️ Dataset file not found!")
    
    st.write('---')
    
    with st.container():
        st.header('💻 GitHub Repository')
        st.write('Access the complete source code and documentation:')
        st.markdown('''
            <div class="info-card">
                <a href="https://github.com/JangaJaganMohanReddy/Calories-Burnt-Prediction" 
                   target="_blank" style="color: white; text-decoration: none; font-size: 1.2rem;">
                    🔗 View on GitHub →
                </a>
            </div>
        ''', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
elif options == 'About':
    st.markdown('<h1 class="main-title">ℹ️ About This App</h1>', unsafe_allow_html=True)
    
    st.markdown('<div class="fade-in">', unsafe_allow_html=True)
    
    with st.container():
        st.header('🎯 Project Overview')
        st.write('''
        This web application predicts calories burnt during exercise based on various physiological 
        and exercise parameters. Using machine learning, it provides accurate predictions to help 
        you track your fitness journey.
        ''')
    
    st.write('---')
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader('🤖 Model Details')
        st.info('''
        **Algorithm:** Random Forest Regressor
        
        **Training Data:** 15,000 samples
        
        **Features:** 7 input parameters
        ''')
    
    with col2:
        st.subheader('📊 Dataset Source')
        st.info('''
        **Source:** Kaggle Dataset
        
        **Link:** [FMendes Dataset](https://www.kaggle.com/datasets/fmendes/fmendesdat263xdemos)
        ''')
    
    st.write('---')
    
    st.header('📬 Contact Information')
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('''
            <div class="info-card">
                <h3>📧 Email</h3>
                <p>jaganjanga06@gmail.com</p>
            </div>
        ''', unsafe_allow_html=True)
    
    with col2:
        st.markdown('''
            <div class="info-card">
                <h3>💼 LinkedIn</h3>
                <a href="https://www.linkedin.com/in/j-m-reddy-447097314/" 
                   target="_blank" style="color: white;">
                    Connect with me →
                </a>
            </div>
        ''', unsafe_allow_html=True)
    
    st.write('---')
    
    st.header('⭐ Open Source')
    st.markdown('''
        <div class="info-card">
            <h3>💻 GitHub Repository</h3>
            <p>This project is open-source! Feel free to contribute, report issues, or fork the repository.</p>
            <a href="https://github.com/JangaJaganMohanReddy/Calories-Burnt-Prediction" 
               target="_blank" style="color: white; text-decoration: none;">
                🔗 View Repository →
            </a>
        </div>
    ''', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('---')
st.markdown('''
    <div style="text-align: center; color: #888; padding: 20px;">
        <p>Made with ❤️ by Jagan Mohan Reddy | © 2024</p>
    </div>
''', unsafe_allow_html=True)