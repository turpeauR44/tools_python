# -*- coding: utf-8 -*-
"""
Created on Sun Sep  6 23:02:59 2020

@author: turpeau.romain
"""
from datetime import datetime

digit2 = lambda myint: '0{}'.format(myint) if  myint<10 else str(myint)

def now():
    '''
    Return current datetime
    '''
    return datetime.now()

def file_stamps(date=now(), time=True, file=""):
    '''
    Return current 'YYmmdd' by default
            <date> 'YYmmdd' if needed 
            with time details : 'YYMMdd_HHMMSS' if <time> set at True
    '''
    date_str = '{}{}{}_'.format(date.year-2000,digit2(date.month),digit2(date.day))
    if time:
        try:
            date_str = '{}{}{}{}_'.format(date_str,digit2(date.hour),digit2(date.minute),digit2(date.second))
        except:
            date_str = '{}00000_'.format(date_str)

    return '{}_{}'.format(date_str,file)


class Date:
    def __init__(self,val, **kwargs):
        '''
        val : date value
        init_type='datetime': input type  ['datetime', 'date', 'iso', 'sql']
        now:=False, replace by current datetime if value  in [None, ""]
        notnull=False True if value excepted
        '''
        #kwargs:
        self.init_type = kwargs.get('type','datetime')
        self.now = kwargs.get('now',False)
        self.notnull = kwargs.get('notnull', False)

        nullValues = [None,""]

        if val in nullValues:
            if self.now: 
                self.Datetime = datetime.now()
            else:
                if self.notnull:
                    print('Warning: Date expected, current date has been added')
                    self.Datetime = datetime.now()
                else:
                    self.Datetime = None
        else:
            if  self.init_type == 'datetime':
                self.Datetime = val
            elif init_type =='iso':
                self.Datetime = datetime.fromisoformat(val)

    def sql(self, **kwargs):
        '''
        time=True, True if False not requested
        date_format='ymd', other type could be used 
        '''
        date_format = kwargs.get('date_format', 'ymd')
        
        if self.Datetime == None:
            return None

        sql_txt = ""
        if date_format=='ymd': 
            sql_txt = '{}-{}-{}'.format(self.Datetime.year, self.Datetime.month, self.Datetime.day)
        elif date_format=='ydm': 
            sql_txt = '{}-{}-{}'.format(self.Datetime.year, self.Datetime.day, self.Datetime.month) 

        if kwargs.get('time',True):
            sql_txt = '{} {}:{}:{}'.format(sql_txt, self.Datetime.hour, self.Datetime.minute, self.Datetime.second)

        return sql_txt

transfrom_Isodatetime = lambda IsoDate:  datetime.datetime.strptime(IsoDate.split('.')[0] , "%Y-%m-%dT%H:%M:%S") if IsoDate!=None else None     
transfrom_Isodate = lambda IsoDate:  datetime.datetime.strptime(IsoDate.split('.')[0] , "%Y-%m-%d").date() if IsoDate!=None else None      

transTo_Isodate = lambda date: "'{}-{}-{}'".format(date.year,date.month,date.day)  if date!=None else ''    


get_Isodate = lambda IsoDate: transfrom_Isodate(IsoDate).date() if IsoDate!=None else datetime.datetime.now().date()  

get_todaydate = lambda : datetime.datetime.now().date()

get_now = lambda : datetime.datetime.now()

transTo_Filedate = lambda date: "{}{}{}".format(digit2_Year(date), digit2_Month(date), digit2_Day(date)) 

digit2_Year = lambda date: date.year-2000
digit2 = lambda myint: '0{}'.format(date.month) if date.month<10 else str(date.month)
digit2_Day = lambda date: '0{}'.format(date.day) if date.day<10 else str(date.day)


#def get_todaydate():
    #return datetime.datetime.now().date()


def myworkdays(d, end, excluded=(6, 7)):
    days = []
    if type(d)!=type(get_todaydate()):
        try:
            d = d.date()
        except:
            raise Exception('format incompatible')
    if type(end)!=type(get_todaydate()):
        try:
            end = end.date()
        except:
            raise Exception('format incompatible')

    while d <= end:
        if d.isoweekday() not in excluded:
            days.append(d)
        d += datetime.timedelta(days=1)
    return days

def lap_workingdays_unsigned(date1, date2):
    n=0
    while date1 > date2:
        if date2.isoweekday() not in [6,7]:
            n+=1
        date2= date2 + datetime.timedelta(days=1)
    return n

def lap_workingdays(date1, date2):
    n = 0
    if date1==date2:
        return 0
    elif date1>date2:
        return - lap_workingdays_unsigned(date1, date2)
    else:
        return lap_workingdays_unsigned(date2, date1)


def date_calc(d, nbjours):
    Signe = int(nbjours/abs(nbjours))
    if nbjours != int(nbjours):
        nbjours = nbjours+1
    nbjours = int(abs(nbjours))   
    
    for nbjours in range(nbjours):
        if (d+Signe*datetime.timedelta(days=1)).isoweekday() in [6,7]:
            d = d + 3*Signe*datetime.timedelta(days=1)
        else:
            d = d + Signe*datetime.timedelta(days=1)
    return d

def date_recalc(date1, date2, nbworkingdays):
    '''
    purpose is to confirm that d1 > d2 + nbworkingdays
    return d2 if yes or return d1 - nbworkingdays else
    '''
    #first count nb of working days between those to dates:
    real_nbworkingdays = lap_workingdays(date2, date1)
    if real_nbworkingdays < nbworkingdays > 0 :
       return date_calc(date2, - nbworkingdays),True
    else:
        return date2,False
    
if __name__=='__main__':
    print(get_todaydate())
    print(digit2_Year(datetime.datetime.now()))
    print(transTo_Filedate(get_todaydate()))