"""
Hinglish narration for the "Fractions and Decimals" lesson.

Each clip has two versions of the same sentence:

* ``NARRATION`` - Roman-script Hinglish, shown on screen as subtitles.
* ``SPEECH``    - the same words in Devanagari, read by the Hindi TTS
                  voice.  English words are written phonetically
                  (e.g. "फ़्रैक्शन") so they come out in a natural
                  Indian classroom accent.

Keep both versions in sync when editing a line.
"""

_LINES = {
    # ---------------------------------------------------------------- intro
    "intro_1": (
        "Namaste bachcho! Aaj ki class mein hum padhenge Fractions aur Decimals.",
        "नमस्ते बच्चो! आज की क्लास में हम पढ़ेंगे फ़्रैक्शन्स और डेसिमल्स।",
    ),
    "intro_2": (
        "Pichhli class mein humne fractions aur decimals ke baare mein seekha tha, aur unko add aur subtract karna bhi seekha tha.",
        "पिछली क्लास में हमने फ़्रैक्शन्स और डेसिमल्स के बारे में सीखा था, और उनको ऐड और सब्ट्रैक्ट करना भी सीखा था।",
    ),
    "intro_3": (
        "Aaj hum multiplication aur division seekhenge, pehle fractions par, aur phir decimals par. Toh chaliye, shuru karte hain!",
        "आज हम मल्टिप्लिकेशन और डिविज़न सीखेंगे, पहले फ़्रैक्शन्स पर, और फिर डेसिमल्स पर। तो चलिए, शुरू करते हैं!",
    ),

    # ------------------------------------------------- multiplying fractions
    "mul_1": (
        "Sabse pehle, fractions ka multiplication. Do fractions ko multiply karne ke liye, numerators ko aapas mein multiply karo, aur denominators ko alag se multiply karo.",
        "सबसे पहले, फ़्रैक्शन्स का मल्टिप्लिकेशन। दो फ़्रैक्शन्स को मल्टिप्लाई करने के लिए, न्यूमरेटर्स को आपस में मल्टिप्लाई करो, और डिनॉमिनेटर्स को अलग से मल्टिप्लाई करो।",
    ),
    "mul_2": (
        "Chalo ek example lete hain. Two by three into five by seven.",
        "चलो एक एग्ज़ाम्पल लेते हैं। टू बाई थ्री इनटू फ़ाइव बाई सेवन।",
    ),
    "mul_3": (
        "Numerators ko multiply karo: two into five. Denominators ko multiply karo: three into seven.",
        "न्यूमरेटर्स को मल्टिप्लाई करो: टू इनटू फ़ाइव। डिनॉमिनेटर्स को मल्टिप्लाई करो: थ्री इनटू सेवन।",
    ),
    "mul_4": (
        "Two into five hota hai ten, aur three into seven hota hai twenty one. Toh answer aaya ten by twenty one. Simple hai na?",
        "टू इनटू फ़ाइव होता है टेन, और थ्री इनटू सेवन होता है ट्वेंटी वन। तो आंसर आया टेन बाई ट्वेंटी वन। सिंपल है ना?",
    ),

    # ------------------------------------------------------ "of" as operator
    "of_1": (
        "Ab dekho, fraction ek operator ki tarah kaam karta hai, jiska matlab hai 'of'. Batao, two ka half kitna hoga?",
        "अब देखो, फ़्रैक्शन एक ऑपरेटर की तरह काम करता है, जिसका मतलब है 'ऑफ़'। बताओ, टू का हाफ़ कितना होगा?",
    ),
    "of_2": (
        "Yahan humare paas do rotiyaan hain. Two ka half matlab, total ka aadha hissa.",
        "यहाँ हमारे पास दो रोटियाँ हैं। टू का हाफ़ मतलब, टोटल का आधा हिस्सा।",
    ),
    "of_3": (
        "Toh, one by two of two, matlab one by two into two, jo hota hai one. Bahut badhiya!",
        "तो, वन बाई टू ऑफ़ टू, मतलब वन बाई टू इनटू टू, जो होता है वन। बहुत बढ़िया!",
    ),

    # --------------------------------------------- comparing the product size
    "cmp_1": (
        "Ab dekhte hain ki product chhota hota hai ya bada. Iske liye hum number line use karenge.",
        "अब देखते हैं कि प्रोडक्ट छोटा होता है या बड़ा। इसके लिए हम नंबर लाइन यूज़ करेंगे।",
    ),
    "cmp_2": (
        "Case one. Do proper fractions ka product. Half into one third barabar one sixth. Yeh dono fractions se chhota hai.",
        "केस वन। दो प्रॉपर फ़्रैक्शन्स का प्रोडक्ट। हाफ़ इनटू वन थर्ड बराबर वन सिक्स्थ। यह दोनों फ़्रैक्शन्स से छोटा है।",
    ),
    "cmp_3": (
        "Case two. Ek proper aur ek improper fraction. Half into five by three barabar five by six. Yeh improper fraction se chhota hai, lekin proper fraction se bada hai.",
        "केस टू। एक प्रॉपर और एक इम्प्रॉपर फ़्रैक्शन। हाफ़ इनटू फ़ाइव बाई थ्री बराबर फ़ाइव बाई सिक्स। यह इम्प्रॉपर फ़्रैक्शन से छोटा है, लेकिन प्रॉपर फ़्रैक्शन से बड़ा है।",
    ),
    "cmp_4": (
        "Case three. Do improper fractions. Three by two into five by three barabar five by two. Yeh dono fractions se bada hai.",
        "केस थ्री। दो इम्प्रॉपर फ़्रैक्शन्स। थ्री बाई टू इनटू फ़ाइव बाई थ्री बराबर फ़ाइव बाई टू। यह दोनों फ़्रैक्शन्स से बड़ा है।",
    ),

    # ------------------------------------------------------------ reciprocal
    "rec_1": (
        "Ab baat karte hain reciprocal ki. Kisi fraction ko ulta kar do, upar ka neeche aur neeche ka upar, toh mil jaata hai uska reciprocal.",
        "अब बात करते हैं रेसिप्रोकल की। किसी फ़्रैक्शन को उल्टा कर दो, ऊपर का नीचे और नीचे का ऊपर, तो मिल जाता है उसका रेसिप्रोकल।",
    ),
    "rec_2": (
        "Jaise, three by five ka reciprocal hai five by three. Numerator aur denominator bas apni jagah badal lete hain.",
        "जैसे, थ्री बाई फ़ाइव का रेसिप्रोकल है फ़ाइव बाई थ्री। न्यूमरेटर और डिनॉमिनेटर बस अपनी जगह बदल लेते हैं।",
    ),

    # -------------------------------------------------------------- division
    "div_1": (
        "Ab division karte hain. Case A. Whole number ko fraction se divide karna ho, toh whole number ko us fraction ke reciprocal se multiply karo.",
        "अब डिविज़न करते हैं। केस ए। होल नंबर को फ़्रैक्शन से डिवाइड करना हो, तो होल नंबर को उस फ़्रैक्शन के रेसिप्रोकल से मल्टिप्लाई करो।",
    ),
    "div_2": (
        "Two divided by three by five ban jaata hai two into five by three, yaani ten by three.",
        "टू डिवाइडेड बाई थ्री बाई फ़ाइव बन जाता है टू इनटू फ़ाइव बाई थ्री, यानी टेन बाई थ्री।",
    ),
    "div_3": (
        "Case B. Fraction ko whole number se divide karna ho, toh fraction ko whole number ke reciprocal se multiply karo.",
        "केस बी। फ़्रैक्शन को होल नंबर से डिवाइड करना हो, तो फ़्रैक्शन को होल नंबर के रेसिप्रोकल से मल्टिप्लाई करो।",
    ),
    "div_4": (
        "Two by three divided by seven ban jaata hai two by three into one by seven, yaani two by twenty one.",
        "टू बाई थ्री डिवाइडेड बाई सेवन बन जाता है टू बाई थ्री इनटू वन बाई सेवन, यानी टू बाई ट्वेंटी वन।",
    ),
    "div_5": (
        "Case C. Ek fraction ko doosre fraction se divide karna ho, toh pehle fraction ko doosre ke reciprocal se multiply karo.",
        "केस सी। एक फ़्रैक्शन को दूसरे फ़्रैक्शन से डिवाइड करना हो, तो पहले फ़्रैक्शन को दूसरे के रेसिप्रोकल से मल्टिप्लाई करो।",
    ),
    "div_6": (
        "Two by three divided by five by seven ban jaata hai two by three into seven by five, yaani fourteen by fifteen.",
        "टू बाई थ्री डिवाइडेड बाई फ़ाइव बाई सेवन बन जाता है टू बाई थ्री इनटू सेवन बाई फ़ाइव, यानी फ़ोर्टीन बाई फ़िफ़्टीन।",
    ),

    # ------------------------------------------------- multiplying decimals
    "dmul_1": (
        "Ab chalte hain decimals ki taraf. Do decimal numbers ko multiply kaise karte hain? Lete hain zero point five into zero point seven.",
        "अब चलते हैं डेसिमल्स की तरफ़। दो डेसिमल नंबर्स को मल्टिप्लाई कैसे करते हैं? लेते हैं ज़ीरो पॉइंट फ़ाइव इनटू ज़ीरो पॉइंट सेवन।",
    ),
    "dmul_2": (
        "Step one. Pehle inhe whole numbers ki tarah multiply karo. Five into seven, thirty five.",
        "स्टेप वन। पहले इन्हें होल नंबर्स की तरह मल्टिप्लाई करो। फ़ाइव इनटू सेवन, थर्टी फ़ाइव।",
    ),
    "dmul_3": (
        "Step two. Decimal point ke right mein kitne digits hain, gino. Yahan ek digit, aur yahan bhi ek digit. One plus one, two.",
        "स्टेप टू। डेसिमल पॉइंट के राइट में कितने डिजिट्स हैं, गिनो। यहाँ एक डिजिट, और यहाँ भी एक डिजिट। वन प्लस वन, टू।",
    ),
    "dmul_4": (
        "Step three. Product mein right side se do jagah gin kar decimal point lagao. Toh answer aaya zero point three five.",
        "स्टेप थ्री। प्रोडक्ट में राइट साइड से दो जगह गिन कर डेसिमल पॉइंट लगाओ। तो आंसर आया ज़ीरो पॉइंट थ्री फ़ाइव।",
    ),

    # ------------------------------------------- multiplying by 10, 100, 1000
    "p10_1": (
        "Decimal ko ten, hundred ya thousand se multiply karna ho, toh decimal point ko right side mein utni jagah khiskao, jitne zeros hain.",
        "डेसिमल को टेन, हंड्रेड या थाउज़ेंड से मल्टिप्लाई करना हो, तो डेसिमल पॉइंट को राइट साइड में उतनी जगह खिसकाओ, जितने ज़ीरोज़ हैं।",
    ),
    "p10_2": (
        "Zero point five three into ten. Ten mein ek zero hai, toh point ek jagah khiskega. Mila five point three.",
        "ज़ीरो पॉइंट फ़ाइव थ्री इनटू टेन। टेन में एक ज़ीरो है, तो पॉइंट एक जगह खिसकेगा। मिला फ़ाइव पॉइंट थ्री।",
    ),
    "p10_3": (
        "Into hundred. Do zeros, do jagah. Mila fifty three.",
        "इनटू हंड्रेड। दो ज़ीरोज़, दो जगह। मिला फ़िफ़्टी थ्री।",
    ),
    "p10_4": (
        "Into thousand. Teen zeros, teen jagah. Khaali jagah mein ek zero lagao, aur mila five hundred thirty.",
        "इनटू थाउज़ेंड। तीन ज़ीरोज़, तीन जगह। ख़ाली जगह में एक ज़ीरो लगाओ, और मिला फ़ाइव हंड्रेड थर्टी।",
    ),

    # ------------------------------------------ dividing decimal by whole no.
    "ddiv_1": (
        "Ab decimals ka division. Case A. Decimal number ko whole number se divide karna ho, toh pehle dono ko whole numbers ki tarah divide karo.",
        "अब डेसिमल्स का डिविज़न। केस ए। डेसिमल नंबर को होल नंबर से डिवाइड करना हो, तो पहले दोनों को होल नंबर्स की तरह डिवाइड करो।",
    ),
    "ddiv_2": (
        "Eight point four divided by four. Eighty four divided by four, twenty one.",
        "एट पॉइंट फ़ोर डिवाइडेड बाई फ़ोर। एटी फ़ोर डिवाइडेड बाई फ़ोर, ट्वेंटी वन।",
    ),
    "ddiv_3": (
        "Phir quotient mein decimal point waise hi lagao, jaise decimal number mein hai. Toh answer hai two point one. Dhyan rahe, yahan hum sirf woh divisions le rahe hain jinka remainder zero hai.",
        "फिर कोशेंट में डेसिमल पॉइंट वैसे ही लगाओ, जैसे डेसिमल नंबर में है। तो आंसर है टू पॉइंट वन। ध्यान रहे, यहाँ हम सिर्फ़ वो डिविज़न्स ले रहे हैं जिनका रिमेंडर ज़ीरो है।",
    ),

    # -------------------------------------------- dividing by 10, 100, 1000
    "d10_1": (
        "Case B. Decimal number ko ten, hundred ya thousand se divide karna ho, toh decimal point ko left side mein utni jagah khiskao, jitne zeros hain.",
        "केस बी। डेसिमल नंबर को टेन, हंड्रेड या थाउज़ेंड से डिवाइड करना हो, तो डेसिमल पॉइंट को लेफ़्ट साइड में उतनी जगह खिसकाओ, जितने ज़ीरोज़ हैं।",
    ),
    "d10_2": (
        "Twenty three point nine divided by ten, mila two point three nine.",
        "ट्वेंटी थ्री पॉइंट नाइन डिवाइडेड बाई टेन, मिला टू पॉइंट थ्री नाइन।",
    ),
    "d10_3": (
        "Divided by hundred, mila zero point two three nine.",
        "डिवाइडेड बाई हंड्रेड, मिला ज़ीरो पॉइंट टू थ्री नाइन।",
    ),
    "d10_4": (
        "Aur divided by thousand, ek zero bharo, aur mila zero point zero two three nine.",
        "और डिवाइडेड बाई थाउज़ेंड, एक ज़ीरो भरो, और मिला ज़ीरो पॉइंट ज़ीरो टू थ्री नाइन।",
    ),

    # ------------------------------------------ dividing decimal by decimal
    "dd_1": (
        "Case C. Ek decimal ko doosre decimal se divide karna ho, toh dono mein decimal point ko barabar jagah right mein khiskao, taaki divisor whole number ban jaaye.",
        "केस सी। एक डेसिमल को दूसरे डेसिमल से डिवाइड करना हो, तो दोनों में डेसिमल पॉइंट को बराबर जगह राइट में खिसकाओ, ताकि डिवाइज़र होल नंबर बन जाए।",
    ),
    "dd_2": (
        "Two point four divided by zero point two. Dono numbers mein point ko ek jagah khiskao.",
        "टू पॉइंट फ़ोर डिवाइडेड बाई ज़ीरो पॉइंट टू। दोनों नंबर्स में पॉइंट को एक जगह खिसकाओ।",
    ),
    "dd_3": (
        "Ab yeh ban gaya twenty four divided by two, yaani twelve. Bas, ho gaya!",
        "अब यह बन गया ट्वेंटी फ़ोर डिवाइडेड बाई टू, यानी ट्वेल्व। बस, हो गया!",
    ),

    # --------------------------------------------------------------- summary
    "sum_1": (
        "Toh chalo, jaldi se revise kar lete hain ki aaj humne kya seekha.",
        "तो चलो, जल्दी से रिवाइज़ कर लेते हैं कि आज हमने क्या सीखा।",
    ),
    "sum_2": (
        "Numerators aur denominators ko multiply karo. Divide karne ke liye reciprocal se multiply karo. Decimals mein decimal places gino, aur ten, hundred, thousand ke liye point khiskao.",
        "न्यूमरेटर्स और डिनॉमिनेटर्स को मल्टिप्लाई करो। डिवाइड करने के लिए रेसिप्रोकल से मल्टिप्लाई करो। डेसिमल्स में डेसिमल प्लेसेज़ गिनो, और टेन, हंड्रेड, थाउज़ेंड के लिए पॉइंट खिसकाओ।",
    ),
    "sum_3": (
        "Ghar par practice karna, aur aap ban jaoge fractions aur decimals ke champion. Thank you bachcho! Milte hain agli class mein.",
        "घर पर प्रैक्टिस करना, और आप बन जाओगे फ़्रैक्शन्स और डेसिमल्स के चैंपियन। थैंक यू बच्चो! मिलते हैं अगली क्लास में।",
    ),
}

NARRATION = {key: roman for key, (roman, _) in _LINES.items()}
SPEECH = {key: devanagari for key, (_, devanagari) in _LINES.items()}
