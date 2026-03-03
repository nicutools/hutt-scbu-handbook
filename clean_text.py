#!/usr/bin/env python3
"""Clean ligature breaks from PDF-extracted handbook text."""

import re

def clean_handbook(input_file, output_file):
    with open(input_file, 'r') as f:
        text = f.read()

    # 1. Remove orphaned ligature lines at page boundaries
    # Pattern: blank line, ligature fragment alone on line, blank line (repeated), page number, "Hu SCBU"
    # First remove blocks of orphaned ligatures + page numbers + headers
    text = re.sub(r'(\n\s*\n(?:(?:ti|tt|fi|fl|ff|ffi|ffl|tti)\s*\n\s*\n)+\d+\s*\nHu SCBU)', '\n', text)

    # Also remove any remaining standalone ligature lines (surrounded by blank lines)
    text = re.sub(r'\n\s*\n(ti|tt|fi|fl|ff|ffi|ffl|tti)\s*\n\s*\n', '\n\n', text)
    # Repeat to catch consecutive ones
    for _ in range(20):
        text = re.sub(r'\n\s*\n(ti|tt|fi|fl|ff|ffi|ffl|tti)\s*\n\s*\n', '\n\n', text)

    # Remove standalone page numbers (just a number on its own line between blank lines)
    text = re.sub(r'\n\s*\n(\d{1,3})\s*\n\s*\n', '\n\n', text)

    # Remove "Hu SCBU" page headers on their own line
    text = re.sub(r'\nHu SCBU\s*\n', '\n', text)
    # Also at start of file
    text = re.sub(r'^Hu SCBU\s*\n', '', text)

    # 2. Fix missing ligatures in words
    # The ligatures fi, fl, ff, ti, tt were stripped from words leaving a space
    # We fix by pattern: replace known broken fragments

    ligature_fixes = {
        # ti ligature (most common)
        ' ti ': ' ti ',  # preserve actual word boundaries - skip
        'ac ve': 'active',
        'ac vely': 'actively',
        'ac vi': 'activi',
        'addi ves': 'additives',
        'addi onal': 'additional',
        'admi ed': 'admitted',
        'admi ng': 'admitting',
        'administra on': 'administration',
        'a er': 'after',  # ft ligature? No - this is tt
        'alterna ve': 'alternative',
        'an bio': 'antibio',
        'an body': 'antibody',
        'an coagula': 'anticoagula',
        'an convulsant': 'anticonvulsant',
        'an gen': 'antigen',
        'an hypertensive': 'antihypertensive',
        'an microbial': 'antimicrobial',
        'an natal': 'antenatal',  # not a ligature issue but common
        'asymptoma c': 'asymptomatic',
        'a en on': 'attention',
        'a end': 'attend',
        'ausculta on': 'auscultation',
        'compa ble': 'compatible',
        'complica on': 'complication',
        'condi on': 'condition',
        'conjunc vi': 'conjunctivi',
        'con nue': 'continue',
        'con nuo': 'continuo',
        'con nuous': 'continuous',
        'correc on': 'correction',
        'defec ve': 'defective',
        'detec on': 'detection',
        'di er': 'differ',
        'diges ve': 'digestive',
        'dilata on': 'dilatation',  # not a ligature but common in source
        'distribu on': 'distribution',
        'documenta on': 'documentation',
        'dura on': 'duration',
        'e ect': 'effect',
        'eleva on': 'elevation',
        'enterocoli s': 'enterocolitis',
        'es mate': 'estimate',
        'evalua on': 'evaluation',
        'examina on': 'examination',
        'excre on': 'excretion',
        'expecta on': 'expectation',
        'func on': 'function',
        'gesta on': 'gestation',
        'iden fy': 'identify',
        'iden ca on': 'identification',
        'iden cal': 'identical',
        'immunisa on': 'immunisation',
        'implica on': 'implication',
        'indica on': 'indication',
        'indica ng': 'indicating',
        'indica ve': 'indicative',
        'infec on': 'infection',
        'informa on': 'information',
        'ini al': 'initial',
        'ini ate': 'initiate',
        'ini a ng': 'initiating',
        'intuba on': 'intubation',
        'inves ga': 'investiga',
        'irrita on': 'irritation',
        'isoimmmunisa on': 'isoimmunisation',
        'jaundice': 'jaundice',  # not broken
        'lacta on': 'lactation',
        'loca on': 'location',
        'manifesta on': 'manifestation',
        'matura on': 'maturation',
        'medica on': 'medication',
        'mee ng': 'meeting',
        'meningi s': 'meningitis',
        'mi ga': 'mitiga',
        'modifica on': 'modification',
        'monitoring': 'monitoring',  # not broken
        'mo on': 'motion',
        'mul ple': 'multiple',
        'necro sing': 'necrotising',
        'nutri on': 'nutrition',
        'observa on': 'observation',
        'opera on': 'operation',
        'op on': 'option',
        'orienta on': 'orientation',
        'Outpa ents': 'Outpatients',
        'outpa ent': 'outpatient',
        'oxida ve': 'oxidative',
        'pallia ve': 'palliative',
        'percen le': 'percentile',
        'posi on': 'position',
        'posi ve': 'positive',
        'prac ce': 'practice',
        'prac cal': 'practical',
        'preven on': 'prevention',
        'presen ng': 'presenting',
        'presenta on': 'presentation',
        'produc on': 'production',
        'propor on': 'proportion',
        'protec on': 'protection',
        'protec ve': 'protective',
        'ra o': 'ratio',
        'reac on': 'reaction',
        'reac ve': 'reactive',
        'recommenda on': 'recommendation',
        'reduc on': 'reduction',
        'regurgita on': 'regurgitation',
        'rela ve': 'relative',
        'repara on': 'reparation',
        'repe ve': 'repetitive',
        'resuscita on': 'resuscitation',
        'rou ne': 'routine',
        'satura on': 'saturation',
        'sec on': 'section',
        'selec ve': 'selective',
        'sensa on': 'sensation',
        'sensi ve': 'sensitive',
        'sensi vity': 'sensitivity',
        'separa on': 'separation',
        'signi cant': 'significant',
        'situa on': 'situation',
        'solu on': 'solution',
        'sta ng': 'stating',
        'S cky': 'Sticky',
        's cky': 'sticky',
        's gmata': 'stigmata',
        'subs tu': 'substitu',
        'symptoma c': 'symptomatic',
        'tachycardia': 'tachycardia',  # not broken
        'thermorregula on': 'thermoregulation',
        'transfusion': 'transfusion',  # not broken
        'ven la': 'ventila',
        'vomi ng': 'vomiting',
        'Introduc on': 'Introduction',
        'introduc on': 'introduction',
        'Resuscita on': 'Resuscitation',
        'resuscita on': 'resuscitation',
        'Intuba on': 'Intubation',
        'intuba on': 'intubation',
        'Nutri on': 'Nutrition',
        'nutri on': 'nutrition',
        'Gastrointes nal': 'Gastrointestinal',
        'gastrointes nal': 'gastrointestinal',
        'Necro sing': 'Necrotising',
        'necro sing': 'necrotising',
        'Conjunc vi s': 'Conjunctivitis',
        'conjunc vi s': 'conjunctivitis',
        'Haemoly c': 'Haemolytic',
        'haemoly c': 'haemolytic',
        'Dilata on': 'Dilatation',
        'ven la on': 'ventilation',
        'Ven la on': 'Ventilation',
        'ven lator': 'ventilator',
        'ca on': 'cation',  # careful - this is used in "classifi-cation" etc
        'preven ve': 'preventive',
        'quan ty': 'quantity',
        'quan es': 'quantities',
        'nega ve': 'negative',
        'primi ve': 'primitive',
        'cogni ve': 'cognitive',
        'alterna ve': 'alternative',
        'qualita ve': 'qualitative',
        'quan ta ve': 'quantitative',
        'repe ve': 'repetitive',
        'opera ve': 'operative',
        'norma ve': 'normative',
        'pre-opera ve': 'pre-operative',
        'post-opera ve': 'post-operative',
        'conserva ve': 'conservative',
        'forma on': 'formation',
        'malforma on': 'malformation',
        'absorp on': 'absorption',
        'consump on': 'consumption',
        'prescrip on': 'prescription',
        'descrip on': 'description',
        'assump on': 'assumption',
        'disrup on': 'disruption',
        'dysfunc on': 'dysfunction',
        'interac on': 'interaction',
        'protec on': 'protection',
        'restric on': 'restriction',
        'destruc on': 'destruction',
        'obstruc on': 'obstruction',
        'constric on': 'constriction',
        'contrac on': 'contraction',
        'retrac on': 'retraction',
        'extrac on': 'extraction',
        'frac on': 'fraction',
        'trac on': 'traction',
        'transi on': 'transition',
        'comple on': 'completion',
        'nutri onal': 'nutritional',
        'conven onal': 'conventional',
        'inten on': 'intention',
        'reten on': 'retention',
        'deten on': 'detention',
        'preven on': 'prevention',
        'inven on': 'invention',
        'interven on': 'intervention',
        'conges on': 'congestion',
        'diges on': 'digestion',
        'inges on': 'ingestion',
        'sugges on': 'suggestion',
        'ques on': 'question',
        'infesta on': 'infestation',
        'manifesta ons': 'manifestations',
        'complica ons': 'complications',
        'indica ons': 'indications',
        'examina ons': 'examinations',
        'inves ga ons': 'investigations',
        'recommenda ons': 'recommendations',
        'concentra on': 'concentration',
        'precipita on': 'precipitation',
        'irriga on': 'irrigation',
        'naviga on': 'navigation',
        'coagula on': 'coagulation',
        'agglu na on': 'agglutination',
        'thermoregula on': 'thermoregulation',
        'decontamina on': 'decontamination',
        'desatura on': 'desaturation',
        'supplementa on': 'supplementation',
        'implementa on': 'implementation',
        'interpreta on': 'interpretation',
        'determina on': 'determination',
        'approxima on': 'approximation',
        'rela onship': 'relationship',
        'compe ve': 'competitive',
        'sensi sa on': 'sensitisation',
        'immunoglobulin': 'immunoglobulin',
        'hepa s': 'hepatitis',
        'derma s': 'dermatitis',
        'encephali s': 'encephalitis',
        'arthri s': 'arthritis',
        'bursitis': 'bursitis',
        'peritoni s': 'peritonitis',
        'bronchioli s': 'bronchiolitis',
        'mastoidi s': 'mastoiditis',
        'retinopath': 'retinopath',
        'pa ent': 'patient',
        'Pa ent': 'Patient',
        'pa ents': 'patients',
        'iden fy': 'identify',
        'iden fied': 'identified',
        'iden es': 'identifies',
        'prac oner': 'practitioner',
        'prac oners': 'practitioners',
        'no fy': 'notify',
        'no fied': 'notified',
        'no fica on': 'notification',
        'jus fy': 'justify',
        'for fy': 'fortify',
        'for fied': 'fortified',
        'for fica on': 'fortification',
        'Iden fica on': 'Identification',
        'gesta onal': 'gestational',
        'occipito-frontal': 'occipito-frontal',
        'Fe al': 'Fetal',
        'fe al': 'fetal',
        'Le er': 'Letter',
        'le er': 'letter',
        'Ma er': 'Matter',
        'ma er': 'matter',
        'Pa ern': 'Pattern',
        'pa ern': 'pattern',
        'Se ng': 'Setting',
        'se ng': 'setting',
        'Se ngs': 'Settings',
        'se ngs': 'settings',
        'Bo le': 'Bottle',
        'bo le': 'bottle',
        'Li le': 'Little',
        'li le': 'little',
        'Be er': 'Better',
        'be er': 'better',
        'Wri en': 'Written',
        'wri en': 'written',
        'a empt': 'attempt',
        'permi ed': 'permitted',
        'admi ance': 'admittance',
        'intermi ent': 'intermittent',
        'a ached': 'attached',
        'a achment': 'attachment',
        're ects': 'reflects',
        're ected': 'reflected',
        're ect ': 'reflect ',
        're ex': 'reflex',
        're ux': 'reflux',
        'in amma': 'inflamma',
        'in uence': 'influence',
        'in ated': 'inflated',
    }

    # Apply specific word fixes
    for broken, fixed in ligature_fixes.items():
        text = text.replace(broken, fixed)

    # General pattern-based fixes for remaining ligature issues
    # Fix "ti" ligature: common suffix patterns
    ti_patterns = [
        (r'(\w)  on\b', r'\1tion'),      # _tion
        (r'(\w)  ons\b', r'\1tions'),     # _tions
        (r'(\w)  onal\b', r'\1tional'),   # _tional
        (r'(\w)  ng\b', r'\1ting'),       # _ting
        (r'(\w)  ve\b', r'\1tive'),       # _tive
        (r'(\w)  cal\b', r'\1tical'),     # _tical
        (r'(\w)  le\b', r'\1tile'),       # _tile (percentile etc)
        (r'(\w)  me\b', r'\1time'),       # _time
        (r'(\w)  fy\b', r'\1tify'),       # _tify
        (r'(\w)  ty\b', r'\1tity'),       # _tity
        (r'(\w)  es\b', r'\1ties'),       # _ties
        (r'(\w)  de\b', r'\1tide'),       # _tide (peptide etc)
        (r'(\w)  fy\b', r'\1tify'),
        (r'(\w)  ally\b', r'\1tially'),
    ]

    # Fix "ff" ligature (use word-boundary-aware patterns to avoid over-matching)
    ff_patterns = [
        (r'\be ect', r'effect'),
        (r'\be ort', r'effort'),
        (r'\ba ect', r'affect'),
        (r'\bdi er(?!e)', r'differ'),  # differ but not already fixed
        (r'\bo er\b', r'offer'),
        (r'\bo ered', r'offered'),
        (r'\bsu er', r'suffer'),
        (r'\bco ee', r'coffee'),
        (r'\bbu er', r'buffer'),
        (r'\be cac', r'efficac'),
        (r'\be cien', r'efficien'),
    ]

    # Fix "fl" ligature
    fl_patterns = [
        (r'\bre ect', r'reflect'),
        (r'\bre ux', r'reflux'),
        (r'\bin amma', r'inflamma'),
        (r'\bin uenc', r'influenc'),
        (r'\bin ow\b', r'inflow'),
        (r'\bout ow\b', r'outflow'),
        (r'\bover ow', r'overflow'),
        (r'\bcon ict', r'conflict'),
        (r'\b uid', r'fluid'),
        (r'(?<!\w) at\b(?=ten)', r'flat'),  # flatten only
        (r'\b ow\b', r'flow'),
        (r'\b uctuati', r'fluctuati'),
        (r'\b uoresce', r'fluoresce'),
    ]

    # Fix "fi" ligature
    fi_patterns = [
        (r'(\w) bre\b', r'\1fibre'),
        (r'(\w) brilla', r'\1fibrilla'),
        (r'(\w) brin', r'\1fibrin'),
        (r'(\w) rst\b', r'\1first'),
        (r'speci c', r'specific'),
        (r'bene t', r'benefit'),
        (r'bene cial', r'beneficial'),
        (r'de cien', r'deficien'),
        (r'de cit', r'deficit'),
        (r'de ned', r'defined'),
        (r'de ni ', r'defini'),
        (r'classi ', r'classifi'),
        (r'con rm', r'confirm'),
        (r'con den', r'confiden'),
        (r'con gur', r'configur'),
        (r'con ned', r'confined'),
        (r'identi ', r'identifi'),
        (r'modi ', r'modifi'),
        (r'noti ', r'notifi'),
        (r'pro le', r'profile'),
        (r'signi ', r'signifi'),
        (r'veri ', r'verifi'),
    ]

    # Fix "tt" ligature
    tt_patterns = [
        (r'a ach', r'attach'),
        (r'a empt', r'attempt'),
        (r'a end', r'attend'),
        (r'a en on', r'attention'),
        (r'bo le', r'bottle'),
        (r'bo om', r'bottom'),
        (r'bu on', r'button'),
        (r'commi ee', r'committee'),
        (r'fa y', r'fatty'),
        (r'fe al', r'fetal'),  # not tt but common
        (r'fi ed', r'fitted'),
        (r'fi ng', r'fitting'),
        (r'fla en', r'flatten'),
        (r'go en', r'gotten'),
        (r'ki en', r'kitten'),
        (r'le er', r'letter'),
        (r'li le', r'little'),
        (r'ma er', r'matter'),
        (r'pa ern', r'pattern'),
        (r'pre y', r'pretty'),
        (r'pu ng', r'putting'),
        (r'se le', r'settle'),
        (r'se ng', r'setting'),
        (r'spo ed', r'spotted'),
        (r'transmi', r'transmit'),
        (r'wri en', r'written'),
        (r'o ered', r'offered'),
        (r'su er', r'suffer'),
    ]

    # fl must run before ff to prevent "re ect" -> "reffect" instead of "reflect"
    all_patterns = fl_patterns + fi_patterns + ff_patterns + ti_patterns + tt_patterns
    for pattern, replacement in all_patterns:
        text = re.sub(pattern, replacement, text)

    # Fix "h ps://" -> "https://"  and "h p://" -> "http://"
    text = text.replace('h ps://', 'https://')
    text = text.replace('h p://', 'http://')

    # Fix "Hu " at start of proper nouns -> "Hutt "
    text = re.sub(r'\bHu (?=[A-Z])', 'Hutt ', text)
    text = re.sub(r'\bHu (?=Special|Valley|Hospital|SCBU)', 'Hutt ', text)

    # Fix common "tt" words
    text = text.replace('Hu Hospital', 'Hutt Hospital')
    text = text.replace('hu and', 'hutt and')  # username

    # Fix "Introduc on" pattern words that may have been missed
    text = re.sub(r'(\w) on\b(?=[\s,.\)\]:;])', lambda m: m.group(0), text)  # skip - too broad

    # Clean up multiple blank lines (more than 2 -> 2)
    text = re.sub(r'\n{3,}', '\n\n', text)

    # Clean up bullet point formatting: "•\n\n" -> "• "
    text = re.sub(r'•\s*\n\s*\n', '• ', text)
    text = re.sub(r'o\s*\n\s*\n(?=[A-Z])', '  - ', text)  # sub-bullets
    text = re.sub(r'▪\s*\n\s*\n', '    - ', text)  # sub-sub-bullets

    # Fix standalone "o" bullets that are sub-items (but be careful not to match actual words)
    # These appear as "o\n\n" at line starts

    with open(output_file, 'w') as f:
        f.write(text)

    print(f"Cleaned text written to {output_file}")
    print(f"Input: {len(open(input_file).readlines())} lines")
    print(f"Output: {len(open(output_file).readlines())} lines")

if __name__ == '__main__':
    clean_handbook('handbook_text.txt', 'handbook_clean.txt')
