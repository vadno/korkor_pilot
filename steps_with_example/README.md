An example file is led through the whole process. In each step the format of the input and the output file is given as well as the tool/script used. In certain steps the modules of [emtsv](https://github.com/dlt-rilmta/emtsv) have to be used, while in others scripts that can be found [here](../scripts).

1. processing with emtsv

   To process the raw texts the following modules of [emtsv](https://github.com/dlt-rilmta/emtsv) have to be used:

   1. tokenization: emtoken (tok)
   2. morphological analysis: emmorph (morph)
   3. disambiguation and lemmatization: emtag (pos)

   Modules can be set separately, but preset `tok-pos` runs exactly the same setup. Find more information about emtsv [here](https://github.com/dlt-rilmta/emtsv)!

   input: raw text [0_exmlp_raw/globv_10.txt](0_exmlp_raw/globv_10.txt)   
   output: xtsv  
    
2. preprocessing the file for manual correction

   The output of emtsv has to be preprocessed to be the input for a prepared Google spreadsheet containing conditional formatting.

   Preprocessing script: [tag_preproc.py](../scripts/tag_preproc.py)  
   input: xtsv  [1_emtsv/globv_10.xtsv](1_emtsv/globv_10.xtsv)  
   output: tsv for Google spreadsheets  
    
3. manual correction in Google spreadsheets

   Human annotators check and correct tokenization and disambugiation (morphological tags and lemmata) in Google spreadsheets.

   Next to the tokens, below the disambiguated morphological tag and lemma, all the possible lemma-morphological tag pairs are listed. The annotation task here is to decide if the disambiguated tag-lemma pair is correct. If not, they can choose from the other tag-lemma pairs or enter the correct ones manually. The spreadsheet allows to correct also the tokenization. For further details see the [annotation guidelines](../guidelines/emmorph_checker_guide.pdf)!

   The empty spreadsheet file: [emtag.xlsx](../google_spreadsheets_files/emtag.xlsx)

   The empty file can be imported into Microsoft Excel and Libre Office next to Google Spreadsheets.

   input: tsv, file with conditional formatting, importing [2_google_preproc/globv_10.tsv](2_google_preproc/globv_10.tsv)  
   output: exported csv
    
4. processing the file from Google spreadsheets

   In this step the exported csv file is processed and prepared for the next step, the dependency analysis. The script takes the tags and lemma corrected by the human annotator, and it processes the commands for correcting tokenization errors (deletes a row or inserts one with the content given by the annotator). The script makes format conversion as well, so the output is in exactly the same format as before the manual correction (after the step 1_emtsv), it differs only in the content of certain cells.

   Postprocessing script: [tag_postproc.py](../scripts/tag_postproc.py)

   input: csv  [3_google_kezi/globv_10.csv](3_google_manual/globv_10.csv)  
   output: xtsv
    
5. processing with emtsv

   For dependency analysis the following modules of [emtsv](https://github.com/dlt-rilmta/emtsv) have to be used. These modules are responsible for tag conversion and format conversion next to dependency analysis.

   1. tag conversion: emmorph2ud (conv-morph)
   1. dependency analysis: emdep (dep)
   1. format conversion: emconll (conll)

   Find more information about emtsv [here](https://github.com/dlt-rilmta/emtsv)!

   input: xtsv  [4_google_posztproc/globv_10.xtsv](4_google_posztproc/globv_10.xtsv)  
   output: conll-u
    
6. preprocessing the file for WebAnno

   This step is a format conversion for [WebAnno](https://webanno.github.io/webanno/). The conversion is made by a short command:

    ```
    cat [file] | awk -F $'\t' ' { t = $4; $4 = $5; $5 = t; print; } ' OFS=$'\t'
   ```
   
   input: conll-u  [5_emtsv/globv_10.conll](5_emtsv/globv_10.conll)  
   output: conll-u for WebAnno
    
7. manual correction in WebAnno  
   
   In this step human annotators check and correct the output of the dependency analysis. The annotators work in [WebAnno](https://webanno.github.io/webanno/). For further details see the [annotation guidelines](../guidelines/emdep_checker_guide.pdf)! Az annotátorok által összegyűjtött kérdésekből készült [gyik](../guidelines/emdep_checker_faq.pdf) is segítséget nyújthat az kérdéses esetekben.

   input: conll-u  [6_webanno_preproc/globv_10.conll](6_webanno_preproc/globv_10.conll)  
   output: conll-u
    
8. inserting zero verbs and zero substantives in [Annotatrix](https://github.com/jonorthwash/ud-annotatrix) 

    Ebben a lépésben az esetleges tokenizálási hibák javítása mellett a zéró létigék és az elliptált igék kézi beillesztése történik. Ehhez az [UD Annotatrix](https://github.com/jonorthwash/ud-annotatrix) eszközt használjuk, amely egy böngészőben használható eszköz függőségi fák vizualizációjára és szerkesztésére.

    For further details see the [annotation guidelines](../guidelines/zero_verb_guide.pdf)!

    input: conll-u  [7_webanno_kezi/globv_10.conll](7_webanno_manual/globv_10.conll)  
    output: conll-u

9. inserting zero pronouns  

   In this step a script inserts zero pronouns into the file. The simple rule-based script relies on the content of the other nnotation layers (lemma, morphological tag, dependency relations).  After inserting zero pronouns extra branches might appear in the dependency tree.

   Script inserting zero pronouns: [pro.py](../scripts/pro.py)
     
   input: conll-u   [8_zeroige_kezi/globv_10.conll](8_zeroverb_manual/globv_10.conll)  
   output: conll-u
    
10. inserting anaphora relations

    In this step a script inserts anaphora relations. The simple rule-based script searches for the personal pronouns and decides on the base of the other tokens and their morphological and syntactical features.  
    The antecedent of all other pronoun types have to be inserted manually in the next step.
   
    Script insetring anaphora relation: [anafora.py](../scripts/anafora.py)

    input: conll-u  [9_pro_beszuro/globv_10.conll](9_pro_insert/globv_10.conll)  
    output: conll-u
    
11. manual correction and inserting coreference relations in Google spreadsheets  
   Az automatikusan beillesztett zérónévmások és anaforikus kapcsolatok ellenőrzését, valamint a koreferenciakapcsolatok beillesztését egyfeltételes formázásokkal ellátott Google Spreadsheets táblázatban lehet elvégezni. Az anaforikus- és koreferenciakapcsolatokat két oszlopban kell jelölni, egyikben annak az elemnek az ID számát kellett megadni, amellyel a visszautaló elem kapcsolatban áll, a másikban pedig a kapcsolat típusát. For further details see the [annotation guidelines](../guidelines/koref_annot_guide.pdf)!  
   
   The empty spreadsheet file: [coref.xlsx](../google_spreadsheets_files/coref.xlsx)  
   
   The empty file can be imported into Microsoft Excel and Libre Office next to Google Spreadsheets.

   input: tsv, file with conditional formatting, importing [10_anaphora_insert/globv_10.conll](10_anaphora_insert/globv_10.conll)  
   output: exported tsv

12. processing the file from Google spreadsheets 

    In this step a script processes the exported tsv file. The script processes not only the content of the columns respect for anaphora and coreference relations, but the content of all the other columns as well, because the annotators can find errors e.g. in the morphological tags as well. The script makes format conversion as well, the output is in the format of emtsv.

    Postprocessing script: [coref_postproc.py](../scripts/coref_postproc.py)

    input: tsv  [11_google_manual/globv_10.tsv](11_google_manual/globv_10.tsv)  
    output: xtsv
    
13. final conversion of the corpus files

    In this step the morphological analysis layer cut in step 6_webanno_prepoc is merged into the file.

    Script for merge: [merge.py](../scripts/merge.py)

    inputs:
    1. first argument: xtsv [4_google_posztproc/globv_10.xtsv](4_google_posztproc/globv_10.xtsv) ( 4_googe_posztproc lépés kimeneteként kapott fájl).
    1. second argument: xtsv  [12_google_posztproc/globv_10.xtsv](12_google_posztproc/globv_10.xtsv)  
     
    output: xtsv
