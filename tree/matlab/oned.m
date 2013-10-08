clc; clear all; close all;

f = Foned();

% see what indices matter
% sample more there

% making x, sampleAt
nPower = 7;
n = 2^nPower;
t = linspace(0, 5, n);
x = 1 ./ (1 + exp(-8 * (t-2.5)));
x = x' + 1;

sampleAt = zeros(n, 1);
sampleAt(1:4:n) = 1;
sampleAt(15:16) = 1;
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% how far to approx the levels?
m = 3;

%w = f.approxWavelet1D(x, sampleAt, m);
interestedIn = [1 2 3 4 ];
w = f.approxWaveletAndScale(x, sampleAt, interestedIn);



h = f.haarMatrix(n);
wE = h * x;
t = h' * w;

figure()
plot(x, 'r-');
hold on;
plot(t, 'b-');
title('Time');
legend('exact', 'approx', 'Location', 'Best')


figure()
plot(w, 'r-');
hold on;
plot(wE, 'b--');
title('Wavelet');
legend('approx', 'exact', 'Location', 'Best')



