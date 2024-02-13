% date, blank, station number, depth, YSI time, YSI Depth, YSI Temp; YSI
% SpecCond; YSI Salinity; YSI DOsat; YSI DO; YSI pH; YSI Turbidity; YSI
% Chlraw; YSI Chl; YSI BP; Secchi; Kd; blank; blank; POC; PN; CtoN; DOC;
% DIC; NO3/NO2; NH4; DIN; TDN; DON; PO4; Blank; SiO2...

PS_WQ=xlsread('PS_WQ_2021.xlsx');
PS_WQ(:,1) = PS_WQ(:,1)+datenum(1999,10,6)-36439;
PS_WQ_st1=PS_WQ(PS_WQ(:,3)==1,:);

time_uniq=unique(PS_WQ_st1(:,1));

for tt=1:length(time_uniq)
    ind=find(PS_WQ_st1(:,1)==time_uniq(tt));
    if(~isempty(ind))
    PS_WQ_st1_top(tt,:)=PS_WQ_st1(ind(1),:);
    end
end

plot(PS_WQ_st1_top(:,1),PS_WQ_st1_top(:,7),'-b','linewidth',2)
xlim([datenum(2019,1,1) datenum(2020,1,1)])
