_I='falling'
_H='Parameter State must be True or False'
_G='dict'
_F='list'
_E='ampm'
_D=None
_C=True
_B='little'
_A=False
from PiicoDev_Unified import *
compat_str='\nUnified PiicoDev library out of date.  Get the latest module: https://piico.dev/unified \n'
_I2C_ADDRESS=82
_SEC=0
_MIN=1
_HOUR=2
_DAY=4
_MONTH=5
_YEAR=6
_STATUS=14
_CTRL1=15
_CTRL2=16
_CIM=18
_ECTRL=19
_SECTS=21
_DAYTS=24
_UNIX=27
_REG_ID=40
_EE_CLKOUT=53
_EE_BACKUP=55
def _setBit(x,n):return x|1<<n
def _clearBit(x,n):return x&~(1<<n)
def _writeBit(x,n,b):
	if b==0:return _clearBit(x,n)
	else:return _setBit(x,n)
def _readBit(x,n):return x&1<<n!=0
def _writeCrumb(x,n,c):x=_writeBit(x,n,_readBit(c,0));return _writeBit(x,n+1,_readBit(c,1))
def _writeTribit(x,n,c):x=_writeBit(x,n,_readBit(c,0));x=_writeBit(x,n+1,_readBit(c,1));return _writeBit(x,n+2,_readBit(c,2))
def _bcdDecode(val):return(val>>4)*10+(val&15)
def _bcdEncode(val):return val//10<<4|val%10
class PiicoDev_RV3028:
	def __init__(self,bus=_D,freq=_D,sda=_D,scl=_D,addr=_I2C_ADDRESS):
		try:
			if compat_ind>=1:0
			else:print(compat_str)
		except:print(compat_str)
		self.i2c=create_unified_i2c(bus=bus,freq=freq,sda=sda,scl=scl);self.addr=addr
		try:part=int(self.i2c.readfrom_mem(self.addr,_REG_ID,1))
		except Exception as e:print(i2c_err_str.format(self.addr));raise e
		self.setBatterySwitchover();self.configTrickleCharger();self.setTrickleCharger()
	def _read(self,reg,N):
		try:tmp=int.from_bytes(self.i2c.readfrom_mem(self.addr,reg,N),_B)
		except:print('Error reading from RV3028');return float('NaN')
		return tmp
	def _write(self,reg,data):
		try:self.i2c.writeto_mem(self.addr,reg,data)
		except:print('Error writing to RV3028');return float('NaN')
	def getUnixTime(self):return self._read(_UNIX,4)
	def setUnixTime(self,time):self._write(_UNIX,time.to_bytes(4,_B,_A))
	def setBatterySwitchover(self,state=_C):
		tmp=self._read(_EE_BACKUP,1)
		if state is _C:tmp=_writeCrumb(tmp,2,1)
		elif state is _A:tmp=_writeCrumb(tmp,2,0)
		else:print(_H);return
		self._write(_EE_BACKUP,tmp.to_bytes(1,_B,_A))
	def setTrickleCharger(self,state=_C):
		tmp=self._read(_EE_BACKUP,1)
		if state is _C:tmp=_writeBit(tmp,5,1)
		elif state is _A:tmp=_writeBit(tmp,5,0)
		else:print(_H);return
		self._write(_EE_BACKUP,tmp.to_bytes(1,_B,_A))
	def configTrickleCharger(self,R='3k'):
		tmp=self._read(_EE_BACKUP,1);tmp=_setBit(tmp,7)
		if R=='3k':tmp=_writeCrumb(tmp,0,0)
		elif R=='5k':tmp=_writeCrumb(tmp,0,1)
		elif R=='9k':tmp=_writeCrumb(tmp,0,2)
		elif R=='15k':tmp=_writeCrumb(tmp,0,3)
		else:print("R parameter must be '3k', '5k', '9k', or '15k'");return
		self._write(_EE_BACKUP,tmp.to_bytes(1,_B,_A))
	def configClockOutput(self,clk=32768):
		tmp=self._read(_EE_CLKOUT,1)
		if clk==32768:tmp=_writeTribit(tmp,0,0)
		elif clk==8192:tmp=_writeTribit(tmp,0,1)
		elif clk==1024:tmp=_writeTribit(tmp,0,2)
		elif clk==64:tmp=_writeTribit(tmp,0,3)
		elif clk==32:tmp=_writeTribit(tmp,0,4)
		elif clk==1:tmp=_writeTribit(tmp,0,5)
		elif clk==0:tmp=_writeTribit(tmp,0,7)
		else:print('clk parameter must be 32678, 8192, 1024, 64,32, 1, or 0. Values are in units of Hz.');return
		self._write(_EE_CLKOUT,tmp.to_bytes(1,_B,_A))
	def resetEventInterrupt(self,edge=_I):
		tmp=self._read(_STATUS,1);tmp=_clearBit(tmp,1);self._write(_STATUS,bytes([tmp]));tmp=self._read(_ECTRL,1);tmp=_clearBit(tmp,0)
		if edge==_I:tmp=_clearBit(tmp,6)
		else:tmp=_setBit(tmp,6)
		tmp=_clearBit(tmp,1);tmp=_setBit(tmp,2);self._write(_ECTRL,bytes([tmp]));tmp=self._read(_CTRL2,1);tmp=_setBit(tmp,2);tmp=_setBit(tmp,7);self._write(_CTRL2,bytes([tmp]));tmp=self._write(_ECTRL,bytes([0]))
	def getEventInterrupt(self):
		tmp=self._read(_STATUS,1)
		if _readBit(tmp,1)==1:return _C
		else:return _A
	def setTime(self,time):
		if type(time)==dict:
			timeTmp=[0,0,0,0];timeTmp[0]=time['hour'];timeTmp[1]=time['min'];timeTmp[2]=time['sec']
			if _E in time:timeTmp[3]=time[_E]
			time=timeTmp
		tmp=self._read(_CTRL2,1)
		if len(time)==3:tmp=_writeBit(tmp,1,0);hrs=_bcdEncode(time[0])
		elif len(time)==4:
			tmp=_writeBit(tmp,1,1);hrs=_bcdEncode(time[0])
			if time[3]=='AM':hrs=_clearBit(hrs,5)
			elif time[3]=='PM':hrs=_setBit(hrs,5)
		self._write(_CTRL2,tmp.to_bytes(1,_B,_A));sec=_bcdEncode(time[2]);mins=_bcdEncode(time[1]);t=[sec,mins,hrs];self._write(_SEC,bytes(t))
	def getTime(self,timeFormat=_F,eventTimestamp=_A):
		if eventTimestamp is _A:t=self._read(_SEC,3)
		else:t=self._read(_SECTS,3)
		hrFormat=_readBit(self._read(_CTRL2,1),1);t=t.to_bytes(3,_B,_A);mins=_bcdDecode(t[1]);secs=_bcdDecode(t[0]);hrs=_bcdDecode(t[2])
		if hrFormat==1:
			if _readBit(t[2],5)==0:time=[hrs,mins,secs,'AM']
			else:hrByte=_clearBit(t[2],5);hrs=_bcdDecode(hrByte);time=[hrs,mins,secs,'PM']
		else:time=[hrs,mins,secs]
		if timeFormat==_G:
			timeTmp={'hour':time[0],'min':time[1],'sec':time[2]}
			if len(time)==4:timeTmp[_E]=time[3]
			time=timeTmp
		return time
	def setDate(self,date):
		if type(date)==dict:day=date['day'];month=date['month'];year=date['year']
		else:day=date[0];month=date[1];year=date[2]
		date=[_bcdEncode(day),_bcdEncode(month),_bcdEncode(year)];self._write(_DAY,bytes(date))
	def getDate(self,timeFormat=_F,eventTimestamp=_A):
		if eventTimestamp is _A:tmp=self._read(_DAY,3)
		else:tmp=self._read(_DAYTS,3)
		date=tmp.to_bytes(3,_B,_A);day=_bcdDecode(date[0]);month=_bcdDecode(date[1]);year=_bcdDecode(date[2])
		if timeFormat==_G:date={'day':day,'month':month,'year':year}
		else:date=[day,month,year]
		return date
	def getDateTime(self,timeFormat=_F,eventTimestamp=_A):
		time=self.getTime(timeFormat=timeFormat,eventTimestamp=eventTimestamp);date=self.getDate(timeFormat=timeFormat,eventTimestamp=eventTimestamp)
		if timeFormat==_G:date.update(time);return date
		return date,time
	def timestamp(self):
		A='0';time=self.getTime();date=self.getDate();strYear=str(date[2]+2000);strMonth=str(date[1])
		if date[1]<10:strMonth=A+strMonth
		strDay=str(date[0])
		if date[0]<10:strDay=A+strDay
		strHour=str(time[0])
		if time[0]<10:strHour=A+strHour
		strMinute=str(time[1])
		if time[1]<10:strMinute=A+strMinute
		strSecond=str(time[2])
		if time[2]<10:strSecond=A+strSecond
		timestamp=strYear+'-'+strMonth+'-'+strDay+' '+strHour+':'+strMinute+':'+strSecond
		if len(time)==4:timestamp+=' '+time[3]
		return timestamp
	def clearAllInterrupts(self):self._write(_STATUS,bytes([0]))