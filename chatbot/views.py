from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import difflib  # For fuzzy matching

@csrf_exempt
def chat_response(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_message = data.get("message", "").strip().lower()  # Normalize input

            # Case-insensitive response dictionary with more variations
            responses = {
                 "hi": "How can I help you?😊",
                "Tell me the OPD Timings": "our OPD is open from 9 AM to AM, Monday to Saturday😊",
                "Where is the hospital Located?": "Shivaratna Nagar, Gopalpur, Pandharpur😊",
                "hello": "Hello! How can I assist you?😊",
                "hii": "Hi there! What can I do for you?😊",
                "hey": "Hey! Need any help?😊",
                "how are you?": "I'm just a bot, but I'm doing great!✌ How can I help you?",
                "tell about the hospital": "Matoshree Hospital is a multi-specialty hospital offering expert care in various medical fields.🏥",
                "how can i book appointment": "You can book an appointment by visiting our 'Appointment' page and filling in the required details.📝",
                "What can you do?": "I can provide information about Matoshree Hospital, help with appointment booking, and answer basic queries.😇",
                 "Tell me a Joke": "Why did the doctor carry a red pen? In case they needed to draw blood! 😂",
                 "Who made you?": " I was created to assist users with hospital-related queries and provide helpful information!",
                 "Thanks": "Happy to help!😀",
                 "Thank You": "My Pleasure!😀",
                 "good morning": "Good morning! Welcome to Matoshree Hospital. How may I assist you? ☀️",
                "good afternoon": "Good afternoon! How can I help you with our healthcare services? 🌞",
                 "good evening": "Good afternoon! How can I help you with our healthcare services? 🌞",
                  "yes i want help": "How can i help you?😊",
                  "I want help": "How can i help you?😊",   
                "hi": "Hello! How can I assist you today? 😊",
                "hello": "Hi! How can I help you? 😊",
                "OPD Timings": "From 9AM to 8AM You can alos see details in our webiste home page 📞",
                "location": "Matoshree Hospital is located in Shivratna Nagar, Gopalpur, Pandharpur, Maharashtra. 📍",
                "hospital location": "Matoshree Hospital is located in Shivratna Nagar, Gopalpur, Pandharpur, Maharashtra. 📍",
                "contact number": "You can reach us at +91-9822353125. 📞",
                "phone number": "You can reach us at +91-9822353125. 📞", 
                "emergency services": "Yes, we provide 24/7 emergency services. 🚑",
                "thanks": "You're welcome! 😊",
                "thank you": "Happy to help! 😊",
                "appointment": "You can book an appointment by visiting the 'Appointment' page. 📝",
                "upload prescription": "You can upload your prescription on our website, and we will deliver your medicines. 💊",
                "patient reports": "Doctors upload patient reports through the admin panel. You can access them by entering your details. 📑",
                "lab test": "Our hospital offers various lab tests, including blood tests, X-rays, and MRIs. 🧪",
                "insurance accepted": "Yes, we accept multiple health insurance providers. 🏥",
                "blood donation": "We organize blood donation camps. You can inquire at our helpdesk. 🩸",
                "pharmacy": "Our in-house pharmacy is open 24/7 for your convenience. 💊",
                "billing and payment": "You can pay bills online via our website or at the hospital counter. 💳",
                "working hours": "We are open 24/7 for emergency services. 🕒",
                "covid protocols": "We follow strict COVID-19 safety measures, including sanitization and temperature checks. 😷",
                "ambulance services": "Yes, we have ambulance services available round the clock. 🚑",
                "specialist doctors": "We have expert doctors in cardiology, neurology, orthopedics, and more. 🏥",
                "diet consultation": "Our hospital provides diet and nutrition consultations. 🥗",
                "maternity services": "We offer maternity care, including prenatal and postnatal services. 🤱",
                "mental health": "We provide mental health consultations with experienced psychologists. 🧠",
                "surgery procedures": "We perform various surgical procedures, including general, orthopedic, and cardiac surgeries. 🏥",
                "home care services": "We offer home care services for elderly and bedridden patients. 🏠",
                "vaccination center": "We provide vaccinations for children and adults, including COVID-19 vaccines. 💉",
                "organ donation": "We support organ donation and transplant procedures. 🏥",
                "dental care": "Our dental department offers routine check-ups and treatments. 🦷",
                "skin and dermatology": "We provide treatments for various skin conditions and cosmetic procedures. 🌿",
                "eye care": "Our ophthalmology department offers eye check-ups and surgeries. 👁️",
                "child specialist": "Our pediatrics department provides specialized care for children. 👶",
                "physiotherapy": "We have a physiotherapy department for rehabilitation. 🏋️",
                "health checkup packages": "We offer comprehensive health checkup packages. 🩺",
                "cardiology": "Our cardiology department provides treatment for heart-related issues. ❤️",
                "neurology": "We have expert neurologists for brain and nerve disorders. 🧠",
                "orthopedics": "We provide orthopedic treatments and surgeries. 🦴",
                "oncology": "We offer cancer diagnosis and treatment. 🎗️",
                "kidney dialysis": "We have a dialysis center for kidney patients. 🏥",
                "weight loss programs": "Our hospital offers weight management consultations. ⚖️",
                "urology treatments": "We provide urology treatments and surgeries. 🚻",
                "respiratory care": "We offer treatments for lung and respiratory conditions. 🌬️",
                "stroke treatment": "We provide emergency stroke care and rehabilitation. 🏥",
                "diabetes care": "Our specialists offer diabetes management and treatment. 🩸",
                "allergy testing": "We conduct allergy tests and offer treatment plans. 🌿",
                "rheumatology": "We provide treatment for arthritis and other joint diseases. 🦵",
                "pain management": "We offer specialized pain management treatments. 💊",
                "fertility treatments": "We provide fertility consultations and treatments. 🤰",
                "sleep disorder treatment": "We diagnose and treat sleep disorders. 😴",
                "ENT specialist": "Our ENT department treats ear, nose, and throat conditions. 👂",
                "gastroenterology": "We provide treatments for digestive system disorders. 🍽️",
                "cosmetic surgery": "We offer cosmetic and reconstructive surgeries. 💉",
                "post-surgery care": "We provide post-operative care and rehabilitation. 🏥",
                "hair transplant": "Our dermatology department offers hair transplant services. 💇‍♂️",
                "home delivery of medicine": "Upload your prescription, and we will deliver your medicines to your doorstep. 🏠💊",
                "download test reports": "You can access your medical reports by logging into the patient portal. 📄",
                "nearest branch": "We have multiple branches. Please visit our website to find the nearest one. 📍",
                "language support": "Our staff speaks multiple languages for better communication. 🌍",
                "hospital facilities": "Our hospital has state-of-the-art facilities, including ICU, NICU, and OPD. 🏥",
                "discounts for senior citizens": "We offer discounts for senior citizens and special packages. 🎟️",
                
                # Additional questions and answers with alternative keywords
                "visiting hours": "Our general visiting hours are from 10 AM to 8 PM daily. ICU visiting hours are restricted to 30 minutes at 11 AM, 4 PM, and 8 PM. 🕒",
                "visitor timings": "Our general visiting hours are from 10 AM to 8 PM daily. ICU visiting hours are restricted to 30 minutes at 11 AM, 4 PM, and 8 PM. 🕒",
                "when can visitors come": "Our general visiting hours are from 10 AM to 8 PM daily. ICU visiting hours are restricted to 30 minutes at 11 AM, 4 PM, and 8 PM. 🕒",
                
                "do i need a referral": "For most specialists, a referral is recommended but not mandatory. Some insurance plans may require referrals for coverage. Please check with your insurance provider. 📋",
                "referral required": "For most specialists, a referral is recommended but not mandatory. Some insurance plans may require referrals for coverage. Please check with your insurance provider. 📋",
                "doctor recommendation needed": "For most specialists, a referral is recommended but not mandatory. Some insurance plans may require referrals for coverage. Please check with your insurance provider. 📋",
                
                "how can i get my medical records": "You can request your medical records through our patient portal or by submitting a written request at the medical records department with valid ID proof. Processing usually takes 3-5 working days. 📁",
                "medical records": "You can request your medical records through our patient portal or by submitting a written request at the medical records department with valid ID proof. Processing usually takes 3-5 working days. 📁",
                "get my health files": "You can request your medical records through our patient portal or by submitting a written request at the medical records department with valid ID proof. Processing usually takes 3-5 working days. 📁",
                "access my health information": "You can request your medical records through our patient portal or by submitting a written request at the medical records department with valid ID proof. Processing usually takes 3-5 working days. 📁",
                
                "parking facilities": "Yes, we have free parking available for patients and visitors in our hospital premises. Valet parking service is also available. 🚗",
                "car parking": "Yes, we have free parking available for patients and visitors in our hospital premises. Valet parking service is also available. 🚗",
                "where to park": "Yes, we have free parking available for patients and visitors in our hospital premises. Valet parking service is also available. 🚗",
                "is parking free": "Yes, we have free parking available for patients and visitors in our hospital premises. Valet parking service is also available. 🚗",
                
                "insurance plans": "We accept most major insurance plans including CGHS, ECHS, and various private insurers. Please contact our billing department at +91-9822353125 for specific inquiries. 💼",
                "insurance coverage": "We accept most major insurance plans including CGHS, ECHS, and various private insurers. Please contact our billing department at +91-9822353125 for specific inquiries. 💼",
                "my insurance valid": "We accept most major insurance plans including CGHS, ECHS, and various private insurers. Please contact our billing department at +91-9822353125 for specific inquiries. 💼",
                
                "pay bill online": "You can pay your hospital bills online through our website's 'Pay Bills' section using credit/debit cards, net banking, or UPI. 💳",
                "online payment": "You can pay your hospital bills online through our website's 'Pay Bills' section using credit/debit cards, net banking, or UPI. 💳",
                "pay fees": "You can pay your hospital bills online through our website's 'Pay Bills' section using credit/debit cards, net banking, or UPI. 💳",
                
                "second opinions": "Yes, we provide second opinion consultations. You can book an appointment through our website or by calling our helpline. 👨‍⚕️",
                "another doctor opinion": "Yes, we provide second opinion consultations. You can book an appointment through our website or by calling our helpline. 👨‍⚕️",
                "additional medical advice": "Yes, we provide second opinion consultations. You can book an appointment through our website or by calling our helpline. 👨‍⚕️",
                
                "cafeteria": "Yes, we have a cafeteria on the ground floor that serves healthy meals, snacks, and beverages from 7 AM to 9 PM daily. 🍽️",
                "food court": "Yes, we have a cafeteria on the ground floor that serves healthy meals, snacks, and beverages from 7 AM to 9 PM daily. 🍽️",
                "food available": "Yes, we have a cafeteria on the ground floor that serves healthy meals, snacks, and beverages from 7 AM to 9 PM daily. 🍽️",
                "canteen": "Yes, we have a cafeteria on the ground floor that serves healthy meals, snacks, and beverages from 7 AM to 9 PM daily. 🍽️",
                
                "what to bring for admission": "Please bring your ID proof, insurance card, doctor's admission note, current medications list, and any previous medical records or test reports. 📝",
                "admission requirements": "Please bring your ID proof, insurance card, doctor's admission note, current medications list, and any previous medical records or test reports. 📝",
                "hospitalization checklist": "Please bring your ID proof, insurance card, doctor's admission note, current medications list, and any previous medical records or test reports. 📝",
                
                "test results time": "Most routine lab tests results are available within 24 hours. Specialized tests may take 2-3 days. Critical results are communicated immediately. ⏱️",
                "when will my test results come": "Most routine lab tests results are available within 24 hours. Specialized tests may take 2-3 days. Critical results are communicated immediately. ⏱️",
                "results waiting time": "Most routine lab tests results are available within 24 hours. Specialized tests may take 2-3 days. Critical results are communicated immediately. ⏱️",
                
                "support groups": "Yes, we conduct regular support group meetings for cancer patients, diabetes management, and mental health. Check our events calendar for schedules. 👥",
                "patient communities": "Yes, we conduct regular support group meetings for cancer patients, diabetes management, and mental health. Check our events calendar for schedules. 👥",
                "therapy groups": "Yes, we conduct regular support group meetings for cancer patients, diabetes management, and mental health. Check our events calendar for schedules. 👥",
                
                "wheelchair accessibility": "Our hospital is fully wheelchair accessible with ramps, elevators, and specially designed restrooms. Wheelchairs are available at all entrances. ♿",
                "disabled access": "Our hospital is fully wheelchair accessible with ramps, elevators, and specially designed restrooms. Wheelchairs are available at all entrances. ♿",
                "accessibility features": "Our hospital is fully wheelchair accessible with ramps, elevators, and specially designed restrooms. Wheelchairs are available at all entrances. ♿",
                
                "cost of general checkup": "Our basic health checkup starts at ₹1500. We also offer specialized packages ranging from ₹3000 to ₹15000 depending on the tests included. 💰",
                "checkup price": "Our basic health checkup starts at ₹1500. We also offer specialized packages ranging from ₹3000 to ₹15000 depending on the tests included. 💰",
                "health screening cost": "Our basic health checkup starts at ₹1500. We also offer specialized packages ranging from ₹3000 to ₹15000 depending on the tests included. 💰",
                
                "cost estimate": "Yes, you can request a cost estimate before your treatment by contacting our billing department with your doctor's treatment plan. 📊",
                "treatment expenses": "Yes, you can request a cost estimate before your treatment by contacting our billing department with your doctor's treatment plan. 📊",
                "surgery cost": "Yes, you can request a cost estimate before your treatment by contacting our billing department with your doctor's treatment plan. 📊",
                "price estimate": "Yes, you can request a cost estimate before your treatment by contacting our billing department with your doctor's treatment plan. 📊",
                
                "feedback or complaints": "You can submit feedback or complaints through our website's 'Contact Us' section, through feedback forms available at the hospital, or by emailing feedback@matoshreehospital.com. 📢",
                "suggest improvements": "You can submit feedback or complaints through our website's 'Contact Us' section, through feedback forms available at the hospital, or by emailing feedback@matoshreehospital.com. 📢",
                "complain about service": "You can submit feedback or complaints through our website's 'Contact Us' section, through feedback forms available at the hospital, or by emailing feedback@matoshreehospital.com. 📢",
                
                "wifi": "Yes, we provide free Wi-Fi for patients and visitors. You can get the access password from the reception desk. 📶",
                "internet connection": "Yes, we provide free Wi-Fi for patients and visitors. You can get the access password from the reception desk. 📶",
                "free wifi": "Yes, we provide free Wi-Fi for patients and visitors. You can get the access password from the reception desk. 📶",
                
                "hospital admission procedure": "For planned admissions, complete pre-admission formalities at the admission desk with doctor's note, ID proof, and insurance details. For emergencies, these can be completed after initial treatment. 🛏️",
                "how to get admitted": "For planned admissions, complete pre-admission formalities at the admission desk with doctor's note, ID proof, and insurance details. For emergencies, these can be completed after initial treatment. 🛏️",
                "inpatient process": "For planned admissions, complete pre-admission formalities at the admission desk with doctor's note, ID proof, and insurance details. For emergencies, these can be completed after initial treatment. 🛏️",
                
                "accommodation for families": "We have a patient family lounge and paid guest rooms available near the hospital for families of admitted patients. 🏠",
                "family stay": "We have a patient family lounge and paid guest rooms available near the hospital for families of admitted patients. 🏠",
                "relative accommodation": "We have a patient family lounge and paid guest rooms available near the hospital for families of admitted patients. 🏠",
                
                "telehealth consultations": "Yes, we offer telehealth consultations for follow-ups and initial consultations. You can book through our website or mobile app. 💻",
                "online consultation": "Yes, we offer telehealth consultations for follow-ups and initial consultations. You can book through our website or mobile app. 💻",
                "video doctor appointment": "Yes, we offer telehealth consultations for follow-ups and initial consultations. You can book through our website or mobile app. 💻",
                "virtual checkup": "Yes, we offer telehealth consultations for follow-ups and initial consultations. You can book through our website or mobile app. 💻",
                
                "covid precautions": "We follow all safety protocols including mandatory masking, sanitization, social distancing, temperature screening, and regular staff testing. 😷",
                "corona safety": "We follow all safety protocols including mandatory masking, sanitization, social distancing, temperature screening, and regular staff testing. 😷",
                "covid safety measures": "We follow all safety protocols including mandatory masking, sanitization, social distancing, temperature screening, and regular staff testing. 😷",
                
                "cancel appointment": "You can cancel by calling our helpline at least 24 hours before your scheduled time. 📅",
                "change my appointment": "You can cancel by calling our helpline at least 24 hours before your scheduled time. 📅",
                "missed appointment": "You can reschedule it by calling our helpline at least 24 hours before your scheduled time. 📅",
                
                "top specialists": "Our hospital features renowned specialists in cardiology, neurology, orthopedics, and oncology. You can view their profiles and specializations on our website. 🥇",
                "best doctors": "Our hospital features renowned specialists in cardiology, neurology, orthopedics, and oncology. You can view their profiles and specializations on our website. 🥇",
                "expert physicians": "Our hospital features renowned specialists in cardiology, neurology, orthopedics, and oncology. You can view their profiles and specializations on our website. 🥇",
                
                "prepare for tests": "Specific preparation instructions will be provided when your test is scheduled. Generally, you may need to fast for blood tests or follow dietary restrictions for certain procedures. 🔬",
                "test preparation": "Specific preparation instructions will be provided when your test is scheduled. Generally, you may need to fast for blood tests or follow dietary restrictions for certain procedures. 🔬",
                "before test instructions": "Specific preparation instructions will be provided when your test is scheduled. Generally, you may need to fast for blood tests or follow dietary restrictions for certain procedures. 🔬",
                
                "translation services": "Yes, we provide translation services for patients who speak different languages. Please inform us of your requirements when scheduling your appointment. 🗣️",
                "language translator": "Yes, we provide translation services for patients who speak different languages. Please inform us of your requirements when scheduling your appointment. 🗣️",
                "interpreter available": "Yes, we provide translation services for patients who speak different languages. Please inform us of your requirements when scheduling your appointment. 🗣️",
                
                "icu visiting guidelines": "ICU visits are limited to two family members for 30 minutes during designated visiting hours (11 AM, 4 PM, and 8 PM). All visitors must follow hygiene protocols. 🏥",
                "icu visitor rules": "ICU visits are limited to two family members for 30 minutes during designated visiting hours (11 AM, 4 PM, and 8 PM). All visitors must follow hygiene protocols. 🏥",
                "intensive care visits": "ICU visits are limited to two family members for 30 minutes during designated visiting hours (11 AM, 4 PM, and 8 PM). All visitors must follow hygiene protocols. 🏥",
                
                "transportation services": "We provide ambulance services for emergencies. We also have a pickup and drop service for elderly and differently-abled patients for scheduled appointments. 🚑",
                "hospital transport": "We provide ambulance services for emergencies. We also have a pickup and drop service for elderly and differently-abled patients for scheduled appointments. 🚑",
                "patient pickup": "We provide ambulance services for emergencies. We also have a pickup and drop service for elderly and differently-abled patients for scheduled appointments. 🚑",
                
                "payment options": "We accept cash, credit/debit cards, online transfers, UPI payments, and checks. EMI options are available for treatments above ₹10,000. 💲",
                "payment methods": "We accept cash, credit/debit cards, online transfers, UPI payments, and checks. EMI options are available for treatments above ₹10,000. 💲",
                "how to pay": "We accept cash, credit/debit cards, online transfers, UPI payments, and checks. EMI options are available for treatments above ₹10,000. 💲",
                "emi available": "We accept cash, credit/debit cards, online transfers, UPI payments, and checks. EMI options are available for treatments above ₹10,000. 💲",
                
                "request specific doctor": "Yes, you can request a specific doctor while booking your appointment subject to their availability. 👩‍⚕️",
                "choose doctor": "Yes, you can request a specific doctor while booking your appointment subject to their availability. 👩‍⚕️",
                "specific physician": "Yes, you can request a specific doctor while booking your appointment subject to their availability. 👩‍⚕️",
                
                "medical emergency": "In case of a medical emergency, call our emergency helpline at +91-9822353125 or visit our 24/7 emergency department immediately. 🚨",
                "emergency help": "In case of a medical emergency, call our emergency helpline at +91-9822353125 or visit our 24/7 emergency department immediately. 🚨",
                "urgent medical care": "In case of a medical emergency, call our emergency helpline at +91-9822353125 or visit our 24/7 emergency department immediately. 🚨",
                
                "health programs": "You can enroll in our health programs like diabetes management, weight loss, or cardiac rehabilitation through our preventive healthcare department or website. 📋",
                "wellness programs": "You can enroll in our health programs like diabetes management, weight loss, or cardiac rehabilitation through our preventive healthcare department or website. 📋",
                "preventive healthcare": "You can enroll in our health programs like diabetes management, weight loss, or cardiac rehabilitation through our preventive healthcare department or website. 📋",
                
                # Common additional keywords for existing answers
                "directions": "Matoshree Hospital is located in Shivratna Nagar, Gopalpur, Pandharpur, Maharashtra. 📍",
                "address": "Matoshree Hospital is located in Shivratna Nagar, Gopalpur, Pandharpur, Maharashtra. 📍",
                "how to reach": "Matoshree Hospital is located in Shivratna Nagar, Gopalpur, Pandharpur, Maharashtra. 📍",
                
                "doctor fees": "Our consultation fees vary by specialty and doctor experience. General consultations start from ₹500. Please check our website for specific doctor fees. 💰",
                "consultation charges": "Our consultation fees vary by specialty and doctor experience. General consultations start from ₹500. Please check our website for specific doctor fees. 💰",
                "how much for appointment": "Our consultation fees vary by specialty and doctor experience. General consultations start from ₹500. Please check our website for specific doctor fees. 💰",
                
                "corona test": "We provide COVID-19 testing services including RT-PCR and Rapid Antigen tests. Results are typically available within 24 hours. 🧪",
                "covid test": "We provide COVID-19 testing services including RT-PCR and Rapid Antigen tests. Results are typically available within 24 hours. 🧪",
                "covid-19 testing": "We provide COVID-19 testing services including RT-PCR and Rapid Antigen tests. Results are typically available within 24 hours. 🧪",
                
                "heart doctor": "Our cardiology department provides treatment for heart-related issues. Our specialists offer comprehensive cardiac care including diagnostics, interventions, and surgeries. ❤️",
                "cardiologist": "Our cardiology department provides treatment for heart-related issues. Our specialists offer comprehensive cardiac care including diagnostics, interventions, and surgeries. ❤️",
                
                "bone doctor": "We provide orthopedic treatments and surgeries. Our orthopedic specialists treat fractures, joint problems, spine issues, and sports injuries. 🦴",
                "orthopedic": "We provide orthopedic treatments and surgeries. Our orthopedic specialists treat fractures, joint problems, spine issues, and sports injuries. 🦴",
                
                "operation": "We perform various surgical procedures, including general, orthopedic, and cardiac surgeries. Our state-of-the-art operation theaters ensure the highest standards of care. 🏥",
                "surgery timing": "Surgery schedules are determined by your surgeon based on priority and availability. Pre-operative instructions will be provided well in advance. ⏰",
                
                "visiting patient": "Our general visiting hours are from 10 AM to 8 PM daily. Please follow hospital guidelines during your visit. 🏥",
                "meet admitted patient": "Our general visiting hours are from 10 AM to 8 PM daily. Please follow hospital guidelines during your visit. 🏥",
                
                "discharge process": "Discharge typically happens in the morning. The process includes doctor's clearance, billing settlement, and discharge medication instructions. 🏥",
                "leaving hospital": "Discharge typically happens in the morning. The process includes doctor's clearance, billing settlement, and discharge medication instructions. 🏥",
                
                "corona vaccine": "We provide COVID-19 vaccinations. You can register through our website or the government CoWIN portal. 💉",
                "covid vaccination": "We provide COVID-19 vaccinations. You can register through our website or the government CoWIN portal. 💉",
                "नमस्कार": "नमस्कार! मी तुम्हाला कशी मदत करू शकते? 😊",
                "हॅलो": "हॅलो! तुम्हाला काय मदत हवी? 😊",
                "कसे आहात": "मी एक बॉट आहे, पण मी छान आहे! तुम्हाला कशी मदत करू? ✌️",
                "ओपीडी वेळ काय आहे": "आमची ओपीडी सकाळी ९ वाजता ते संध्याकाळी ८ वाजेपर्यंत आहे, सोमवार ते शनिवार 😊",
                "   ": "शिवरत्न नगर, गोपाळपूर, पंढरपूर, महाराष्ट्र 😊",
                "रुग्णालयाचे स्थान": "शिवरत्न नगर, गोपाळपूर, पंढरपूर, महाराष्ट्र 📍",
                "अपॉइंटमेंट कसे बुक करावे": "तुम्ही आमच्या 'अपॉइंटमेंट' पेजवर जाऊन आवश्यक तपशील भरून अपॉइंटमेंट बुक करू शकता 📝",
                "धन्यवाद": "आनंद झाला! 😊",
                "आभार": "माझा आनंद झाला! 😊",
                "सुप्रभात": "सुप्रभात! मातोश्री हॉस्पिटलमध्ये आपले स्वागत आहे. मी तुम्हाला कशी मदत करू? ☀️",
                "नमस्कार मला मदत हवी": "तुम्हाला कशी मदत हवी? 😊",
                "मला मदत हवी": "तुम्हाला कशी मदत हवी? 😊",
                "कॉन्टॅक्ट नंबर": "तुम्ही आम्हाला +91-9822353125 या नंबरवर संपर्क करू शकता 📞",
                "फोन नंबर": "तुम्ही आम्हाला +91-9822353125 या नंबरवर संपर्क करू शकता 📞",
                "आणीबाणी सेवा": "होय, आम्ही 24/7 आणीबाणी सेवा पुरवतो 🚑",
                "प्रिस्क्रिप्शन कसे अपलोड करावे": "तुम्ही आमच्या वेबसाइटवर तुमचे प्रिस्क्रिप्शन अपलोड करू शकता आणि आम्ही तुमची औषधे पोहोचवू 💊",
                "रुग्ण अहवाल": "डॉक्टर रुग्ण अहवाल व्यवस्थापक पॅनेलद्वारे अपलोड करतात. तुम्ही तुमचे तपशील प्रविष्ट करून त्यांना प्रवेश करू शकता 📑",
                "प्रयोगशाळा चाचणी": "आमच्या रुग्णालयात रक्त चाचण्या, एक्स-रे आणि एमआरआय यासह विविध प्रयोगशाळा चाचण्या उपलब्ध आहेत 🧪",
                "विमा स्वीकारला जातो का": "होय, आम्ही अनेक आरोग्य विमा प्रदात्यांना स्वीकारतो 🏥",
                "रक्तदान": "आम्ही रक्तदान शिबिरे आयोजित करतो. तुम्ही आमच्या हेल्पडेस्कवर विचारू शकता 🩸",
                "औषधालय": "आमचे इन-हाऊस फार्मसी तुमच्या सोयीसाठी 24/7 उघडे आहे 💊",
                "बिल आणि पेमेंट": "तुम्ही आमच्या वेबसाइटद्वारे किंवा रुग्णालयाच्या काउंटरवर बिले ऑनलाइन भरू शकता 💳",
                "कामाचे तास": "आम्ही आणीबाणी सेवांसाठी 24/7 उपलब्ध आहोत 🕒",
                "कोविड प्रोटोकॉल": "आम्ही स्वच्छता आणि तापमान तपासणीसह कठोर COVID-19 सुरक्षा उपायांचे पालन करतो 😷",
                "रुग्णवाहिका सेवा": "होय, आमच्याकडे रात्रंदिवस रुग्णवाहिका सेवा उपलब्ध आहे 🚑"
            }
            

            # Exact match first
            if user_message in responses:
                bot_reply = responses[user_message]
            else:
                # Fuzzy match for close matches3
                closest_match = difflib.get_close_matches(user_message, responses.keys(), n=1, cutoff=0.7)
                bot_reply = responses.get(closest_match[0], "I'm not sure about that. Can you please rephrase?") if closest_match else "I'm not sure about that. Can you please rephrase?"

            return JsonResponse({"response": bot_reply})
        except json.JSONDecodeError:
            return JsonResponse({"response": "Invalid request"}, status=400)
    return JsonResponse({"response": "Invalid request method"}, status=405)