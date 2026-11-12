"""
Narration script for the "Fractions and Decimals" lesson.

Each key is one voice-over clip. The text is written the way an Indian
teacher would read it aloud in class ("two by three", "let us see",
"very good"), so the TTS voice sounds natural, and numbers are spelt
out wherever a symbol would be read badly.
"""

NARRATION = {
    # ---------------------------------------------------------------- intro
    "intro_1": "Namaste, students! Welcome to today's class on fractions and decimals.",
    "intro_2": "In the earlier class, we learnt about fractions and decimals, and how to add and subtract them.",
    "intro_3": "Today, we will study the operations of multiplication and division, first on fractions, and then on decimals. So, let us begin!",

    # ------------------------------------------------- multiplying fractions
    "mul_1": "First, multiplication of fractions. Two fractions are multiplied by multiplying their numerators and their denominators separately.",
    "mul_2": "Let us take two by three, multiplied by five by seven.",
    "mul_3": "Multiply the numerators: two into five. Multiply the denominators: three into seven.",
    "mul_4": "Two into five is ten, and three into seven is twenty one. So the answer is ten by twenty one. Simple, no?",

    # ------------------------------------------------------ "of" as operator
    "of_1": "Now, a fraction acts as an operator, 'of'. What is half of two?",
    "of_2": "Here we have two whole rotis. Half of two means we take one half of the total.",
    "of_3": "So, one by two of two is one by two into two, which equals one. Very good!",

    # --------------------------------------------- comparing the product size
    "cmp_1": "Now, let us see what happens to the size of the product. We will use a number line.",
    "cmp_2": "Case one. Product of two proper fractions. Half into one third is one sixth. It is less than both the fractions.",
    "cmp_3": "Case two. A proper fraction into an improper fraction. Half into five by three is five by six. It is less than the improper fraction, but greater than the proper fraction.",
    "cmp_4": "Case three. Two improper fractions. Three by two into five by three is five by two. It is greater than both the fractions.",

    # ------------------------------------------------------------ reciprocal
    "rec_1": "Next, the reciprocal. The reciprocal of a fraction is obtained by inverting it, upside down.",
    "rec_2": "So, the reciprocal of three by five is five by three. The numerator and denominator simply change places.",

    # -------------------------------------------------------------- division
    "div_1": "Now, let us divide. Case A. To divide a whole number by a fraction, multiply the whole number by the reciprocal of that fraction.",
    "div_2": "Two divided by three by five becomes two into five by three, which is ten by three.",
    "div_3": "Case B. To divide a fraction by a whole number, multiply the fraction by the reciprocal of the whole number.",
    "div_4": "Two by three divided by seven becomes two by three into one by seven, which is two by twenty one.",
    "div_5": "Case C. To divide one fraction by another, multiply the first fraction by the reciprocal of the second.",
    "div_6": "Two by three divided by five by seven becomes two by three into seven by five, which is fourteen by fifteen.",

    # ------------------------------------------------- multiplying decimals
    "dmul_1": "Now, let us move to decimals. How do we multiply two decimal numbers? Take zero point five into zero point seven.",
    "dmul_2": "Step one. First, multiply them as whole numbers. Five into seven is thirty five.",
    "dmul_3": "Step two. Count the digits to the right of the decimal point. One digit here, and one digit here. One plus one is two.",
    "dmul_4": "Step three. In the product, count two places from the rightmost digit and put the decimal point. So the answer is zero point three five.",

    # ------------------------------------------- multiplying by 10, 100, 1000
    "p10_1": "To multiply a decimal by ten, hundred or thousand, move the decimal point to the right, by as many places as there are zeros.",
    "p10_2": "Zero point five three into ten. Ten has one zero, so the point moves one place. We get five point three.",
    "p10_3": "Into hundred. Two zeros, two places. We get fifty three.",
    "p10_4": "Into thousand. Three zeros, three places. We put a zero to fill the empty place, and we get five hundred and thirty.",

    # ------------------------------------------ dividing decimal by whole no.
    "ddiv_1": "Now, division of decimals. Case A. To divide a decimal number by a whole number, first divide them as whole numbers.",
    "ddiv_2": "Eight point four divided by four. Eighty four divided by four is twenty one.",
    "ddiv_3": "Then place the decimal point in the quotient, as in the decimal number. So the answer is two point one. Note, here we take only those divisions where the remainder is zero.",

    # -------------------------------------------- dividing by 10, 100, 1000
    "d10_1": "Case B. To divide a decimal number by ten, hundred or thousand, shift the decimal point to the left, by as many places as there are zeros.",
    "d10_2": "Twenty three point nine divided by ten gives two point three nine.",
    "d10_3": "Divided by hundred gives zero point two three nine.",
    "d10_4": "And divided by thousand, we fill in a zero, and get zero point zero two three nine.",

    # ------------------------------------------ dividing decimal by decimal
    "dd_1": "Case C. To divide one decimal number by another, first shift the decimal point to the right by an equal number of places in both, so that the divisor becomes a whole number.",
    "dd_2": "Two point four divided by zero point two. Shift the point one place in both numbers.",
    "dd_3": "Now it becomes twenty four divided by two, which is twelve. That's it!",

    # --------------------------------------------------------------- summary
    "sum_1": "So, let us quickly revise what we learnt today.",
    "sum_2": "Multiply numerators and denominators. To divide, multiply by the reciprocal. For decimals, count the decimal places, and move the point for ten, hundred and thousand.",
    "sum_3": "Practise these at home, and you will become a champion of fractions and decimals. Thank you, students! See you in the next class.",
}
