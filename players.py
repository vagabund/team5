import re

import teams
from teams import Team


class Player:
    def __init__(self, name: str, team: Team, predict: tuple = ()):
        self.name = name
        self.team = team
        self.predict = predict

    def update_predict(self):
        with open("input.txt", 'r', encoding='cp1251') as f:
            lines = f.readlines()
        found_lines = []
        for line in lines:
            stripped = line.strip()
            match = re.match(r"^\s*\d+\.\s+(.+?)\s*\(", stripped)
            if not match:
                continue
            name_in_line = match.group(1).strip()
            if name_in_line == self.name:
                found_lines.append(stripped)
        if not found_lines:
            print(f"Прогноз для {self.name} не найден в input.txt")
            return
        last_line = found_lines[-1]
        if '(' not in last_line or ')' not in last_line:
            print(f"У {self.name} отсутствуют скобки в строке")
            return
        inline = last_line[last_line.rfind('(') + 1:last_line.rfind(')')]
        try:
            self.predict = tuple(map(int, inline.split('-')))
            print(f"Новый прогноз {self.name} - {self.predict}")
        except ValueError:
            raise ValueError("Невозможно преобразовать строку в прогноз")


fbtgenius = Player("FBTgenius", teams.monaco)
dan_ignatiev = Player("Даниил Игнатьев", teams.monaco)
vl_zinkovsky = Player("Владимир Зиньковский", teams.monaco)
algrtm = Player("AlGrTm22", teams.monaco)
ar_clementyev = Player("Артём Клементьев", teams.monaco)
maxvelo = Player("Maxvelo", teams.monaco)

mr_grigg = Player("MrGrigg182", teams.lucky_7)
tamb36 = Player("TAMB36", teams.lucky_7)
bogdan = Player("Богдан", teams.lucky_7)
pta = Player("Playing The Angel", teams.lucky_7)
sdryapko = Player("sdryapko", teams.lucky_7)
push = Player("Push", teams.lucky_7)

koch = Player("KoCH", teams.pentagon)
a_myagkova = Player("Anna Myagkova", teams.pentagon)
fabio = Player("Fabio", teams.pentagon)
wallker = Player("Wallker", teams.pentagon)
andorac = Player("andorac", teams.pentagon)
alexandre = Player("Алешандре", teams.pentagon)

sweetsky = Player("Sweetsky", teams.qed)
shinayar = Player("ShinaYar", teams.qed)
kiper1663 = Player("kiper1663", teams.qed)
joker_89 = Player("JOKER 89", teams.qed)
travakyr = Player("TRaBaKyR", teams.qed)
bvb_ultras = Player("BVB Ultras", teams.qed)

bons = Player("Bons", teams.san_marino)
m_dvornikov = Player("Михаил Дворников", teams.san_marino)
heops = Player("Хеопс", teams.san_marino)
morocco = Player("Morocco", teams.san_marino)
shummy = Player("Shummy", teams.san_marino)
hammer = Player("Hammer22", teams.san_marino)
emank = Player("Emank", teams.san_marino)


afscheid = Player("afscheid", teams.corleone)
south_russian = Player("south_russian", teams.corleone)
fanat4ik = Player("Fanat4ik", teams.corleone)
pahomov = Player("Лейтенант Пахомов", teams.corleone)
a_borisov = Player("Артём Борисов", teams.corleone)


snatch88 = Player("Snatch88", teams.hati)
o_kai = Player("o_kai", teams.hati)
staut = Player("Staut", teams.hati)
regys = Player("Regys", teams.hati)
rafa_benitez = Player("Rafa_Benitez", teams.hati)


jack_daniels = Player("Jack_Daniels", teams.radzi)
gol = Player("ГОЛ", teams.radzi)
dima_k = Player("DIMA_K", teams.radzi)
alex_20 = Player("Alex20", teams.radzi)
az = Player("AZ", teams.radzi)
michael = Player("Michael", teams.radzi)


x3 = Player("3X", teams.seldon)
kinzu = Player("КинЗю", teams.seldon)
roby_iz = Player("RobyIZ", teams.seldon)
sladim14 = Player("SlaDim14", teams.seldon)
oleg = Player("Олег", teams.seldon)
ip67 = Player("ip67pol", teams.seldon)


l_aksiutsin = Player("Leanid Aksiutsin", teams.lrsch)
r_fedorinin = Player("Роман Федоринин", teams.lrsch)
parabellum = Player("ParaBellum", teams.lrsch)
za_17 = Player("17za-raz", teams.lrsch)
a_golubev = Player("Андрей Голубев", teams.lrsch)
k_samkov = Player("Кирилл Самков", teams.lrsch)
tasman = Player("Tasman", teams.lrsch)
ewgen_88 = Player("Ewgen_88", teams.lrsch)


shred = Player("Shred", teams.stalevary)
v_gavdan = Player("Влад Гавдан", teams.stalevary)
n_lazutov = Player("Николай Лазутов", teams.stalevary)
billy93 = Player("billy93", teams.stalevary)
segys = Player("Segys", teams.stalevary)
s_kuchinsky = Player("Степан Кучинский", teams.stalevary)


asil756 = Player("asil756", teams.pro_vercelli)
wertal = Player("WERTAL", teams.pro_vercelli)
bogdan_22 = Player("Богдан22", teams.pro_vercelli)
dnipro83 = Player("dnipro83", teams.pro_vercelli)
om27 = Player("OM27", teams.pro_vercelli)


e_zhevora = Player("Егор Жевора", teams.supernova)
egorus = Player("egorus", teams.supernova)
recreated = Player("Recreated", teams.supernova)
drongo = Player("Дронго", teams.supernova)
alex_fanat_cska = Player("alex_fanat_cska", teams.supernova)
alex_brazhny = Player("Alex Brazhny", teams.supernova)


d_kupriyanov = Player("Дмитрий Куприянов", teams.avtobus)
e_goncharov = Player("Евгений Гончаров", teams.avtobus)
d_glukhov = Player("Дмитрий Глухов", teams.avtobus)
v_sutyrin = Player("Виктор Сутырин", teams.avtobus)
v_moiseenko = Player("Владимир Моисеенко", teams.avtobus)
s_baskin = Player("Сергей Баскин", teams.avtobus)


sokrat_57 = Player("Sokrat_57", teams.orion)
abejorro = Player("Abejorro", teams.orion)
olegnester = Player("OlegNester", teams.orion)
d_ratkevich = Player("Дмитрий Раткевич", teams.orion)
gooner_22 = Player("Gooner22", teams.orion)


v_kushta = Player("Влад Кушта", teams.legion)
dimas = Player("DimaS", teams.legion)
greg = Player("Greg", teams.legion)
rainbow = Player("Rainbow", teams.legion)
dimas2 = Player("Dimas", teams.legion)

players = [fbtgenius, dan_ignatiev, vl_zinkovsky, algrtm, ar_clementyev, mr_grigg, tamb36, bogdan, pta,
           sdryapko, koch, a_myagkova, fabio, wallker, andorac, sweetsky, shinayar, kiper1663, joker_89, travakyr,
           bons, m_dvornikov, heops, morocco, shummy, afscheid, south_russian, fanat4ik, pahomov, a_borisov,
           snatch88, o_kai, staut, regys, rafa_benitez, jack_daniels, gol, dima_k, alex_20, az, x3, kinzu,
           roby_iz, sladim14, oleg, l_aksiutsin, r_fedorinin, parabellum, za_17, a_golubev, shred, v_gavdan, n_lazutov,
           billy93, segys, asil756, wertal, bogdan_22, dnipro83, om27, e_zhevora, egorus, recreated, drongo,
           alex_fanat_cska, d_kupriyanov, e_goncharov, d_glukhov, v_sutyrin, v_moiseenko, sokrat_57, abejorro,
           olegnester, d_ratkevich, gooner_22, maxvelo, push, alexandre, bvb_ultras, emank, hammer, michael, ip67,
           k_samkov, tasman, s_kuchinsky, alex_brazhny, s_baskin, v_kushta, dimas, greg, rainbow, dimas2, ewgen_88]
