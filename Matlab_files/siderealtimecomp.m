% compare different ways to compute the sidereal time
% Carolin Frueh, 10/6/2016
% updated 10/1/2017
%
%
% set the UT time at which you are interested in the sidereal time
no_years=2016;
no_months=9.0;
no_days=8.0;
no_hours=18.0; % times are in UT
no_minutes=0.0;
no_seconds=0.0;
nom_epoch=jday(no_years,no_months,no_days,no_hours,no_minutes,no_seconds); % julanian date

%%%%%%%%%%%%%%%%%%%%%%%  how it is done in my matlab routine
epo=nom_epoch-2400000.5; % in modified julanian date
% computer sidereal time 
% sidereal time
%%% centuries elapsed since 2000/01/1.5
% JD
TU=(epo-51544.5)/36525.0;
%% GMST in time seconds at 0 UT
gmstjb=24110.54841+8640184.812866*TU+0.093104*TU*TU-(6.2E-6)*TU*TU*TU;
%% corrections for other time than 0 UT modulo rotations
GMSTUT=43200.0+3155760000.0*TU;
gmstjb=gmstjb+mod(GMSTUT,86400.0);
gmstjb=mod(gmstjb/43200.0*pi,2.0*pi);
if gmstjb<0.0
    gmstjb=gmstjb+2.0*pi;
end
sidereal_mymatlab=gmstjb

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% sidereal time exactly how it is in the script, Eq. 4.46
JD0=jday(no_years,no_months,no_days,0.0,0.0,0.0);
JD1=nom_epoch;
T0=(JD0-2451545)/36525.0;
T1=(JD1-2451545)/36525.0;
UTsec=(JD1-JD0)*86400;
if UTsec<0.0
    UTsec=86400+UTsec;
end
theta0=24110.54841+8640184.812866*T0+0.093104*T1*T1-(6.2E-6)*T1*T1*T1+1.0027279093*UTsec;
% transform theta from seconds to radians
%theta0=theta0/86400*2*pi; 86400 seconds in one day, equivalnt to the
%following line:
theta0=theta0/43200*pi;
theta0=mod(theta0,2*pi);
if theta0<0.0
    theta0=theta0+2*pi;
end
siderealscriptprecise=theta0
% difference to sidereal_mymatlab in the order of 10^-6 radians, 10^-10 seconds

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% approximation from script, Eq. 4.47
JD0=jday(no_years,no_months,no_days,0.0,0.0,0.0);
JD1=nom_epoch;
UThours=(JD1-JD0)*24.0;
if UTsec<0.0
    UTsec=24+UTsec;
end
beta0=6.664520+0.0657098244*(JD0-2451544.5)+1.0027279093*UThours;
% transform hours into radians
%beta0=beta0*2*pi/24 24 hours in one day, equivalent to :
beta0=beta0/12*pi;
beta0=mod(beta0,2*pi);
if beta0<0.0
    beta0=theta0+2*pi;
end

siderealtimescriptapprox=beta0

%difference to 10^6 radians to sidereal_mymatlab in the order of 10^-6 radians, 10^-10 seconds
% difference to 10^7 radians to siderealscriptprecise in the order of 10^-6 radians, 10^-12 seconds




