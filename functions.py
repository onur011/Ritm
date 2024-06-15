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
VOWELS = ['a', 'ă', 'â', 'e','î', 'i', 'o', 'u', 'A', 'Ă', 'Â', 'E', 'I','Î', 'O', 'U']
PUNCTUATION_MARKS = ['.', ',', '!', '?', ':', ';' , '-', '(', ')', '[', ']', '{', '}', "'", '"', '...', '“', '”', '/', '\\', '|', '_', '@', '#', '$', '%', '^', '&', '*', '~', '`', '<', '>', '=']
CONJ_SUB = ["să", "că", "dacă", "deși", "când", "cum", "ca", "pentru", "fie", "atât","încât"]
CONSONANTS = ['ț', 'ș', 'Ț', 'Ș','b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'p', 'q', 'r', 's', 't', 'v', 'w', 'x', 'y', 'z', 'B', 'C', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'X', 'Y', 'Z']
SO_O_VOWELS = ['a', 'o', 'ă', 'e']
CLOSE_VOWELS = ['â', 'i', 'u', 'î']
dictionary = {}
dic = pyphen.Pyphen(lang='ro_RO')

# Desparte textul in fraze
def split_phases(text):
    phases = []
    text = text.replace("\n", " ")

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
        elif (text[i] == '.') or (text[i] == '?') or (text[i] == '!')or (text[i] == '\n'):
            if one_phase.endswith('-'):
                one_phase = one_phase[:-1]
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

    for line in Lines:
        count += 1
        line = line.strip()

        words = line.split("\t")

        if words[0] in dictionary.keys():
            dictionary[words[0]][words[2][0]] = [words[3].replace(".","-"), words[4]]
        else:
            dictionary[words[0]] = {words[2][0] : [words[3].replace(".","-"), words[4]]}

def create_dic_perc(dict):
    total_count = sum(dict.values())
    percentage_frequencies = {k: round((v / total_count) * 100, 2) for k, v in dict.items()}
    percentage_frequencies = {k: v for k, v in sorted(percentage_frequencies.items(), key=lambda item: item[1], reverse=True)}
    return percentage_frequencies

def update_freq(frequency_dict, element):
    if element in frequency_dict:
        frequency_dict[element] += 1
    else:
        frequency_dict[element] = 1

def accentuate(syllables):
    syllables_copy = syllables.copy()
    if len(syllables_copy) < 2:
        syllable_copy = syllables_copy[0]
        for i, char in enumerate(syllable_copy):
            if char in VOWELS:
                syllables_copy[0] = syllable_copy[:i] + "'" + syllable_copy[i:]
                break
        return ''.join(syllables_copy)
    
    penultimate_syllable = syllables_copy[-2]
    for i, char in enumerate(penultimate_syllable):
        if char in VOWELS:
            syllables_copy[-2] = penultimate_syllable[:i] + "'" + penultimate_syllable[i:]
            break
    
    return ''.join(syllables_copy)

def process_word(word):

    syllables = dic.inserted(word,hyphen="^")
    syllables = syllables.split("^")
    if "-" in syllables:
        syllables = [x for x in syllables if x != "-"]

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
            current_token = token.text.lower()

            if current_token.startswith('-') and len(current_token) > 1:
                current_token = current_token[1:]
            if current_token.endswith('-') and len(current_token) > 1:
                current_token = current_token[:-1]

            if token.pos_ not in ['PUNCT', 'SYM', 'X']:
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
                    accent = dictionary[current_token][key][1]
                else:
                    syll, accent = process_word(current_token)
                    
                paragraf_syll.append(syll)

                if current_token in PRON_REFLEXIV or current_token in CONJ_SUB:
                    for _ in syll:
                        paragraf_accent.append(0)
                    words_with_accent.append(0)
                elif "'" in accent and token.pos_ not in ['DET', 'CONJ', "CCONJ", "SCONJ", "ADP", "PRON"]:
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
                            

                elif token.pos_ not in ['DET', 'CONJ', "CCONJ", "SCONJ", "ADP", "PRON"]:
                    paragraf_accent.append(1)
                    words_with_accent.append(1)
                else:
                    for _ in syll:
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

def calculate_frequencies(lst): 
    frequencies = {}
    total_count = 0

    for element in lst:
        total_count += 1
        if element in frequencies:
            frequencies[element] += 1
        else:
            frequencies[element] = 1

    percentage_frequencies = {k: round((v / total_count) * 100, 2) for k, v in frequencies.items()}
    percentage_frequencies = {k: v for k, v in sorted(percentage_frequencies.items(), key=lambda item: item[1], reverse=True)}
    return percentage_frequencies

def format_frequencies(name, frequency_dict):
    result = name + "\n" 
    for element, frequency in frequency_dict.items():
        result += str(element) + " : " + str(frequency) + "%\n"
    
    return result

def vasile_vasile(text, choice):
    fragments = None
    if choice == 'vers':
        fragments_aux = text.split("\n")
        fragments = [sublist for sublist in fragments_aux if sublist]
    if choice == 'frază':
        fragments = split_phases(text)
    
    type_group_freq = {}
    group_freq = {}

    line_groups_vowels = []
    for line in fragments:
        groups_vowels = []
        aux_group = []
        aux_group_sort = []
        count_vowels = 0
        for i in range(0, len(line)):
            if count_vowels == 3:
                groups_vowels.append(aux_group)
                aux_group = []
                aux_group_sort = sorted(aux_group_sort)
                update_freq(group_freq, ''.join(aux_group_sort))
                if (((aux_group_sort[0] in CLOSE_VOWELS) and (aux_group_sort[1] in CLOSE_VOWELS)) or
                    ((aux_group_sort[1] in CLOSE_VOWELS) and (aux_group_sort[2] in CLOSE_VOWELS)) or
                    ((aux_group_sort[0] in CLOSE_VOWELS) and (aux_group_sort[2] in CLOSE_VOWELS))):
                    update_freq(type_group_freq, "închise")
                else:
                    update_freq(type_group_freq, "semi/deschise")
                aux_group_sort = []
                count_vowels = 0
            if line[i] in VOWELS:
                count_vowels += 1
                aux_group.append(line[i])
                aux_group_sort.append(line[i].lower())
            elif (count_vowels > 0) and (line[i] in CONSONANTS):
                aux_group.append('-')
        if count_vowels == 3:
            groups_vowels.append(aux_group)
            aux_group = []
            count_vowels = 0
        line_groups_vowels.append(groups_vowels)

    output_text = ""
    for i in range(0, len(fragments)):
        output_text += (fragments[i] + "\n")
        output_text += (' | '.join([' '.join(sublist) for sublist in line_groups_vowels[i]]) + "\n\n")

    output_text += (format_frequencies("Frecvență grupuri", create_dic_perc(group_freq)) + "\n")
    output_text += format_frequencies("Frecvență tip grup", create_dic_perc(type_group_freq))

    return output_text
    
def solomon_marcus(text, choice):
    fragments = None
    if choice == 'vers':
        fragments_aux = text.split("\n")
        fragments = [sublist for sublist in fragments_aux if sublist]
    if choice == 'frază':
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

    len_phi_freq = calculate_frequencies(len_phi)
    rhythmic_indices_freq = calculate_frequencies(rhythmic_indices)
    lower_rhythmic_borders_freq = calculate_frequencies(lower_rhythmic_borders)
    superior_rhythmic_borders_freq = calculate_frequencies(superior_rhythmic_borders)
    rhythmic_diameters_freq = calculate_frequencies(rhythmic_diameters)
    
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
        output_text += ("Structura ritmică = <" + ", ".join(map(str, rhythmic_structure[i])) + ">\n")
        output_text += ("Lungimea ritmică = " + str(len_phi[i]) + "\n")
        output_text += ("Indicele ritmic = " + str(rhythmic_indices[i]) + "\n")
        output_text += ("Marginea ritmică inferioară = " + str(lower_rhythmic_borders[i]) + "\n")
        output_text += ("Marginea ritmică superioară = " + str(superior_rhythmic_borders[i]) + "\n")
        output_text += ("Diametrul ritmic = " + str(rhythmic_diameters[i]) + "\n\n")

    output_text += ("Marginea inferioară a limbajului = " + str(min(lower_rhythmic_borders)) + "\n")
    output_text += ("Marginea superioară a limbajului = " + str(max(superior_rhythmic_borders)) + "\n")
    output_text += ("Diametrul ritmic al limbajului = " + str(max(rhythmic_diameters)) + "\n")
    output_text += ("Dimensiunea ritmică a limbajului = " + str(max(superior_rhythmic_borders) - min(lower_rhythmic_borders)) + "\n\n")

    output_text += (format_frequencies("Frecvență lungime ritmică", len_phi_freq) + "\n")
    output_text += (format_frequencies("Frecvență indice ritmic", rhythmic_indices_freq) + "\n")
    output_text += (format_frequencies("Frecvență margine ritmică inferioară", lower_rhythmic_borders_freq) + "\n")
    output_text += (format_frequencies("Frecvență margine ritmică superioară", superior_rhythmic_borders_freq) + "\n")
    output_text += format_frequencies("Frecvență diametru ritmic", rhythmic_diameters_freq)


    
    return output_text

def remove_punctuation(nested_list):
    for sublist in nested_list:
        i = 0
        while i < len(sublist):
            if isinstance(sublist[i], list) and len(sublist[i]) == 1 and sublist[i][0] in PUNCTUATION_MARKS:
                punctuation = sublist[i][0]
                j = i + 1
                while j < len(sublist) and isinstance(sublist[j], list) and len(sublist[j]) == 1 and sublist[j][0] in PUNCTUATION_MARKS:
                    punctuation += sublist[j][0]
                    sublist[j] = []
                    j += 1
                if i > 0:
                    sublist[i - 1][-1] += punctuation
                sublist[i] = []
            i += 1
    return [[item for item in sublist if item] for sublist in nested_list]

def flatten_and_remove_empty(nested_list):
    return [[item for sublist in inner_list if sublist for item in sublist] for inner_list in nested_list]

def mihai_dinu(text, choice):
    fragments = None
    if choice == 'vers':
        fragments_aux = text.split("\n")
        fragments = [sublist for sublist in fragments_aux if sublist]
    if choice == 'frază':
        fragments = split_phases(text)

    create_dic()
    global nlp

    nlp = spacy.load("ro_core_news_sm")

    silabe, accent, len_phases, words_with_accent = syllable_split_and_accent(fragments)
    
    silabe = remove_punctuation(silabe)
    words_with_accent = flatten_and_remove_empty(words_with_accent)

    all_phase_accent = []
    
    for i in range(0, len(silabe)):
        accent_index = 0
        phase_accents = []
        for word in silabe[i]:
            word_accents = []
            for syllable in word:

                if syllable not in PUNCTUATION_MARKS:
                    word_accents.append(accent[i][accent_index])
                    accent_index += 1
            phase_accents.append(word_accents)
        all_phase_accent.append(phase_accents)

    units_syll = []
    units_accent = []

    for i in range(0, len(words_with_accent)):
        syll_one_phase = []
        accent_one_phase = []
        syll_one_unit = []
        accent_one_unit = []
        for words_accent, word_syll, word_syll_acc in zip(words_with_accent[i], silabe[i], all_phase_accent[i]):

            if words_accent == 1:
                syll_one_unit.append(word_syll)
                syll_one_phase.append(syll_one_unit)
                syll_one_unit = []

                accent_one_unit.append(word_syll_acc)
                accent_one_phase.append(accent_one_unit)
                accent_one_unit = []
            else:
                syll_one_unit.append(word_syll)

                accent_one_unit.append(word_syll_acc)
        
        if len(syll_one_unit) != 0:
            if len(accent_one_phase) > 0:
                accent_one_phase[-1] += accent_one_unit
                syll_one_phase[-1] += syll_one_unit
            else:
                accent_one_phase.append(accent_one_unit)
                syll_one_phase.append(syll_one_unit)

        units_syll.append(syll_one_phase)
        units_accent.append(accent_one_phase)

    output = ""

    len_freq = {}
    rang_freq = {}
    distance_freq = {}
    rhythm_type_freq = {}
    measure_freq = {}
    verse_type_freq = {}


    for i in range(0, len(units_syll)):
        phase_unit_len = []
        phase_unit_rang = []
        phase_unit_distance = []
        for j in range(0, len(units_syll[i])):
            unit_len = 0
            unit_rang = 0
            for k in range(0, len(units_syll[i][j])):

                word = ""
                for syll, acc in zip(units_syll[i][j][k], units_accent[i][j][k]):
                    if acc == 1:
                        word += "#"
                    word += syll + "-"

                word = word.rstrip('-')

                output += (word + " ")

                for l in range(0, len(units_syll[i][j][k])):
                    unit_len += 1
                    if units_accent[i][j][k][l] == 1:
                        unit_rang = unit_len
                
            output += " | "
            phase_unit_len.append(unit_len)
            phase_unit_rang.append(unit_rang)

        output = (output[:-2] + '\n\n')
        for j in range(0, len(units_syll[i])):
            output += ("Lungime_" + str(j+1) + " = " + str(phase_unit_len[j]) + "    " + "Rang_" + str(j+1) + " = " + str(phase_unit_rang[j]) + "\n")
            update_freq(len_freq, phase_unit_len[j])
            update_freq(rang_freq, phase_unit_rang[j])

        for j in range(0, len(units_syll[i]) - 1):
            phase_unit_distance.append(phase_unit_len[j] - phase_unit_rang[j] + phase_unit_rang[j+1])
            output += ("Distanță_"+ str(j+1) + "_" + str(j+2) + " = " + str(phase_unit_distance[j]) + "\n")
            update_freq(distance_freq, phase_unit_distance[j])

        rhythm_freq = [0, 0, 0]
        for d in phase_unit_distance:
            if d % 4 == 0:
                rhythm_freq[2] += 1
            elif d % 3 == 0:
                rhythm_freq[1] += 1
            elif d % 2 == 0:
                rhythm_freq[0] += 1

        max_index = rhythm_freq.index(max(rhythm_freq))
        rhythm_type = None
        if max_index == 0:
            rhythm_type = 2
            output += "Ritm predominant binar.\n" 
        elif max_index == 1:
            rhythm_type = 3
            output += "Ritm predominant ternar.\n"
        elif max_index == 2:
            rhythm_type = 4
            output += "Ritm predominant cuaternar.\n"
        update_freq(rhythm_type_freq, rhythm_type)
        
        measure = sum(phase_unit_len)
        update_freq(measure_freq, measure)

        output += "Măsura = " + str(measure) + "\n"
        
        if measure % rhythm_type == 0:
            output += "Vers acatalectic.\n\n"
            update_freq(verse_type_freq, "acatalectic")
        else:
            output += "Vers catalectic.\n\n"
            update_freq(verse_type_freq, "catalectic")

    output += (format_frequencies("Frecvență lungime", create_dic_perc(len_freq)) + "\n")
    output += (format_frequencies("Frecvență rang", create_dic_perc(rang_freq)) + "\n")
    output += (format_frequencies("Frecvență distanță", create_dic_perc(distance_freq)) + "\n")
    output += (format_frequencies("Frecvență ritm", create_dic_perc(rhythm_type_freq)) + "\n")
    output += (format_frequencies("Frecvență măsură", create_dic_perc(measure_freq)) + "\n")
    output += format_frequencies("Frecvență vers", create_dic_perc(verse_type_freq))

    return output





            
    
        
    





#solomon_marcus("Adormite păsărele pe, la cuiburi se adună.\nSeara pe deal buciumul sună cu jale.")
#text = "Adormind de armonia\nCodrului bătut de gânduri."
#groups_vowels = mihai_dinu(text)

# print(groups_vowels)



        






