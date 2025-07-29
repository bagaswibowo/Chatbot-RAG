from collections import Counter
import re

def extract_user_style(chats, user_name):
    user_msgs = [c['message'] for c in chats if c['sender'] == user_name]
    # Contoh ekstraksi: kata paling sering, emoji, panjang rata-rata
    words = []
    emojis = []
    emosi_positif = ['senang', 'happy', 'baik', 'mantap', 'oke', 'sip', '😊', '👍', '😁', '😂']
    emosi_negatif = ['sedih', 'marah', 'kesal', 'jelek', 'tidak', 'enggak', '😢', '😭', '😡', '👎']
    formal_words = ['saya', 'anda', 'bapak', 'ibu', 'terima kasih', 'permisi', 'silakan']
    informal_words = ['gue', 'elo', 'lu', 'bro', 'sis', 'wkwk', 'haha', 'yaudah', 'gak', 'nggak']
    emosi_score = 0
    formal_score = 0
    informal_score = 0
    for msg in user_msgs:
        words += re.findall(r'\w+', msg.lower())
        emojis += re.findall(r'[\U0001F600-\U0001F64F]', msg)
        # Emosi
        if any(e in msg.lower() for e in emosi_positif):
            emosi_score += 1
        if any(e in msg.lower() for e in emosi_negatif):
            emosi_score -= 1
        # Formalitas
        if any(f in msg.lower() for f in formal_words):
            formal_score += 1
        if any(i in msg.lower() for i in informal_words):
            informal_score += 1
    word_freq = Counter(words).most_common(10)
    emoji_freq = Counter(emojis).most_common(5)
    avg_len = sum(len(m) for m in user_msgs) / (len(user_msgs) or 1)
    # Analisis emosi
    if emosi_score > 2:
        emosi_label = 'positif'
    elif emosi_score < -2:
        emosi_label = 'negatif'
    else:
        emosi_label = 'netral'
    # Analisis formalitas
    if formal_score > informal_score:
        formal_label = 'formal'
    elif informal_score > formal_score:
        formal_label = 'informal'
    else:
        formal_label = 'campuran'
    return {
        'top_words': word_freq,
        'top_emojis': emoji_freq,
        'avg_length': avg_len,
        'emosi': emosi_label,
        'formalitas': formal_label
    }
