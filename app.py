import streamlit as st
from google import genai
from google.genai import types
from PIL import Image
import io
import random

# =====================================================================
# 🟢 CUSTOMIZATION ZONE: THIS IS WHERE THE BRAND NAME IS SET
# =====================================================================
BRAND_NAME = "SecureDezy"  
PAGE_ICON = "🛡️"              

# Customize the phase progress labels
STAGE_1_TEXT = "1. Evidence Entry"
STAGE_2_TEXT = "2. AI Assessment"
STAGE_3_TEXT = "3. Adjuster Verification"
STAGE_4_TEXT = "4. Final Settlement"

# =====================================================================
# 🔴 CORE SYSTEM LOGIC: WORKFLOW AND AI INTEGRATION
# =====================================================================

st.set_page_config(page_title=f"{BRAND_NAME} AI Claims", page_icon=PAGE_ICON, layout="wide")

# Secure API Key Setup
# IMPORTANT: Put your real Gemini API key between the quotation marks below!
API_KEY = "YOUR_GEMINI_API_KEY_HERE"

client = None
if API_KEY and API_KEY != "YOUR_GEMINI_API_KEY_HERE":
    try:
        client = genai.Client(api_key=API_KEY)
    except Exception as e:
        st.error(f"Initialization Error: {e}")

# Initialize all the new business logic states
if "pipeline_stage" not in st.session_state:
    st.session_state.pipeline_stage = 1
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "selected_domain" not in st.session_state:
    st.session_state.selected_domain = "Vehicle Insurance"
if "vision_text" not in st.session_state:
    st.session_state.vision_text = ""
if "case_id" not in st.session_state:
    st.session_state.case_id = f"CLM-2026-{random.randint(1000, 9999)}"
if "quote_amount" not in st.session_state:
    st.session_state.quote_amount = f"₹{random.randint(15000, 85000):,}"
if "outcome" not in st.session_state:
    st.session_state.outcome = ""

# ✨ THE FIX: We moved the roster outside the IF statement so it never forgets the names!
broker_roster = ["Ramesh Kumar", "Priya Sharma", "Amit Patel", "Sneha Gupta", "Vikram Singh", "Anjali Desai", "Ravi Menon"]

if "broker_name" not in st.session_state:
    st.session_state.broker_name = random.choice(broker_roster)

with st.sidebar:
    st.title(f"{PAGE_ICON} {BRAND_NAME} Portal")
    st.markdown("---")
    
    previous_domain = st.session_state.selected_domain
    st.session_state.selected_domain = st.radio(
        "Select Policy Domain:",
        ["Vehicle Insurance", "Home Insurance"]
    )
    
    # If they change domains, reset the entire application and pick a new broker
    if previous_domain != st.session_state.selected_domain:
        st.session_state.pipeline_stage = 1
        st.session_state.chat_history = []
        st.session_state.vision_text = ""
        st.session_state.outcome = ""
        st.session_state.broker_name = random.choice(broker_roster)
        st.rerun()
        
    st.markdown("---")
    st.info(f"Active Framework: {st.session_state.selected_domain} Assessment Engine")

# Smart Logic Switcher. Changes wording based on Vehicle vs. Home
if st.session_state.selected_domain == "Vehicle Insurance":
    domain_context = "automobile accidents, dents, collisions, and vehicular structural degradation"
    vision_instruction = "Inspect this damage photo for a vehicle insurance claim. Provide a structured, objective bulleted breakdown of visible vehicular structural failure or collision indications."
    partner_title = "Authorized Mechanic Assigned"
    partner_desc = "A verified service partner from our authorized network garage in your area has been assigned to your case. The garage manager will contact you within the next 2 hours for a complete repair briefing and to schedule your vehicle drop-off or pickup."
    accept_btn_text = "🤝 Accept & Assign Garage"
else:
    domain_context = "residential property damages, water leakage, structural cracks, and fire/weather hazards"
    vision_instruction = "Inspect this damage photo for a residential property insurance claim. Provide a structured, objective bulleted breakdown of visible property damage, structural hazards, or affected residential areas."
    partner_title = "Network Restoration Contractor Assigned"
    partner_desc = "A verified contracting team from our home restoration network has been assigned to your property. The project manager will contact you within the next 2 hours to schedule an on-site repair briefing and material delivery timeline."
    accept_btn_text = "🤝 Accept & Assign Contractor"

system_rules = f"""
You are the interactive expert AI Claims Processor for {BRAND_NAME} Insurance specializing in {st.session_state.selected_domain}.
Your primary objective is to assist users in documenting a transparent new claim insurance file.
Please execute the following actions precisely:
1. Prompt the customer politely to provide the exact date, time, and geographic location of the event.
2. ONCE the user has provided the date, time, and location, you MUST explicitly instruct them to upload photographic evidence of the damage to the "Digital Evidence Vault" on the right side of their screen so you can begin the visual assessment.
3. Maintain an objective, analytical, and highly reassuring tone throughout the conversation.
"""

st.title(f"Automated Real-Time AI Claims Assistant")
st.subheader(f"Autonomous Evaluation Pipeline — Powered by Gemini")

progress_mapping = {1: 25, 2: 50, 3: 75, 4: 100}
current_progress = progress_mapping.get(st.session_state.pipeline_stage, 25)

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(f"**{STAGE_1_TEXT}**" if st.session_state.pipeline_stage == 1 else STAGE_1_TEXT)
with col2:
    st.markdown(f"**{STAGE_2_TEXT}**" if st.session_state.pipeline_stage == 2 else STAGE_2_TEXT)
with col3:
    st.markdown(f"**{STAGE_3_TEXT}**" if st.session_state.pipeline_stage == 3 else STAGE_3_TEXT)
with col4:
    st.markdown(f"**{STAGE_4_TEXT}**" if st.session_state.pipeline_stage == 4 else STAGE_4_TEXT)
st.progress(current_progress)

st.markdown("---")

welcome_msg = f"Welcome to the {BRAND_NAME} automated support center. Please describe the incident including date, time, and specific location to initiate your {st.session_state.selected_domain} claim valuation."

left_panel, right_panel = st.columns([1.2, 0.8])

# 💬 LEFT PANEL: The Chatbot
with left_panel:
    st.markdown("### 💬 Real-Time Claims Communication")
    
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.write(message["content"])
            
    if not st.session_state.chat_history:
        st.session_state.chat_history.append({"role": "assistant", "content": welcome_msg})
        st.rerun()

    if user_input := st.chat_input("Provide event details or answer AI questions here..."):
        with st.chat_message("user"):
            st.write(user_input)
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        
        if client:
            with st.chat_message("assistant"):
                response_placeholder = st.empty()
                response_placeholder.markdown("*Analyzing claim profile...*")
                
                try:
                    formatted_contents = []
                    for msg in st.session_state.chat_history:
                        if msg["content"] == welcome_msg:
                            continue
                            
                        gemini_role = "model" if msg["role"] == "assistant" else "user"
                        
                        if len(formatted_contents) == 0 or formatted_contents[-1].role != gemini_role:
                            formatted_contents.append(
                                types.Content(role=gemini_role, parts=[types.Part.from_text(text=msg["content"])])
                            )
                        else:
                            combined_text = formatted_contents[-1].parts[0].text + "\n" + msg["content"]
                            formatted_contents[-1] = types.Content(role=gemini_role, parts=[types.Part.from_text(text=combined_text)])
                    
                    ai_response = client.models.generate_content(
                        model='gemini-2.5-flash',
                        contents=formatted_contents,
                        config=types.GenerateContentConfig(
                            system_instruction=system_rules,
                            temperature=0.3
                        )
                    )
                    
                    final_text = ai_response.text
                    response_placeholder.markdown(final_text)
                    st.session_state.chat_history.append({"role": "assistant", "content": final_text})
                    
                    st.rerun()
                    
                except Exception as api_err:
                    st.error(f"Google API Error (Usually a 60-second speed limit): {api_err}")
                    st.session_state.chat_history.pop() # Removes your unsent message so you can try again
        else:
            st.warning("AI Node Offline: Connect a valid Google Gemini API Key in the application source script to enable execution.")


# 📁 RIGHT PANEL: The New Business Logic Pipeline
with right_panel:
    st.markdown("### 📁 Digital Evidence Vault")
    
    # STAGE 1: Uploading the image
    if st.session_state.pipeline_stage in [1, 2]:
        uploaded_image = st.file_uploader(
            "Upload photographic damage evidence (.png, .jpg, .jpeg)", 
            type=["png", "jpg", "jpeg"]
        )
        
        if uploaded_image:
            opened_image = Image.open(uploaded_image)
            st.image(opened_image, caption="Uploaded Claims Evidence Material", use_container_width=True)
            
            if st.session_state.pipeline_stage == 1 and client:
                try:
                    with st.spinner("🤖 AI Vision Module scanning structural damage..."):
                        img_byte_arr = io.BytesIO()
                        opened_image.save(img_byte_arr, format=opened_image.format if opened_image.format else 'JPEG')
                        img_bytes = img_byte_arr.getvalue()
                        
                        visual_analysis = client.models.generate_content(
                            model='gemini-2.5-flash',
                            contents=[
                                types.Part.from_bytes(data=img_bytes, mime_type=f"image/{opened_image.format.lower() if opened_image.format else 'jpeg'}"),
                                vision_instruction # Uses the smart prompt based on Car vs Home
                            ]
                        )
                        st.session_state.vision_text = visual_analysis.text
                        st.session_state.pipeline_stage = 2
                        st.rerun()
                except Exception as vision_err:
                    st.error(f"Google Vision API Error (Usually a 60-second speed limit): {vision_err}")

            # STAGE 2: User Verifies & Edits the AI's Description
            if st.session_state.pipeline_stage == 2:
                st.markdown("#### 🤖 Automated Assessment (Pending User Review)")
                
                edited_assessment = st.text_area(
                    "Review and edit the AI's assessment below. Add any missing details or context for the human adjuster:",
                    value=st.session_state.vision_text,
                    height=200
                )
                
                if st.button("✅ Lock Assessment & Request Human Adjuster"):
                    st.session_state.vision_text = edited_assessment 
                    st.session_state.pipeline_stage = 3
                    st.rerun()

    # STAGE 3: The Fraud Checkpoint, Broker Notice & Adjuster Call
    if st.session_state.pipeline_stage == 3:
        st.success(f"**Evidence Locked! Case ID:** {st.session_state.case_id}")
        st.markdown("### 🔒 Human Verification Required")
        
        st.warning(
            "**Fraud Prevention Protocol Active:** "
            "To ensure accuracy and protect our ecosystem, the AI engine does not issue automatic blind approvals. "
            "Your digital evidence has been securely locked and routed to our human Settlement Department."
        )
        
        st.success(
            f"🟢 **Claim Details Shared with Your Broker**\n\n"
            f"**Your Assigned Broker:** {st.session_state.broker_name}\n\n"
            f"The broker who facilitated your policy has been notified of this active claim. They have been securely provided with your locked photos and AI assessment. As your mediator, {st.session_state.broker_name.split()[0]} is tracking your file to ensure a smooth and fair settlement process with our underwriting team.\n\n"
            f"*Need guidance on how claims work before the adjuster calls? Contact your broker directly at **+91-98765-43210**.*"
        )
        
        st.info(
            "📞 **Priority Call Scheduled**\n\n"
            "An available claims adjuster is currently reviewing your uploaded photos and edited AI text. "
            "**You will receive a call on your registered mobile number shortly.** "
            "Once the adjuster confirms the details on the phone, they will digitally unlock your final quote here on the portal."
        )
        
        st.markdown("---")
        st.write("**Awaiting Adjuster Confirmation...**")
        st.write("*Once your phone verification is complete, click below to securely retrieve your final authorized quote.*")
        if st.button("🔄 Refresh Dashboard to View Quote"):
            st.session_state.pipeline_stage = 4
            st.rerun()

    # STAGE 4: Final Settlement Decision
    if st.session_state.pipeline_stage == 4:
        st.markdown("### 💰 Official Settlement Offer")
        st.write("Following your adjuster phone verification, your final repair approval quote has been unlocked:")
        st.metric(label="Verified Payout Quote:", value=st.session_state.quote_amount)
        
        if st.session_state.outcome == "":
            st.write("**How would you like to proceed with this verified offer?**")
            colA, colB = st.columns(2)
            with colA:
                if st.button(accept_btn_text): # Uses dynamic button text
                    st.session_state.outcome = "accepted"
                    st.rerun()
            with colB:
                if st.button("⚖️ Reject Quote & Escalate"):
                    st.session_state.outcome = "escalated"
                    st.rerun()

        # The End Result (Cashless Garage vs Legal Rights)
        if st.session_state.outcome == "accepted":
            st.markdown("---")
            st.success(f"🎉 **Claim Successfully Approved!** You accepted the repair quote of {st.session_state.quote_amount}.")
            
            st.write(f"*Note: This evaluation represents the fair repair amount deemed accurate after our surveyor's inspection of your evidence, applying standard depreciation and regional labor rates.*")
            
            st.write("The Claims Department has authorized the repairs under our Cashless Network.")
            
            # Uses the smart logic to assign a Mechanic OR a Contractor
            st.info(f"🛠️ **{partner_title}**\n\n{partner_desc}")
            st.balloons()
        
        elif st.session_state.outcome == "escalated":
            st.markdown("---")
            st.error("⚠️ Settlement Rejected – Arbitration Protocol Active")
            
            st.write("You have officially rejected the human adjuster's verified quote. Automated processing is now paused, and your case requires manual review.")
            
            st.success(
                f"🤝 **Broker Intervention Recommended**\n\n"
                f"Before filing a formal legal dispute, we highly recommend consulting your assigned broker, **{st.session_state.broker_name}**. "
                f"As your mediator, {st.session_state.broker_name.split()[0]} can step in to negotiate directly with the underwriting team on your behalf or help you review the surveyor's calculations.\n\n"
                f"📞 **Call {st.session_state.broker_name.split()[0]} directly at +91-98765-43210**"
            )
            
            st.warning(
                "🏢 **Need further help understanding your quote?**\n\n"
                "You can also speak directly with a Senior Escalation Manager. "
                "Call our priority helpline at **1800-258-0000 (Extension: 9)** and provide your Case ID."
            )
            
            st.markdown("#### ⚖️ Know Your Consumer Rights")
            st.write("As per standard Indian insurance regulations, please review your statutory rights while your case is escalated:")
            st.markdown("""
            * **Independent Property Surveyor / Engineer:** Under IRDAI guidelines, you may request a secondary inspection by an independent surveyor if you disagree with the company's evaluation.
            * **Detailed Calculation Request:** You are legally entitled to request an itemized breakdown of depreciation and labor costs applied to your quote.
            * **Insurance Ombudsman:** If a resolution cannot be reached within 30 days, you retain the absolute right to file a formal grievance with the regional Insurance Ombudsman.
            """)