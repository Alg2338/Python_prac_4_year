import re
import os

lines = []

dictionary = {'var_1_1.tex': 'new_1.tex', 'var_1_2.tex': 'new_2.tex', 'var_1_3.tex': 'new_3.tex'}
for old, new in dictionary.items():
    with open(old, 'r+') as fp:
        with open(new, 'a+') as fp_new:
            lines = fp.readlines()
            row = "References"

            for index, line in enumerate(lines):
                if row in line:
                    res_index = index
                    break
            fp_new.writelines("\\documentclass[a4paper,12pt]{article}\n\\usepackage{cmap}\n\\usepackage[T2A]{fontenc}\n\\usepackage[utf8]{inputenc}\n\\usepackage[english,russian]{babel}")
            if old == 'var_1_2.tex':
                fp_new.writelines("\n\n\\newcommand\\Pfaff{Pfaff\kern.1em}\n")
                new_s = "".join(lines[res_index + 1:]).split('\n\\bib\n')
            else:
                fp_new.writelines("\n\n\\newcommand\\AW{Addison\\kern.1em--Wesley}")
                new_s = "".join(lines[res_index + 1:]).split('\n\\smallskip\n\\bib\n')
            fp_new.writelines("\n\n\\begin{document}\n")
        
            for i in range(len(new_s)):
                new_s[i] = re.sub(r'(\\bf\s?\d+)', r'V. \1' , new_s[i]) # Том
            
                new_s[i] = re.sub(r'\s?(\d+--\d+)', r' pp. \1' , new_s[i]) # Страницы
                pages = re.findall(r'(\d+--\d+)', new_s[i])
                
                year = re.findall(r' \(\d{4}\)', new_s[i]) #Год в виде (1987)
                for j in range(len(year)):
                    year[j] = ", " + year[j][2:-1] + "."
                    if year[j] != ', .':
                        new_s[i] = re.sub(r' \(\d{4}\)', "", new_s[i])
                        new_s[i] = re.sub(pages[j] + r'\.', pages[j] + year[j], new_s[i])

                year_exp = re.findall(r'\(\d{4}\)\,', new_s[i]) #Когда год в виде (1987)
                for j in range(len(year_exp)):
                        year_exp[j] = ", " + year_exp[j][1:-2] + "."
                        new_s[i] = re.sub(r'\n\(\d{4}\)\,', ",", new_s[i])
                        new_s[i] = re.sub(r'\.\n', year_exp[j], new_s[i])
                        
                #year = ", " + "".join(re.findall(r' \(\d{4}\)', new_s[i]))[2:-1] + "." #Год в виде (1987)
                #if year != ', .':
                    #new_s[i] = re.sub(r' \(\d{4}\)', "", new_s[i])
                    #new_s[i] = re.sub(pages[0] + r'\.', pages[0] + year, new_s[i])

                replace_match_1 = lambda x: '{}. {} {}'.format(x[1][0], x[2], x[3])
                replace_match_2 = lambda x: '{}. {}{}'.format(x[1][0], x[2], x[3])
                replace_match_3 = lambda x: '{}. {} {} {}'.format(x[1][0], x[2], x[3], x[4])
                replace_match_4 = lambda x: '{}.-{}.~{}'.format(x[1][0], x[2][0], x[3])

                new_s[i] = re.sub(r'\\Pfaff\/ian', r'Pfaff', new_s[i])

                new_s[i] = re.sub(r'([A-Z]\w+) ([A-Z]\.) ([A-Z]\w+)', replace_match_1, new_s[i])

                new_s[i] = re.sub(r'([A-Z]\w+) (\{?\\?[A-Z]\}?\w+)(\,| and)', replace_match_2, new_s[i])
            
                new_s[i] = re.sub(r'([A-Z]\w+) ([A-Z]\.) ([A-Z]\.) ([A-Z]\w+)', replace_match_3, new_s[i])

                new_s[i] =  re.sub(r'([A-Z]\w+)-([A-Z]\w+) ([A-Z]\w+)', replace_match_4, new_s[i])

                new_s[i] = re.sub(r'\[\\\w+\](\n| )', "{" + repr(i) + "} ", new_s[i])

                #print(new_s[i])
            fp_new.writelines("\n\\begin{thebibliography}{99}\n")
            res = '\n\\bibitem'.join(new_s)
            res = re.sub(r'\\end|\\bye', "", res)

            fp_new.writelines(res)
            fp_new.writelines("\n\\end{thebibliography}\n\\end{document}")


'''text = "Mathematics\\/ \\bf 7} (1957), 1073--1082.\n"
print(text)
text = re.sub(r'(\\bf\s?\d+)', r'V.\1' , text) # Том
text = re.sub(r'(\d+--\d+)', r'pp.\1' , text) # Страницы
year = ", " + "".join(re.findall(r' \(\d{4}\)', text))[2:-1] + "." #Год в виде (1987)
text = re.sub(r' \(\d{4}\)', "", text)
text = re.sub(r'\.\n', year, text)
print(text)

replace_match_1 = lambda x: '{}.~{}~{}'.format(x[1][0], x[2], x[3])
replace_match_2 = lambda x: '{}.~{}{}'.format(x[1][0], x[2], x[3])
replace_match_3 = lambda x: '{}.~{}~{}~{}'.format(x[1][0], x[2], x[3], x[4])
replace_match_4 = lambda x: '{}.-{}. {}'.format(x[1][0], x[2][0], x[3])
replace_match_5 = lambda x: '{}.~{}'.format(x[1][0], x[2])

text_2 = 'Andreas W. Dress and Walter Wenzel,'
name = re.sub(r'([A-Z]\w+) ([A-Z]\.) ([A-Z]\w+)', replace_match_1, text_2)
print(name)

text_3 = 'Svante Janson, Donald E. Knuth, Tomasz {\L}uczak, and Boris Pittel,'
name_3 = re.sub(r'([A-Z]\w+) (\{?\\?[A-Z]\}?\w+)(\,| and)', replace_match_2, text_3)
print(name_3)

text_4 = 'Andreas W. M. Dress and Walter Wenzel,'
name_4 = re.sub(r'([A-Z]\w+) ([A-Z]\.) ([A-Z]\.) ([A-Z]\w+)', replace_match_3, text_4)
print(name_4)

text_5 = 'Ira Gessel and Da-Lun Wang.'
name_5 =  re.sub(r'([A-Z]\w+)-([A-Z]\w+) ([A-Z]\w+)', replace_match_4, text_5)
print(name_5)

text_6 = '[\Kiii] D. E. Knuth'
name_6 = re.sub(r'\[\\\w+\](\n| )', repr(1), text_6)
print(name_6)

text_7 = 'L\'aszl\'o Lov\'asz'
name_7 = re.sub(r'L\'aszl\'o Lov\'asz', r'Lib Lov\'asz', text_7)
print(name_7)'''
