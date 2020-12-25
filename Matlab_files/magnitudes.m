% computation of the object magnide
%
%
%
% C. Frueh, Sep 9, 2019
%
%
%
%
% comments: Lambertian point source
%
%
%
I0=1361.0; % Watt/m^2 solar constant, value according to IAU
magsun=-26.8; % solar magnitude

sunangle=30*pi/180.0; % rad, angle normal direction to the sun direction
obsangle=0*pi/180.0;  % rad, angle normal direction to the observer direction
dist=300.0*10^3; % meter, distance observer to object; altitude

area=1; %m^2 reflecting area
CD=1; %diffuse/Lambertian reflection parameter


Iobj=I0*cos(sunangle)*1/dist^2*CD*cos(obsangle)* area; % object irradiation
magobj=magsun-2.5*log10(Iobj/I0) % magnitude, not needed for further calculation

rad2arcsec = 180/pi*3600; % conversation radians in arcseconds
%D = pi*1.5^2; %[m2] area of aperture
%d = pi*0.05^2; %[m2] area of obstruction
h = 6.626070040e-34; %[kg m2 s-1] or [J s] Planck constant
c = 299792458; %[m/s] speed of light

% telescope
D=1; % m^2, aperture
d=10*(10^-2)^2; % m^2, obstruction
r_aperture = sqrt(pi*D); % radius aperture
loss=0.8; %unitless

%color or mean wavelength
lambda=600*10^-9; % mean wavelength [m]

% observation conditions
zenith=0*180.0/pi; %rads, zenith angle
tau = 0.1; %  atmospheric extinction
Q = 0.7; % quantum efficiency, unitless
FWHM_seeing = 3; %[arcsecond]

% camera parameters
delta_t = 3; %[s] shutter time
pix = 1; % pixel scale, arcseconds per pixel (size of the camera vs focal length)




E3 = (D-d)*lambda/(h*c)*exp(-tau*1/cosd(zenith))*Iobj*loss;
E3_total = E3*Q*delta_t; %[count]


FWHM_airy = 1.028*lambda/(2*r_aperture); %[rad]
FWHM_airy_arcsec = FWHM_airy*rad2arcsec;

FWHM = max([FWHM_airy,FWHM_seeing])/pix;
sigma = FWHM/(2*sqrt(2*log(2)));

imres = [9,9];
[xmat,ymat] = meshgrid(1:imres(1),1:imres(2));

A_gauss = 0.838*E3_total/(2*pi*sigma^2);
xl = [xmat(:),ymat(:)]-0.5; % orient your coordiantes
xu = xl+1; % orient coordinates
mu = 0.5*imres+0.5;  % place the mean relative to the pixel grid
SIGMA = sigma^2*eye(2,2); %variance over the pixels [pixels]
E_img = reshape(A_gauss*mvncdf(xl,xu,mu,SIGMA),imres); % one way to compute the integral, but can be done by hand
img = poissrnd(E_img); % draw a sample from poisson distribution

figure()
imagesc(img)
colormap(gray(256))
axis equal



