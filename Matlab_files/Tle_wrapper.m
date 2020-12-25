% wrapper to propagate TLE objects
% 
% Author Carolin Frueh
% creation date: 8/31/2017
% last modified: 8/26/2019
% based on vallado's routines (celestrack.com), code distribtution blackboard August 2019
%
%
% errata and modifications:
% added julianian date 9/4/2017
% added GEO and other criteria and plotting 9/4/2017
% cleaned up satrec call 8/25/2019
% added alternative for tsince computation 8/25/2019
%

clear all;
% open tle file
% initialize count parameters
cc=0;
dd=0;

% gravitational parameter
mu=398600.4418;      % km3/s2

% absolute target time
no_years=2019;
no_months=8.0;
no_days=27.0;
no_hours=14.0; % times are in UT
no_minutes=30.0;
no_seconds=0.0;

% open TLE file for sequential read in
fid = fopen('TLEcatalog.txt'); % load the TL

tline2='gg';
while ischar(tline2)
    cc = cc+1 % counter
    name = fgets(fid);% for the ones with three lines
    tline1 = fgets(fid); % first line of TLE
    tline2 = fgets(fid); % second line of TLE

    if tline2>0
        % initialize
        [satrec, startmfe, stopmfe, deltamin]=twoline2rv(721,tline1,tline2,'c','d');

        % complete year with four digits instead of two (input for day2mdh)
        if (satrec.epochyr < 57)
          satrec.epochyr= satrec.epochyr + 2000;
        else
          satrec.epochyr= satrec.epochyr + 1900;
        end

        % determine epoch of the specific TLE set, called nominal epoch
        [tle_mon,tle_day,tle_hr,tle_minute,tle_sec] = days2mdh (satrec.epochyr, satrec.epochdays );
        tle_jdsatepoch = jday(satrec.epochyr,tle_mon,tle_day,tle_hr,tle_minute,tle_sec);

        nom_epoch=jday(no_years,no_months,no_days,no_hours,no_minutes,no_seconds);
        
        % compute difference from desired to nominal
        diff_epochjd=nom_epoch-tle_jdsatepoch; % difference in fractions of days
        
        
        % determine the time since the nominal epoch in minutes (1440 minutes in
        % one day)
        tsince=1440.0*diff_epochjd;

        % osculating position r and velocity v
        [satrec, r, v] = sgp4(satrec,tsince); % unites km and km/s
        
        % if desired transform it back into orbital elements
        [p,a,ecc,incl,omega,argp,nu,m,arglat] = rv2coe (r,v,mu);
        
        % save the state, it would be better initialize than growing in loop
            dd=dd+1
            Rsave1(cc)=r(1);
            Rsave2(cc)=r(2);
            Rsave3(cc)=r(3);
     
    end
end

% quick and dirty 3D plot
if dd>0
     plot3(Rsave1,Rsave2,Rsave3,'.') % units for axis!
     legend("TLE catalog")
     xlabel("[km]")
     ylabel("[km]")
     xlabel("[km]")
end 


%%%%alternative, only valid if the nominal and desired time is within the same
%%%%year, input number of days in the year (nodaysinyear), minutes
%%%%(nomin) and seconds (nosec) of desired epoch
% % tsince in minutes
% desiredEpochMin = nodaysinyear * 1440 + nomin+ nosec/60; % minutes
% tsince = desiredEpochMin - satrec(1).epochdays*1440; % time passed since the
% epoch listed in the TLEs
