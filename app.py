import nltk
import streamlit as st
import pickle
import string
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import time

# Download required NLTK data
nltk.download('punkt')
nltk.download('stopwords')

# Initialize Porter Stemmer
ps = PorterStemmer()

# Text transformation function
def transform_text(text):
    text = text.lower()
    text = nltk.word_tokenize(text)
    y = []
    for i in text:
        if i.isalnum():
            y.append(i)
    text = y[:]
    y.clear()
    for i in text:
        if i not in stopwords.words('english') and i not in string.punctuation:
            y.append(i)
    text = y[:]
    y.clear()
    for i in text:
        y.append(ps.stem(i))
    return " ".join(y)

# Load models
tk = pickle.load(open("vectorizer.pkl", 'rb'))
model = pickle.load(open("model.pkl", 'rb'))

# Page configuration
st.set_page_config(
    page_title="SMS Spam Detective 🕵️",
    page_icon="🔍",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 2rem;
        border-radius: 10px;
    }
    .stTextInput > div > div > input {
        border-radius: 10px;
    }
    .stButton>button {
        border-radius: 20px;
        padding: 1rem 2rem;
        font-weight: bold;
    }
    .spam-result {
        padding: 20px;
        border-radius: 10px;
        margin: 20px 0;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.sidebar.image("https://cdn-icons-png.flaticon.com/512/2471/2471610.png", width=150)
    st.title("About 📱")
    st.info("""
    This SMS Spam Detective helps you identify unwanted spam messages using advanced machine learning.
    
    How to use:
    1. Enter your SMS text 📝
    2. Click Analyze ✨
    3. Get instant results! 🎯
    """)

# Main content
st.title("SMS Spam Detective 🕵️‍♂️")
st.markdown("### Your Guardian Against Unwanted Messages ✨")

# Input section with animation
input_sms = st.text_area("📝 Enter your message here", height=100,
    placeholder="Type or paste your SMS message here...")

col1, col2, col3 = st.columns([1,2,1])
with col2:
    if st.button("🔍 Analyze Message", use_container_width=True):
        if input_sms:
            # Add a spinner during processing
            with st.spinner("🔄 Analyzing your message..."):
                time.sleep(1)  # Artificial delay for effect
                
                # Process the message
                transformed_sms = transform_text(input_sms)
                vector_input = tk.transform([transformed_sms])
                result = model.predict(vector_input)[0]
                
                # Display result with animation
                if result == 1:
                    st.error("🚨 SPAM DETECTED! 🚨")
                    st.markdown("""
                        <div class='spam-result' style='background-color: #FFE0E0;'>
                            <h2>⚠️ This message appears to be SPAM</h2>
                            <p>Be careful with this message. It might be attempting to deceive you.</p>
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    st.success("✅ LEGITIMATE MESSAGE")
                    st.markdown("""
                        <div class='spam-result' style='background-color: #E0FFE0;'>
                            <h2>✨ This message appears to be legitimate</h2>
                            <p>The message looks safe and genuine.</p>
                        </div>
                    """, unsafe_allow_html=True)
                
                # Show confidence score
                confidence = model.predict_proba(vector_input)[0]
                st.markdown("### Confidence Analysis 📊")
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Spam Probability", f"{confidence[1]:.2%}")
                with col2:
                    st.metric("Ham Probability", f"{confidence[0]:.2%}")
        else:
            st.warning("⚠️ Please enter a message to analyze")

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center'>
        <p>Made with ❤️ by Anil Kumawat</p>
        <p>Protecting your inbox, one message at a time 🛡️</p>
    </div>
""", unsafe_allow_html=True)
