clear all
close all
clc
%システム設定
LengthOfWaveform = 1000; % 波形長
X_Nums = 365+1; % X方向の点数
Y_Nums = 32+1; % Y方向の点数
n = X_Nums*Y_Nums; % 走査点数
X_Inter = 0.415; % 長手方向の点間距離(m)
Y_Inter = 0.417; % 幅方向の点間距離(m)        
X_range = X_Inter*(0:X_Nums-1);
Y_range = Y_Inter*(0:Y_Nums-1);
SamplingRate = 5000000;
TimeInterval = 1/SamplingRate;
t=TimeInterval*(1:LengthOfWaveform);


%プログラムファイル読み込み、バイナリデータを解答
fileID = fopen('wave.dat'); % ファイルを開く
Data_Binary = fread(fileID,[LengthOfWaveform n],'int16','b' ); % バイナリデータを符号付き16ビットの整数、かつビッグエンディアン順で読み込む
fclose(fileID);% 読み込み終了


%%
% generate 3D matrix
Wavefield=zeros(Y_Nums,X_Nums,LengthOfWaveform);
for i=1:LengthOfWaveform
    XY_1=reshape(Data_Binary(i,:),Y_Nums,X_Nums);
    Wavefield(:,:,i)=XY_1;
end
%%
% extract a line along  x-direction
y=reshape(Wavefield(16,:,:), [X_Nums,LengthOfWaveform]);
Fy = fft2(y);
Fy1=fftshift(log(abs(Fy))); 
FFy=abs(Fy1);

ds=0.415e-3;  % X_inter

F=linspace(-1/(2*TimeInterval),1/(2*TimeInterval),LengthOfWaveform);     %频率范围
K=linspace(-pi/(1*ds),pi/(1*ds),X_Nums); %波数

L=0:ds:(X_Nums-1)*ds;


% wavefield
figure(1)
imagesc(t,L,y');
set(gca,'XDir','normal')
ylabel('Distance (m)');
xlabel('Time (s)');
% caxis([-2e-1,2e-1]);

% wavenumber
figure(2)
imagesc(K,F,FFy');hold on;
set(gca,'YDir','normal')
xlim([0,3000]);
ylim([0,5e5]);
xlabel('Wavenumber (1/m)');
ylabel('Frequency (Hz)');
%%
% interrupt
[KI,FI]=meshgrid(0:1:5000,(10e5:-20:0));
FyI = interp2(K,F,FFy',KI,FI,'spline');
figure(3)
imagesc(KI(1,:),FI(:,1),FyI);hold on
set(gca,'YDir','normal')
ylim([0,10E5]);
xlim([0,5000]);
xlabel('Wavenumber (1/m)');
ylabel('Frequency (Hz)');


%%
% comparison
load('Al_A_mode.mat')
load('Al_S_mode.mat')
load('A_mode.mat')
load('S_mode.mat')

h1=0.5;
h=13.7;
A_Lamb=table2array(A_Lamb);
S_Lamb=table2array(S_Lamb);
Al_A_Lamb=table2array(Al_A_Lamb);
Al_S_Lamb=table2array(Al_S_Lamb);
% figure(3)
plot(A_Lamb(:,4)*1e3,A_Lamb(:,1)*1e6/h,'r--','linewidth',2);hold on
% plot(A_Lamb(:,8)*1e3,A_Lamb(:,5)*1e6/h,'w--','linewidth',2);hold on
plot(S_Lamb(:,4)*1e3,S_Lamb(:,1)*1e6/h,'r-','linewidth',2);hold on
% plot(S_Lamb(:,4)*1e3,S_Lamb(:,3)*1e6/h,'w-','linewidth',2);hold on
plot(Al_A_Lamb(:,2)*1e3,Al_A_Lamb(:,1)*1e6/h1,'wo','linewidth',1);hold on
plot(Al_S_Lamb(:,2)*1e3,Al_S_Lamb(:,1)*1e6/h1,'w*','linewidth',1);hold on




