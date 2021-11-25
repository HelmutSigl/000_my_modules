#!/usr/bin/python3
# ------------------------------
# datei: hs_vaping.py
# autor: Helmut Sigl
# datum: 25/11/2021
# ------------------------------

# Imports

# Definitions

class Liquid:

    def __init__(self,  p_menge_ml = 0,    p_vg_prozent = 0, 
                        p_pg_prozent = 0,  p_nic_mg_p_ml = 0):
        # Übernahme, Check und Berechnung
        self.set(p_menge_ml, p_vg_prozent, p_pg_prozent, p_nic_mg_p_ml)
        
    def set(self,   p_menge_ml = 0,    p_vg_prozent = 0,
                    p_pg_prozent = 0,  p_nic_mg_p_ml = 0):
        # Vorbelegungen
        self.fehler = ''
        # Übernahme
        self.menge_ml = round(p_menge_ml,2)
        self.vg_prozent = round(p_vg_prozent,2)
        self.pg_prozent = round(p_pg_prozent,2)
        self.nic_mg_p_ml = round(p_nic_mg_p_ml,2)
        # Check auf Plausibilität
        self.__check()
        # Berechnungen
        self.__calc()

    def state(self):
        if self.fehler == '': ret = True
        else: ret = False
        return ret

    def data(self):
        ret = (round(self.menge_ml, 2), round(self.vg_prozent, 2), round(self.pg_prozent, 2), round(self.nic_mg_p_ml, 2))
        return ret

    def message(self):
        if self.fehler == '':
            ret = 'Aktuell liegt kein Fehler vor'
        else:
            ret = self.fehler
        return ret

    def ausgabe(self):
        ret = ''
        if self.fehler == '':
            ret += str(self.menge_ml) + ' ml --- '
            ret += str(self.vg_prozent) + ' / ' + str(self.pg_prozent) + ' --- '
            ret += str(self.nic_mg_p_ml) + ' mg/ml'
        else:
            ret += self.fehler 
        return ret

    def __check(self):
        if self.menge_ml > 0:
            if (self.vg_prozent + self.pg_prozent) == 100:
                pass
            else: self.fehler = 'Menge VG in % + Menge PG in % muss 100% ergeben!'
        else: self.fehler = 'Die Menge muss größer Null sein!'

    def __calc(self):
        if self.fehler == '':
            self.vg_ml = self.menge_ml / 100 * self.vg_prozent
            self.pg_ml = self.menge_ml / 100 * self.pg_prozent
            self.nic_mg = self.nic_mg_p_ml * self.menge_ml
        else: pass
    
    def __add__(self, other):
        ret = Liquid()
        if isinstance(other, Liquid):
            if self.state():
                if other.state():
                    menge_ml = self.menge_ml + other.menge_ml
                    vg_ml = self.vg_ml + other.vg_ml
                    pg_ml = self.pg_ml + other.pg_ml
                    nic_mg = self.nic_mg + other.nic_mg
                    nic_mg_p_ml = nic_mg / menge_ml
                    vg_prozent = vg_ml * 100 / menge_ml
                    pg_prozent = pg_ml * 100 / menge_ml
                    ret.set(menge_ml, vg_prozent, pg_prozent, nic_mg_p_ml)
                else: ret.fehler = 'add: Fehler im rechten Term'
            else: ret.fehler = 'add: Fehler im linken Term'
        else: ret.fehler = 'add: Rechter Term ist kein Liquid-Objekt'
        return ret
        
    def __sub__(self, other):
        ret = Liquid()
        if isinstance(other, Liquid):
            if self.state():
                if other.state():
                    if self.menge_ml > other.menge_ml:
                        menge_ml = self.menge_ml - other.menge_ml
                        vg_ml = self.vg_ml - other.vg_ml
                        pg_ml = self.pg_ml - other.pg_ml
                        nic_mg = self.nic_mg - other.nic_mg
                        nic_mg_p_ml = nic_mg / menge_ml
                        vg_prozent = vg_ml * 100 / menge_ml
                        pg_prozent = pg_ml * 100 / menge_ml
                        ret.set(menge_ml, vg_prozent, pg_prozent, nic_mg_p_ml)
                    else: ret.fehler = 'sub: Rechter Term ist größer oder gleich linker Term'
                else: ret.fehler = 'sub: Fehler im rechten Term'
            else: ret.fehler = 'sub: Fehler im linken Term'
        else: ret.fehler = 'sub: Rechter Term ist kein Liquid-Objekt'
        return ret

    def __mul__(self, other):
        ret = Liquid()
        if isinstance(other, int):
            menge_ml = self.menge_ml * other
            vg_ml = self.vg_ml * other
            pg_ml = self.pg_ml * other
            nic_mg = self.nic_mg * other
            nic_mg_p_ml = nic_mg / menge_ml
            vg_prozent = vg_ml * 100 / menge_ml
            pg_prozent = pg_ml * 100 / menge_ml
            ret.set(menge_ml, vg_prozent, pg_prozent, nic_mg_p_ml)
        else: ret.fehler = 'mul: Rechter Term ist kein Int-Objekt'
        return ret
    
class Bunker_mischung:

        def __init__(self, p_liquid):
            self.fehler = ''
            self.bunker_nic_mg_p_ml = 48
            self.__calc(p_liquid)

        def __calc(self, p_liquid):
            if isinstance(p_liquid, Liquid):
                if p_liquid.state():
                    self.bunker_ml = p_liquid.nic_mg / self.bunker_nic_mg_p_ml
                    self.pg_ml = p_liquid.pg_ml - self.bunker_ml
                    self.vg_ml = p_liquid.vg_ml
                    if self.bunker_ml >= 0 and self.pg_ml >= 0 and self.vg_ml >= 0:
                        pass
                    else:
                        self.fehler = 'Mischung: Nicht herstellbar'
                else: self.fehler = 'Liquidfehler: ' + p_liquid.message()
            else: self.fehler = 'Mischung: Objektfehler'
            
        def state(self):
            if self.fehler == '': ret = True
            else: ret = False
            return ret

        def data(self):
            ret = (round(self.bunker_ml, 2), round(self.pg_ml, 2), round(self.vg_ml, 2))
            return ret

        def message(self):
            if self.fehler == '':
                ret = 'Mischung: Aktuell liegt kein Fehler vor'
            else:
                ret = self.fehler
            return ret

        def ausgabe(self):
            ret = ''
            if self.fehler == '':
                ret += str(self.bunker_ml) + ' ml Bunkerbase mit '
                ret += str(self.bunker_nic_mg_p_ml) + ' mg/ml --- '
                ret += str(self.pg_ml) + ' ml PG --- '
                ret += str(self.vg_ml) + ' ml VG'
            else:
                ret += self.fehler 
            return ret


            
        