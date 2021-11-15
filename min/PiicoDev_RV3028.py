_H='falling'
_G='Parameter State must be True or False'
_F='dict'
_E='list'
_D='ampm'
_C=True
_B='little'
_A=False
from machine import I2C,Pin
_ADDR=82
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
_ID=40
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
class rv3028:
	def __init__(A,i2c=None):
		B=i2c
		if isinstance(B,I2C)is _A:print('RV3028 requires a valid i2c device');raise TypeError
		A.i2cDev=B
		try:D=int(B.readfrom_mem(_ADDR,_ID,1))
		except Exception as C:print('Failed to find RV3028 on i2c bus');raise C
		A.setBatterySwitchover();A.configTrickleCharger();A.setTrickleCharger()
	def _read(A,reg,N):
		try:B=int.from_bytes(A.i2cDev.readfrom_mem(_ADDR,reg,N),_B)
		except:print('Error reading from RV3028');return float('NaN')
		return B
	def _write(A,reg,data):
		try:A.i2cDev.writeto_mem(_ADDR,reg,data)
		except:print('Error writing to RV3028');return float('NaN')
	def getUnixTime(A):return A._read(_UNIX,4)
	def setUnixTime(A,time):A._write(_UNIX,time.to_bytes(4,_B,_A))
	def setBatterySwitchover(B,state=_C):
		C=state;A=B._read(_EE_BACKUP,1)
		if C is _C:A=_writeCrumb(A,2,1)
		elif C is _A:A=_writeCrumb(A,2,0)
		else:print(_G);return
		B._write(_EE_BACKUP,A.to_bytes(1,_B,_A))
	def setTrickleCharger(B,state=_C):
		C=state;A=B._read(_EE_BACKUP,1)
		if C is _C:A=_writeBit(A,5,1)
		elif C is _A:A=_writeBit(A,5,0)
		else:print(_G);return
		B._write(_EE_BACKUP,A.to_bytes(1,_B,_A))
	def configTrickleCharger(B,R='3k'):
		A=B._read(_EE_BACKUP,1);A=_setBit(A,7)
		if R=='3k':A=_writeCrumb(A,0,0)
		elif R=='5k':A=_writeCrumb(A,0,1)
		elif R=='9k':A=_writeCrumb(A,0,2)
		elif R=='15k':A=_writeCrumb(A,0,3)
		else:print("R parameter must be '3k', '5k', '9k', or '15k'");return
		B._write(_EE_BACKUP,A.to_bytes(1,_B,_A))
	def configClockOutput(C,clk=32768):
		B=clk;A=C._read(_EE_CLKOUT,1)
		if B==32768:A=_writeTribit(A,0,0)
		elif B==8192:A=_writeTribit(A,0,1)
		elif B==1024:A=_writeTribit(A,0,2)
		elif B==64:A=_writeTribit(A,0,3)
		elif B==32:A=_writeTribit(A,0,4)
		elif B==1:A=_writeTribit(A,0,5)
		elif B==0:A=_writeTribit(A,0,7)
		else:print('clk parameter must be 32678, 8192, 1024, 64,32, 1, or 0. Values are in units of Hz.');return
		C._write(_EE_CLKOUT,A.to_bytes(1,_B,_A))
	def resetEventInterrupt(B,edge=_H):
		A=B._read(_STATUS,1);A=_clearBit(A,1);B._write(_STATUS,bytes([A]));A=B._read(_ECTRL,1);A=_clearBit(A,0)
		if edge==_H:A=_clearBit(A,6)
		else:A=_setBit(A,6)
		A=_clearBit(A,1);A=_setBit(A,2);B._write(_ECTRL,bytes([A]));A=B._read(_CTRL2,1);A=_setBit(A,2);A=_setBit(A,7);B._write(_CTRL2,bytes([A]));A=B._write(_ECTRL,bytes([0]))
	def getEventInterrupt(A):
		B=A._read(_STATUS,1)
		if _readBit(B,1)==1:return _C
		else:return _A
	def setTime(D,time):
		A=time
		if type(A)==dict:
			timeTmp[0]=A['hour'];timeTmp[1]=A['min'];timeTmp[2]=A['sec']
			if _D in A:timeTmp[3]=A[_D]
			A=timeTmp
		C=D._read(_CTRL2,1)
		if len(A)==3:C=_writeBit(C,1,0);B=_bcdEncode(A[0])
		elif len(A)==4:
			C=_writeBit(C,1,1);B=_bcdEncode(A[0])
			if A[3]=='AM':B=_clearBit(B,5)
			elif A[3]=='PM':B=_setBit(B,5)
		D._write(_CTRL2,C.to_bytes(1,_B,_A));E=_bcdEncode(A[2]);F=_bcdEncode(A[1]);G=[E,F,B];D._write(_SEC,bytes(G))
	def getTime(D,timeFormat=_E,eventTimestamp=_A):
		if eventTimestamp is _A:B=D._read(_SEC,3)
		else:B=D._read(_SECTS,3)
		H=_readBit(D._read(_CTRL2,1),1);B=B.to_bytes(3,_B,_A);E=_bcdDecode(B[1]);F=_bcdDecode(B[0]);C=_bcdDecode(B[2])
		if H==1:
			if _readBit(B[2],5)==0:A=[C,E,F,'AM']
			else:I=_clearBit(B[2],5);C=_bcdDecode(I);A=[C,E,F,'PM']
		else:A=[C,E,F]
		if timeFormat==_F:
			G={'hour':A[0],'min':A[1],'sec':A[2]}
			if len(A)==4:G[_D]=A[3]
			A=G
		return A
	def setDate(E,date):
		A=date
		if type(A)==dict:B=data['day'];C=data['month'];D=data['year']
		else:B=A[0];C=A[1];D=A[2]
		A=[_bcdEncode(B),_bcdEncode(C),_bcdEncode(D)];E._write(_DAY,bytes(A))
	def getDate(B,timeFormat=_E,eventTimestamp=_A):
		if eventTimestamp is _A:C=B._read(_DAY,3)
		else:C=B._read(_DAYTS,3)
		A=C.to_bytes(3,_B,_A);D=_bcdDecode(A[0]);E=_bcdDecode(A[1]);F=_bcdDecode(A[2])
		if timeFormat==_F:A={'day':D,'month':E,'year':F}
		else:A=[D,E,F]
		return A
	def getDateTime(C,timeFormat=_E,eventTimestamp=_A):
		D=eventTimestamp;A=timeFormat;E=C.getTime(timeFormat=A,eventTimestamp=D);B=C.getDate(timeFormat=A,eventTimestamp=D)
		if A==_F:B.update(E);return B
		return B,E
	def timestamp(C):
		A=C.getTime();B=C.getDate();D=str(B[2]+2000)+'-'+str(B[1])+'-'+str(B[0])+' '+str(A[0])+':'+str(A[1])+':'+str(A[2])
		if len(A)==4:D+=' '+A[3]
		return D
	def clearAllInterrupts(A):A._write(_STATUS,bytes([0]))