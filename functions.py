import spacy
import re
import pyphen

mapping_dict = {
    "ADJ": "A",
    "ADP": "S",
    "ADV": "R",
    "AUX": "V",
    "CONJ": "C",
    "CCONJ": "C",
    "DET": "D",
    "INTJ": "I",
    "NOUN": "N",
    "NUM": "M",
    "PART": "Q",
    "PRON": "P",
    "PROPN": "N",
    "PUNCT": "Z",
    "SCONJ": "S",
    "SYM": "X",
    "VERB": "V"
}
PRON_REFLEXIV = ["mă", "te", "se", "ne", "vă"]
VOWELS = ['a', 'ă', 'â', 'e', 'i', 'o', 'u', 'A', 'Ă', 'Â', 'E', 'I', 'O', 'U']
PUNCTUATION_MARKS = ['.', ',', '!', '?', ':', ';' , '-', '(', ')', '[', ']', '{', '}', "'", '"', '...', '“', '”', '/', '\\', '|', '_', '@', '#', '$', '%', '^', '&', '*', '~', '`', '<', '>', '=']

dictionary = {}
dic = pyphen.Pyphen(lang='ro_RO')

# Desparte textul in fraze
def split_phases(text):
    phases = []
    one_phase = ''
    len_text = len(text)
    skip = 0
    for i in range(0, len_text):
        if one_phase == '' and text[i] == ' ':
            continue
        
        one_phase += text[i]
        
        if(skip > 0):
            skip -= 1
            continue
        # In cazul in care textul se termina cu puncte de suspensie
        if (i == len_text - 3) and (text[i] == '.') and (text[i+1] == '.') and (text[i+2] == '.'):
            one_phase += ".."
            phases.append(one_phase)
            break
        # Daca punctele de suspensie sunt in interiorul frazei
        if (i < len_text - 2) and (text[i] == '.') and (text[i+1] == '.') and (text[i+2] == '.'):
            skip = 2
        # Frazele sunt despartite in functie de punct, semnul intrebarii si semnul exclamarii
        elif (text[i] == '.') or (text[i] == '?') or (text[i] == '!'):
            phases.append(one_phase)
            one_phase = ''

    return phases

def search_rhytmic_indices(len_phases, len_phi):
    rhythmic_indices = []
    for i in range(0,len(len_phases)):
        for k in range(1,10000):
            if len_phases[i]/k < len_phi[i] and len_phi[i] < k * len_phases[i]:
                rhythmic_indices.append(k)
                break

    return rhythmic_indices

def create_dic ():
    file1 = open('lexicon_reterom_final.v1.txt', 'r', encoding='utf-8')
    Lines = file1.readlines()
 
    count = 0
    # Strips the newline character
    for line in Lines:
        count += 1
        line = line.strip()
        # Desparte linia în funcție de tabulator (\t)
        words = line.split("\t")

        if words[0] in dictionary.keys():
            dictionary[words[0]][words[2][0]] = [words[3].replace(".","-"), words[4]]
        else:
            dictionary[words[0]] = {words[2][0] : [words[3].replace(".","-"), words[4]]}

def accentuate(syllables):
    if len(syllables) < 2:
        syllable = syllables[0]
        for i, char in enumerate(syllable):
            if char in VOWELS:
                syllables[0] = syllable[:i+1] + "'" + syllable[i+1:]
                break
        return ''.join(syllables)
    
    penultimate_syllable = syllables[-2]
    for i, char in enumerate(penultimate_syllable):
        if char in VOWELS:
            syllables[-2] = penultimate_syllable[:i+1] + "'" + penultimate_syllable[i+1:]
            break
    
    return ''.join(syllables)

def process_word(word):
    syllables = dic.inserted(word)
    accented_word = accentuate(syllables)
    
    return (syllables, accented_word)

# Functie de despartire in silabe si determinare silaba accentuata
def syllable_split_and_accent(fragments) :
    # Procesați paragraful cu spaCy
    global nlp
    all_phases_syll = []
    all_phases_accent = []
    all_phases_len = []
    all_words_with_accent = []
    for paragraf in fragments:
        doc = nlp(paragraf)
        # Iterați peste fiecare cuvânt din paragraf și afișați partea de vorbire a fiecărui cuvânt
        paragraf_accent = []
        paragraf_syll = []
        words_with_accent_in_paragraf = []
        
        len_phas = 0
        
        for token in doc:
            words_with_accent = []
            current_token = None
            if token.pos_ == "PROPN":
                current_token = token.text
            else:
                current_token = token.text.lower()
            if token.pos_ not in ['PUNCT', 'SYM']:
                len_phas += 1
                syll = None
                accent = None

                if current_token in dictionary:

                    key = None
                    if mapping_dict[token.pos_] in dictionary[current_token]:
                        key = mapping_dict[token.pos_]
                    else:
                        key = list(dictionary[current_token].keys())[0]

                    syll = dictionary[current_token][key][0]
                    syll = syll.split("-")

                    paragraf_syll.append(syll)

                    accent = dictionary[current_token][key][1]
                else:
                    syll, accent = process_word(current_token)

                if token.text in PRON_REFLEXIV:
                    paragraf_accent.append(0)
                    words_with_accent.append(0)
                elif "'" in accent and token.pos_ not in ['DET', 'CONJ', "CCONJ", "SCONJ", "ADP"]:
                    index_accent = accent.index("'")
                    count_ch = 0
                    is_found = False
                    for one_syll in syll:
                        if is_found == False and index_accent >= count_ch and index_accent < count_ch + len(one_syll):
                            paragraf_accent.append(1)
                            is_found = True
                        else:
                            paragraf_accent.append(0)
                        count_ch += len(one_syll)
                    words_with_accent.append(1)
                            

                elif token.pos_ not in ['DET', 'CONJ', "CCONJ", "SCONJ", "ADP"]:
                    paragraf_accent.append(1)
                    words_with_accent.append(1)
                else:
                    paragraf_accent.append(0)
                    words_with_accent.append(0)

            else:
                paragraf_syll.append([token.text])
            
            words_with_accent_in_paragraf.append(words_with_accent)    
        
        all_words_with_accent.append(words_with_accent_in_paragraf)  
        all_phases_syll.append(paragraf_syll)
        all_phases_accent.append(paragraf_accent)
        all_phases_len.append(len_phas)
    return (all_phases_syll, all_phases_accent, all_phases_len, all_words_with_accent)

def vasile_vasile(text):
    lines = text.split("\n")
    groups_vowels = []
    for line in lines:
        one_group_vowels = []
        words = re.split(r'[ ,.!?;:"]+', line)

        for word in words:
            aux_group = []
            count_vowels = 0
            for i in range(0, len(word)):
                if count_vowels == 3:
                    break

                if word[i] in VOWELS:
                    count_vowels += 1
                    aux_group.append(word[i])
                elif count_vowels > 0:
                    aux_group.append('-')
            if count_vowels == 3:
                one_group_vowels.append(aux_group)

        groups_vowels.append(one_group_vowels)

    output_text = ""
    for i in range(0, len(lines)):
        output_text += (lines[i] + "\n")
        output_text += (' | '.join([' '.join(sublist) for sublist in groups_vowels[i]]) + "\n\n")

    return output_text
    
def solomon_marcus(text):
    fragments = split_phases(text)
    create_dic()
    global nlp

    nlp = spacy.load("ro_core_news_sm")

    silabe, accent, len_phases, words_with_accent = syllable_split_and_accent(fragments)
    
    # Structura ritmica
    rhythmic_structure = []
    for ac in accent:
        count = 0
        one_rhythmic_structure = []
        for is_accentuated in ac:
            count += 1
            if is_accentuated == 1:
                one_rhythmic_structure.append(count)
                count = 0
        if count != 0:
            one_rhythmic_structure.append(count)
        rhythmic_structure.append(one_rhythmic_structure)

    len_phi = [len(lst) for lst in rhythmic_structure]
    superior_rhythmic_borders = [max(lst) for lst in rhythmic_structure]
    lower_rhythmic_borders = [min(lst) for lst in rhythmic_structure]
    rhythmic_diameters = [a - b for a, b in zip(superior_rhythmic_borders, lower_rhythmic_borders)]


    rhythmic_indices = search_rhytmic_indices(len_phases, len_phi)
    output_text = ""
    for i in range(0, len(silabe)):
        ind_start = 0
        ind_end = 0
        for word in silabe[i]:
            if word[0] in PUNCTUATION_MARKS:
                output_text += (word[0] + " ")
            else:
                ind_end = ind_start + len(word)
                word_accent = accent[i][ind_start:ind_end]
                for ind_accent in range(0, len(word_accent)):
                    if word_accent[ind_accent] == 1:
                        word[ind_accent] = "#" + word[ind_accent]
                ind_start = ind_end            
                output_text += ('-'.join(word) + " ")

        output_text += "\n"

        output_text += ("Lungimea ritmica: " + str(len_phi[i]) + "\n")
        output_text += ("Indicele ritmic: " + str(rhythmic_indices[i]) + "\n")
        output_text += ("Marginea ritmica inferioara: " + str(lower_rhythmic_borders[i]) + "\n")
        output_text += ("Marginea ritmica superioara: " + str(superior_rhythmic_borders[i]) + "\n")
        output_text += ("Diametrul ritmic: " + str(rhythmic_diameters[i]) + "\n\n")

    
    return output_text

def mihai_dinu(text):
    fragments = text.split("\n")
    create_dic()
    global nlp

    nlp = spacy.load("ro_core_news_sm")

    silabe, accent, len_phases, words_with_accent = syllable_split_and_accent(fragments)

    





#solomon_marcus("Adormite păsărele pe, la cuiburi se adună. Seara pe deal buciumul sună cu jale.")
#text = "Adormind de armonia\nCodrului bătut de gânduri."
#groups_vowels = vasile_vasile(text)

# print(groups_vowels)



        






